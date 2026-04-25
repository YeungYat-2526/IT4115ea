# 模板文件指南

## 新增模板文件說明

本應用新增了3個用戶界面模板文件，提供以下功能：

### 1. profile.html - 用戶個人頁面
**路由**: `/profile`  
**方法**: GET  
**功能**:
- 顯示用戶基本信息（頭像、名稱、簡介）
- 顯示用戶角色標籤（管理員、商戶、會員）
- 顯示聯絡信息（郵箱、電話、地址）
- 顯示帳號統計數據
- 選項卡式導航：
  - 購物記錄
  - 商品管理（商戶專用）
  - 評價記錄
  - 訂單管理

**主要功能**:
- 粘性側邊欄（sticky sidebar）
- 響應式設計
- Bootstrap 5 組件

### 2. edit_profile.html - 編輯個人資料
**路由**: 
- GET `/profile/edit` - 顯示表單
- POST `/profile/edit` - 保存更改

**功能**:
- 編輯個人簡介
- 編輯電話號碼
- 編輯地址信息
- 帳號安全提示

**表單字段**:
- bio (個人簡介) - TextArea
- phone (電話號碼) - Text Input
- address (地址) - TextArea

**特色**:
- 清晰的表單分組
- 取消和保存按鍵
- 安全提示警告框

### 3. notifications.html - 訊息通知頁面
**路由**: `/notifications`  
**方法**: GET  
**功能**:
- 顯示所有訊息通知
- 過濾未讀通知
- 標記通知為已讀
- 刪除通知

**特色**:
- 通知類型顏色編碼：
  - 成功 (綠色)
  - 警告 (黃色)
  - 錯誤 (紅色)
  - 信息 (藍色)
- 未讀通知高亮顯示
- 未讀計數徽章
- 時間戳顯示
- 快速操作按鍵

## 已修改的模板文件

### base.html - 基礎模板
**主要變更**:
1. 導航欄改進：
   - 用戶名鏈接更改為 `/profile`
   - "新增商品" 按鍵移除
   - 訊息按鍵改為 `/notifications`
   - 添加未讀通知徽章

2. 頁腳新增：
   - 關於我們部分
   - 快速導航鏈接
   - 幫助與支持
   - 社交媒體鏈接
   - 版權信息

3. JavaScript 改進：
   - 自動更新通知徽章函數
   - 30秒刷新間隔

## 模板結構總覽

```
templates/
├── base.html                     (基礎模板 - 已修改)
├── profile.html                  (新增 - 用戶個人頁面)
├── edit_profile.html            (新增 - 編輯資料)
├── notifications.html           (新增 - 通知管理)
├── index.html
├── login.html
├── register.html
├── product.html
├── add_product.html
├── edit_product.html
├── merchant_dashboard.html
├── cart.html
├── messages.html
├── category_list.html
├── add_category.html
└── edit_category.html
```

## 自定義說明

### 修改個人頁面佈局

編輯 `profile.html` 的以下部分：
- 改變側邊欄寬度：修改 `<div class="col-md-4">` 的值
- 添加新的統計卡：複製 `<div class="card text-center">` 結構
- 添加新的選項卡：在 `<ul class="nav nav-tabs">` 中添加新的 `<li>`

### 修改通知樣式

編輯 `notifications.html` 的以下部分：
- 改變通知類型顏色：修改 `notification_type` 判斷中的顏色代碼
- 改變未讀徽章樣式：修改 `.list-group-item.list-group-item-light` CSS
- 添加新的通知類型：擴展 `{% if notification.notification_type %}` 判斷

### 修改頁腳內容

編輯 `base.html` 的頁腳部分：
- 改變公司信息：修改 "關於我們" 段落
- 添加新鏈接：在相應的 `<ul>` 中添加 `<li>` 項
- 修改社交媒體：改變 `<a>` 標籤的 `href`

## 使用 Bootstrap 組件

所有新模板都使用了 Bootstrap 5 的以下組件：
- Card (`card`, `card-body`, `card-header`)
- Nav Tabs (`nav-tabs`, `nav-link`)
- Badges (`badge`)
- Alerts (`alert`)
- Buttons (`btn`, `btn-primary`, `btn-outline-secondary`)
- Form Controls (`form-control`, `form-label`)
- Responsive Grid (`col-md-*`, `offset-md-*`)

## 響應式設計

所有模板都採用移動優先的響應式設計：
- 移動設備：單列佈局
- 平板設備：兩列佈局
- 桌面設備：優化的多列佈局

## 無障礙考慮

模板中包含的無障礙特性：
- 語義 HTML (`<button>`, `<nav>`, `<footer>`)
- ARIA 標籤（如適用）
- 清晰的標題層次結構
- 足夠的顏色對比度

## 常見修改

### 修改導航欄鏈接
在 `base.html` 中的 `<nav>` 區域修改 `url_for()` 調用。

### 添加新的通知類型
1. 修改 `app.py` 中的 Notification 模型
2. 在 `notifications.html` 中添加新的 `{% elif %}` 分支

### 修改個人頁面字段
1. 修改 `app.py` 中的 `edit_profile()` 路由
2. 在 `edit_profile.html` 中添加新的表單字段

---

**版本**: 1.0  
**最後更新**: 2026年1月9日
