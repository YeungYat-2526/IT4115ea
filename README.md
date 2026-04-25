# shop - Flask 電商應用

輕量級電子商務平台，以 Flask 框架實現，整合帳戶管理、商品展示、購物籃功能與評論系統。

---

## 環境需求

| 組件 | 版本要求 |
|------|--------|
| Python | 3.7+ |
| pip | 最新版 |
| 虛擬環境 | 強烈建議 |

---

## 快速設置

### 步驟 1：進入專案目錄

```bash
cd /workspaces/IT4115ea/shop
```

### 步驟 2：建立並啟用虛擬環境（首次設置）

```bash
# 建立虛擬環境
python -m venv .venv

# 啟用虛擬環境
# Linux / macOS:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

### 步驟 3：安裝所有依賴

```bash
pip install -r requirements.txt
```

**所需依賴包括：**
- Flask ≥ 2.0
- Flask-Login ≥ 0.6
- Flask-WTF ≥ 1.0
- Flask-SQLAlchemy ≥ 3.0
- Flask-Migrate ≥ 4.0
- SQLAlchemy ≥ 1.4
- WTForms ≥ 3.0
- email-validator ≥ 1.1

### 步驟 4：初始化數據庫

```bash
flask db upgrade
```

### 步驟 5：啟動應用

```bash
python app/app.py
```

應用將在 `http://localhost:8080` 上運行。在瀏覽器中打開此地址即可訪問網站。

---

## 常見問題及解決方案

### 問題 1：找不到 requirements.txt

**症狀：**
```
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
```

**解決：**
確保在正確的目錄中。專案結構為：
```
/workspaces/IT4115ea/
├── README.md
└── shop/
    ├── app.py
    ├── models.py
    ├── requirements.txt    ← 在這個目錄
    └── ...
```

正確的命令：
```bash
cd /workspaces/IT4115ea/shop
pip install -r requirements.txt
```

### 問題 2：ModuleNotFoundError（缺失 Flask-SQLAlchemy 等模組）

**症狀：**
```
ModuleNotFoundError: No module named 'flask_sqlalchemy'
```

**解決：**
重新安裝所有依賴：
```bash
pip install -r requirements.txt
```

或單獨安裝缺失的模組：
```bash
pip install Flask-SQLAlchemy Flask-Migrate
```

### 問題 3：端口 8080 已被佔用

**症狀：**
```
Address already in use
```

**查看佔用端口的進程：**
```bash
lsof -i :8080
```

輸出示例：
```
COMMAND   PID USER   FD   TYPE DEVICE SIZE NODE NAME
python   2547 user    3u  IPv4  ...      TCP *:8080
```

**終止該進程：**
```bash
kill -9 2547  # 將 2547 替換為你的 PID
```

**驗證端口已空閒：**
```bash
lsof -i :8080  # 應該無輸出
```

**或改用其他端口：**
修改 [app.py](app.py) 的最後一行：
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # 改為 5000
```

然後訪問 `http://localhost:5000`

### 問題 4：數據庫錯誤或遷移失敗

**症狀：**
```
ERROR: Could not determine a database version on this connection
```

**解決：**
重置數據庫：
```bash
# 刪除現有數據庫
rm instance/db.sqlite3

# 重新創建
flask db upgrade
```

### 問題 5：在 Dev Container 或雲端無法訪問網站

**解決：**
- 確認容器的端口對外開放
- 使用容器的外部 IP 或域名來訪問
- 檢查防火牆設置

---

##  初始化後的第一步測試

1. **訪問首頁：** `http://localhost:8080/`
2. **註冊新帳戶：** 點擊「註冊」並填寫表單
3. **登入：** 使用剛註冊的帳戶登入
4. **查看個人資料：** 點擊右上角的用戶名
5. **新增商品（僅管理員）：** 第一個註冊的用戶為管理員

---

##  專案結構

```
shop/
├── app.py                # Flask 應用主文件
├── models.py             # 數據庫模型定義
├── forms.py              # WTForms 表單定義
├── requirements.txt      # Python 依賴列表
├── templates/            # HTML 模板文件
│   ├── base.html         # 基礎模板
│   ├── index.html        # 首頁
│   ├── register.html     # 註冊頁
│   ├── login.html        # 登入頁
│   └── ...
├── static/               # 靜態文件（CSS、JS、圖片）
│   └── styles.css
├── migrations/           # 數據庫遷移文件
├── instance/             # 運行時文件（數據庫等）
│   └── db.sqlite3        # SQLite 數據庫
└── UPDATES/              # 更新日誌和文檔
```

---

## 開發模式

應用默認以調試模式運行（`debug=True`），支持自動重載。修改代碼後自動重新加載，受保護的頁面需要重新登入。

關閉調試模式（生產環境）：
```python
# 修改 app.py 的最後一行
app.run(host='0.0.0.0', port=8080, debug=False)
```

---

## 需要幫助

如遇到其他問題，請檢查：
1. 虛擬環境是否已啟用（提示符前應有 `(.venv)` 或類似標記）
2. 所有依賴是否已安裝：`pip list | grep Flask`
3. 數據庫文件是否存在：`ls -la instance/db.sqlite3`
4. 應用日誌是否有錯誤信息

---

**最後更新：2026年2月24日**