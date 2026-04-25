from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate

# === 正確的絕對 import（推薦方式） ===
from app.models import db, User, Product, Review, CartItem, Message, Category, Notification
from app.forms import RegistrationForm, LoginForm, ProductForm, ReviewForm, CategoryForm, EditProductForm, UpdateUserForm

from werkzeug.security import generate_password_hash
import os
import logging
from logging.handlers import RotatingFileHandler
import datetime

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 配置日志系统
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10485760, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('微型商店應用啟動')

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from sqlalchemy.orm import Session
        return db.session.get(User, int(user_id))

    # create tables immediately when the app is created (Flask 3 removed before_first_request)
    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        # 支持搜索功能
        query = request.args.get('q', '').strip()
        categories = Category.query.order_by(Category.id).all()
        
        products_query = Product.query.filter_by(is_active=True)
        
        if query:
            # 按名稱或描述搜索
            products = products_query.filter(
                (Product.name.ilike(f'%{query}%')) | 
                (Product.description.ilike(f'%{query}%'))
            ).order_by(Product.id.desc()).all()
            app.logger.info(f'用戶搜索: {query}, 找到 {len(products)} 個商品')
        else:
            products = products_query.order_by(Product.id.desc()).all()
        
        return render_template('index.html', products=products, categories=categories, search_query=query)

    # 商業賬號 - 商家儀表板 (查看自己的商品)
    @app.route('/merchant/dashboard')
    @login_required
    def merchant_dashboard():
        if not (current_user.is_merchant or current_user.is_admin):
            flash('只有商戶可以訪問此頁面。')
            return redirect(url_for('index'))
        
        products = Product.query.filter_by(merchant_id=current_user.id).order_by(Product.id.desc()).all()
        return render_template('merchant_dashboard.html', products=products)

    # 商業賬號 - 編輯產品
    @app.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_product(product_id):
        product = Product.query.get_or_404(product_id)
        
        # 確認只有商品所有者或管理員可以編輯
        if product.merchant_id != current_user.id and not current_user.is_admin:
            flash('無權限編輯此商品。')
            return redirect(url_for('index'))
        
        form = EditProductForm()
        if form.validate_on_submit():
            product.name = form.name.data
            product.description = form.description.data
            product.price = form.price.data
            db.session.commit()
            flash('商品已更新。')
            return redirect(url_for('merchant_dashboard'))
        elif request.method == 'GET':
            form.name.data = product.name
            form.description.data = product.description
            form.price.data = product.price
        
        return render_template('edit_product.html', form=form, product=product)

    # 商業賬號 - 下架產品
    @app.route('/product/<int:product_id>/deactivate', methods=['POST'])
    @login_required
    def deactivate_product(product_id):
        product = Product.query.get_or_404(product_id)
        
        # 確認只有商品所有者或管理員可以下架
        if product.merchant_id != current_user.id and not current_user.is_admin:
            flash('無權限下架此商品。')
            return redirect(url_for('index'))
        
        product.is_active = False
        db.session.commit()
        flash('商品已下架。')
        return redirect(url_for('merchant_dashboard'))

    # 商業賬號 - 重新上架產品
    @app.route('/product/<int:product_id>/activate', methods=['POST'])
    @login_required
    def activate_product(product_id):
        product = Product.query.get_or_404(product_id)
        
        # 確認只有商品所有者或管理員可以上架
        if product.merchant_id != current_user.id and not current_user.is_admin:
            flash('無權限上架此商品。')
            return redirect(url_for('index'))
        
        product.is_active = True
        db.session.commit()
        flash('商品已上架。')
        return redirect(url_for('merchant_dashboard'))

    # 分類管理
    @app.route('/categories')
    @login_required
    def category_list():
        categories = Category.query.order_by(Category.id).all()
        return render_template('category_list.html', categories=categories)

    @app.route('/category/add', methods=['GET', 'POST'])
    @login_required
    def add_category():
        if not current_user.is_admin:
            flash('只有管理員可以新增分類。')
            return redirect(url_for('category_list'))
        form = CategoryForm()
        if form.validate_on_submit():
            c = Category(name=form.name.data)
            db.session.add(c)
            db.session.commit()
            flash('分類已新增。')
            return redirect(url_for('category_list'))
        return render_template('add_category.html', form=form)

    @app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_category(category_id):
        if not current_user.is_admin:
            flash('只有管理員可以編輯分類。')
            return redirect(url_for('category_list'))
        category = Category.query.get_or_404(category_id)
        form = CategoryForm(obj=category)
        if form.validate_on_submit():
            category.name = form.name.data
            db.session.commit()
            flash('分類已更新。')
            return redirect(url_for('category_list'))
        return render_template('edit_category.html', form=form, category=category)

    @app.route('/category/<int:category_id>/delete', methods=['POST'])
    @login_required
    def delete_category(category_id):
        if not current_user.is_admin:
            flash('只有管理員可以刪除分類。')
            return redirect(url_for('category_list'))
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        flash('分類已刪除。')
        return redirect(url_for('category_list'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        # 選擇帳號類型頁面
        if request.method == 'POST':
            return redirect(url_for('register_user'))
        return render_template('register.html')

    @app.route('/register/user', methods=['GET', 'POST'])
    def register_user():
        form = RegistrationForm()
        if form.validate_on_submit():
            is_admin = (User.query.count() == 0)  # 第一個用戶為管理員
            user = User(
                username=form.username.data,
                email=form.email.data,
                is_admin=is_admin,
                is_merchant=False  # 普通用戶
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            app.logger.info(f'新普通用戶註冊: {form.username.data}')
            flash('普通用戶註冊成功，請登入。')
            return redirect(url_for('login'))
        return render_template('register_user.html', form=form)

    @app.route('/register/merchant', methods=['GET', 'POST'])
    def register_merchant():
        form = RegistrationForm()
        if form.validate_on_submit():
            is_admin = (User.query.count() == 0)  # 第一個用戶為管理員
            user = User(
                username=form.username.data,
                email=form.email.data,
                is_admin=is_admin,
                is_merchant=True  # 商家用戶
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            app.logger.info(f'新商家用戶註冊: {form.username.data}')
            flash('商家用戶註冊成功，請登入。')
            return redirect(url_for('login'))
        return render_template('register_merchant.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                user_type = '管理員' if user.is_admin else ('商家' if user.is_merchant else '普通用戶')
                app.logger.info(f'{user_type} {form.username.data} 已登入')
                flash(f'登入成功，歡迎 {user.username}！')
                return redirect(url_for('index'))
            app.logger.warning(f'登入失敗: 用戶名 {form.username.data}')
            flash('使用者或密碼錯誤。')
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        username = current_user.username
        logout_user()
        app.logger.info(f'用戶 {username} 已登出')
        flash('已登出。')
        return redirect(url_for('index'))

    @app.route('/product/add', methods=['GET', 'POST'])
    @login_required
    def add_product():
        # only merchant or admin can add
        if not (current_user.is_merchant or current_user.is_admin):
            flash('需要商戶或管理者權限。')
            return redirect(url_for('index'))
        form = ProductForm()
        if form.validate_on_submit():
            p = Product(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                merchant_id=current_user.id
            )
            db.session.add(p)
            db.session.commit()
            flash('商品已新增。')
            return redirect(url_for('index'))
        return render_template('add_product.html', form=form)

    @app.route('/product/<int:product_id>', methods=['GET', 'POST'])
    def product_detail(product_id):
        product = Product.query.get_or_404(product_id)
        form = ReviewForm()
        if form.validate_on_submit():
            if not current_user.is_authenticated:
                flash('請先登入才能留言與評分。')
                return redirect(url_for('login'))
            review = Review(rating=form.rating.data, content=form.content.data, user_id=current_user.id, product_id=product.id)
            db.session.add(review)
            db.session.commit()
            flash('已新增評價。')
            return redirect(url_for('product_detail', product_id=product.id))
        reviews = Review.query.filter_by(product_id=product.id).order_by(Review.id.desc()).all()
        return render_template('product.html', product=product, reviews=reviews, form=form)

    @app.route('/cart')
    @login_required
    def cart():
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        total = sum(item.subtotal() for item in cart_items)
        return render_template('cart.html', cart_items=cart_items, total=total)

    @app.route('/cart/add/<int:product_id>', methods=['POST'])
    @login_required
    def add_to_cart(product_id):
        product = Product.query.get_or_404(product_id)
        cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(user_id=current_user.id, product_id=product_id)
            db.session.add(cart_item)
            
        db.session.commit()
        flash('商品已加入購物車。')
        return redirect(url_for('cart'))

    @app.route('/cart/update/<int:item_id>', methods=['POST'])
    @login_required
    def update_cart(item_id):
        item = CartItem.query.get_or_404(item_id)
        if item.user_id != current_user.id:
            flash('無權限進行此操作。')
            return redirect(url_for('cart'))
            
        action = request.form.get('action')
        if action == 'increase':
            item.quantity += 1
        elif action == 'decrease':
            if item.quantity > 1:
                item.quantity -= 1
            else:
                db.session.delete(item)
                
        db.session.commit()
        return redirect(url_for('cart'))

    @app.route('/cart/remove/<int:item_id>', methods=['POST'])
    @login_required
    def remove_from_cart(item_id):
        item = CartItem.query.get_or_404(item_id)
        if item.user_id != current_user.id:
            flash('無權限進行此操作。')
            return redirect(url_for('cart'))
            
        db.session.delete(item)
        db.session.commit()
        flash('商品已從購物車移除。')
        return redirect(url_for('cart'))

    @app.route('/messages')
    @app.route('/messages/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def messages(user_id=None):
        # 獲取所有聊天過的用戶
        messages_sent = Message.query.filter_by(sender_id=current_user.id).with_entities(Message.receiver_id).distinct()
        messages_received = Message.query.filter_by(receiver_id=current_user.id).with_entities(Message.sender_id).distinct()
        contact_ids = set([r[0] for r in messages_sent] + [r[0] for r in messages_received])
        contacts = User.query.filter(User.id.in_(contact_ids) if contact_ids else False).all()

        other_user = None
        messages = []
        
        if user_id:
            other_user = User.query.get_or_404(user_id)
            if request.method == 'POST':
                content = request.form.get('content')
                if content:
                    message = Message(
                        content=content,
                        sender_id=current_user.id,
                        receiver_id=user_id
                    )
                    db.session.add(message)
                    db.session.commit()
                    return redirect(url_for('messages', user_id=user_id))
            
            # 獲取與特定用戶的對話
            messages = Message.query.filter(
                ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
                ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
            ).order_by(Message.created_at.asc()).all()

        return render_template(
            'messages.html',
            contacts=contacts,
            other_user=other_user,
            messages=messages
        )

    # 用戶個人頁面
    @app.route('/profile')
    @login_required
    def profile():
        user = current_user
        products_count = Product.query.filter_by(merchant_id=user.id).count() if user.is_merchant else 0
        reviews_count = Review.query.filter_by(user_id=user.id).count()
        return render_template('profile.html', user=user, products_count=products_count, reviews_count=reviews_count)

    # 編輯個人頁面
    @app.route('/profile/edit', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        form = UpdateUserForm()
        if form.validate_on_submit():
            # 檢查username是否已被使用
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user and existing_user.id != current_user.id:
                flash('此用戶名已被使用。')
                return redirect(url_for('edit_profile'))
            
            current_user.username = form.username.data
            
            if form.password.data:
                current_user.set_password(form.password.data)
            
            current_user.bio = form.bio.data
            current_user.phone = form.phone.data
            current_user.address = form.address.data
            
            db.session.commit()
            flash('個人資料已更新。')
            return redirect(url_for('profile'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.bio.data = current_user.bio
            form.phone.data = current_user.phone
            form.address.data = current_user.address
        
        return render_template('edit_profile.html', form=form)

    # 訊息通知頁面
    @app.route('/notifications')
    @login_required
    def notifications():
        notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
        unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        return render_template('notifications.html', notifications=notifications, unread_count=unread_count)

    # 標記通知為已讀
    @app.route('/notification/<int:notification_id>/read', methods=['POST'])
    @login_required
    def mark_notification_read(notification_id):
        notification = Notification.query.get_or_404(notification_id)
        if notification.user_id != current_user.id:
            flash('無權限進行此操作。')
            return redirect(url_for('notifications'))
        notification.is_read = True
        db.session.commit()
        return redirect(url_for('notifications'))

    # 獲取未讀通知數（用於AJAX）
    @app.route('/api/unread-notifications-count')
    @login_required
    def get_unread_notifications_count():
        count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        return jsonify({'count': count})

    # 刪除通知
    @app.route('/notification/<int:notification_id>/delete', methods=['POST'])
    @login_required
    def delete_notification(notification_id):
        notification = Notification.query.get_or_404(notification_id)
        if notification.user_id != current_user.id:
            flash('無權限進行此操作。')
            return redirect(url_for('notifications'))
        db.session.delete(notification)
        db.session.commit()
        flash('通知已刪除。')
        return redirect(url_for('notifications'))

    return app

if __name__ == '__main__':
    app = create_app()
    # bind to 0.0.0.0 so host machine can access the dev server (useful in containers)
    port = int(os.environ.get('PORT', 8080))
    is_dev = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=is_dev)
