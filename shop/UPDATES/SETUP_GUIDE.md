# 🚀 快速設置指南

## 安裝依賴

```bash
pip install -r requirements.txt
```

## 數據庫遷移

應用新功能後，需要運行以下命令更新數據庫：

```bash
# 升級數據庫到最新版本
flask db upgrade
```

如果出現問題，可以重置數據庫：

```bash
# 刪除現有數據庫
rm instance/db.sqlite3

# 重新創建數據庫
flask db upgrade
```

## 啟動應用

```bash
# 設定環境變數（可選）
export FLASK_ENV=development
export SECRET_KEY=your-secret-key

# 啟動應用
python app.py
```

應用將在 `http://localhost:8080` 上運行。

## 測試新功能

### 1. 註冊新帳戶
- 導航到 `http://localhost:8080/register`
- 填寫表單並提交
- 應用應能成功創建新用戶

### 2. 查看個人頁面
- 登錄後，點擊導航欄中的用戶名
- 進入 `/profile` 頁面

### 3. 編輯個人資料
- 在個人頁面點擊 "編輯個人資料"
- 進入 `/profile/edit` 頁面
- 修改並保存信息

### 4. 查看通知
- 點擊導航欄的 "訊息" 按鍵
- 進入 `/notifications` 頁面

## 調試

### 查看應用日誌
```bash
# 啟用詳細模式
FLASK_ENV=development python app.py
```

### 數據庫檢查
```bash
python -c "
from app import create_app
from models import db, User, Notification

app = create_app()
with app.app_context():
    print('Users:', User.query.count())
    print('Notifications:', Notification.query.count())
"
```

## 常見問題

### 頁面返回404
- 確保所有路由都在 `app.py` 中定義
- 檢查模板文件是否存在於 `templates/` 目錄

### 數據庫錯誤
- 運行 `flask db upgrade` 更新數據庫
- 檢查遷移文件是否正確

### 靜態文件未加載
- 確保 `static/` 目錄存在
- 檢查CSS文件路徑是否正確

## 更多信息

詳見 `CHANGES_2026_01_09.md` 了解所有更改內容。
