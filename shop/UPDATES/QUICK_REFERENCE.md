# 快速参考 - 新功能指南

## 🚀 快速开始

### 1. 分离的注册流程
```
浏览器访问: http://localhost:8080/register
↓
选择用户类型页面
├─ 左侧: 普通用户 (蓝色) → /register/user
└─ 右侧: 商家用户 (绿色) → /register/merchant
```

### 2. 用户类型标识
```
导航栏显示:
- 👑 管理員 (红色徽章)
- 🏪 商家 (绿色徽章)  
- 👤 會員 (青色徽章)

个人页面:
- 头像为渐变背景
- 颜色同徽章一致
```

### 3. 搜索商品
```
方式1: 使用导航栏搜索框
方式2: 直接访问 /?q=关键词

示例:
- /?q=手机
- /?q=衣服
- /?q=电脑
```

### 4. 首页显示
```
首页排版:
分类1 (n件商品)
├─ [商品卡片] [商品卡片] ...
│
分类2 (n件商品)
├─ [商品卡片] [商品卡片] ...
│
其他商品 (n件商品)
└─ [商品卡片] [商品卡片] ...
```

### 5. 查看日志
```
位置: /workspaces/FYP-A20/logs/app.log

查看最近日志:
tail -f logs/app.log

查看所有日志:
cat logs/app.log
```

---

## 📊 路由对照表

| 功能 | 路由 | 方法 | 权限要求 |
|------|------|------|---------|
| 选择注册类型 | `/register` | GET/POST | 无 |
| 普通用户注册 | `/register/user` | GET/POST | 无 |
| 商家注册 | `/register/merchant` | GET/POST | 无 |
| 登入 | `/login` | GET/POST | 无 |
| 登出 | `/logout` | GET | 登入用户 |
| 首页（支持搜索） | `/` | GET | 无 |
| 个人资料 | `/profile` | GET | 登入用户 |
| 商家中心 | `/merchant/dashboard` | GET | 商家/管理员 |

---

## 🔍 搜索功能详解

### 搜索示例

```
基本搜索:
http://localhost:8080/?q=手机

多词搜索:
http://localhost:8080/?q=苹果手机
(会搜索名称或描述中包含"苹果手机"的商品)

空搜索:
http://localhost:8080/?q=
(显示所有商品按分类)
```

### 搜索字段

搜索会在以下字段中查找:
- `Product.name` - 商品名称
- `Product.description` - 商品描述

### 搜索日志

每次搜索都会记录:
```
2026-01-09 16:00:15,234 INFO: 用户搜索: 手机, 找到 5 个商品 [...]
```

---

## 📈 日志监控

### 查看实时日志
```bash
cd /workspaces/FYP-A20
tail -f logs/app.log
```

### 查看特定事件
```bash
# 查看所有登入事件
grep "已登入" logs/app.log

# 查看所有注册事件
grep "註冊" logs/app.log

# 查看搜索记录
grep "用户搜索" logs/app.log

# 查看登入失败
grep "登入失敗" logs/app.log
```

### 日志文件管理
```
位置: /workspaces/FYP-A20/logs/

自动轮转规则:
- 单个文件最大: 10MB
- 保留备份数: 10个
- 文件名: app.log, app.log.1, app.log.2...
```

---

## 💡 使用提示

### 注册流程
1. 新用户访问 `/register`
2. 看到两个选项: 普通用户 或 商家
3. 点击相应按钮进入注册页面
4. 注册成功后跳转到登入页

### 权限管理
- 第一个注册的用户自动成为管理员
- 商家和普通用户在注册时决定
- 管理员可以修改所有用户的权限（需后续实现）

### 搜索体验
- 搜索框在导航栏，随处可见
- 支持模糊匹配（不必完全匹配）
- 搜索结果即时显示

### 首页体验
- 自动按分类组织商品
- 无分类的商品单独显示
- 搜索时隐藏分类直接显示结果

---

## ⚠️ 常见问题

**Q: 为什么看不到"商家中心"？**  
A: 因为你是普通用户。只有商家和管理员能看到。需要重新注册为商家账户。

**Q: 搜索没有找到想要的商品？**  
A: 检查以下几点:
- 关键词是否正确拼写
- 商品是否已上架 (is_active = True)
- 搜索会查找名称和描述

**Q: 日志文件会不会无限增大？**  
A: 不会。自动轮转规则确保单个文件最多10MB，最多保留10个备份。

**Q: 如何重置用户类型？**  
A: 目前需要修改数据库或删除用户重新注册。

---

## 🔧 开发者注意事项

### 添加新搜索字段
编辑 `app.py` 的 `/` 路由:
```python
products = products_query.filter(
    (Product.name.ilike(f'%{query}%')) | 
    (Product.description.ilike(f'%{query}%')) |
    (Product.category.name.ilike(f'%{query}%'))  # 新增
).order_by(Product.id.desc()).all()
```

### 修改日志级别
编辑 `app.py` 的日志配置:
```python
file_handler.setLevel(logging.DEBUG)  # 从 INFO 改为 DEBUG
app.logger.setLevel(logging.DEBUG)
```

### 自定义日志位置
编辑 `app.py`:
```python
if not os.path.exists('custom_logs'):  # 改为自定义路径
    os.mkdir('custom_logs')

file_handler = RotatingFileHandler('custom_logs/app.log', ...)
```

---

**最后更新**: 2026-01-09  
**文档版本**: v1.0
