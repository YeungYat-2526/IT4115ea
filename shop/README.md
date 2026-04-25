# 如何啟動本專案網站

1. 安裝依賴：
```bash
pip install -r requirements.txt
```

2. 啟動網站（預設端口 8080）：
```bash
python app.py
```

3. 在瀏覽器打開：
```
http://localhost:8080
```

## 常見端口問題

- 如果 8080 端口被佔用，可以改用 5000 或其他端口：
  
	修改 `app.py` 最後一行：
	```python
	app.run(host='0.0.0.0', port=5000, debug=True)
	```
	然後用 `http://localhost:5000` 訪問。

- 若在 dev container 或雲端環境，請確認端口已對外開放。

---
如仍有端口無法啟動，請提供錯誤訊息協助排查。
# Micro Shopping Website (Flask)

這是一個可繼續擴充的微型購物網站雛形，使用 Flask、SQLite 與 SQLAlchemy 實作。包含：

- 帳號系統（註冊 / 登入 / 登出）
- 商品列表與詳細頁
- 留言評分系統（Review with rating 1-5）

快速啟動

1. 建議建立虛擬環境並啟用：

```bash
python -m venv .venv
source .venv/bin/activate
```

2. 安裝依賴：

```bash
pip install -r requirements.txt
```

3. 啟動應用：

```bash
python app.py
```

4. 開啟瀏覽器並前往 http://127.0.0.1:5000

預設行為與延伸建議

- 第一個註冊的使用者會被標示為管理者（可新增商品）。
- 資料庫使用 SQLite（db.sqlite3），啟動時若不存在會自動建立。
- 可延伸：上傳商品圖片、分頁、API（REST/GraphQL）、管理介面、測試。
# FYP







python app.py 行個db  行咗先用到個web site 
git add .
git commit -m "fix db and add tables"
git push origin main --force !!!!!!
flask db upgrade
如果佢話8080被佔用就入
lsof -i :8080
跟着將 -->python  2547 user <-- 嘅數字抄低
入 kill -9 （數字）
跟住入 lsof -i :8080
見到冇嘢出就可以重新行個DB