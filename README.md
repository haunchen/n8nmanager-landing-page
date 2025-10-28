# n8nManager Landing Page - 純 HTML 版本

這是 n8n-management-tool-landing-page 的純 HTML + CSS + JavaScript 版本，專為部署在 `/n8nmanager/` 子目錄設計。

## 目錄結構

```
n8nmanager/
├── index.html          # 首頁（Landing Page）
├── privacy.html        # 隱私權政策頁面
├── changelog.html      # 更新日誌頁面
├── css/
│   └── styles.css      # 編譯後的完整 CSS（Tailwind + 自定義樣式）
├── js/
│   └── main.js         # 所有交互功能的 JavaScript
└── images/             # 圖片資源
    ├── icon.png
    ├── app-store-badge.webp
    └── google-play-badge.png
```

## 功能特點

### 1. 完整保留的功能
- 響應式設計（桌面版 + 行動版）
- 行動版側邊欄選單（滑動動畫）
- FAQ 展開/收合功能
- 平滑滾動（Smooth Scroll）
- Intersection Observer 滾動淡入動畫
- 完整的 SEO 優化（Meta 標籤 + Schema.org 結構化數據）
- 下載按鈕（Google Play 可點擊，App Store 顯示即將推出）

### 2. 技術實作
- 純 HTML5 + CSS3 + ES6 JavaScript
- Tailwind CSS（編譯版本）
- 原生 Intersection Observer API
- CSS transitions 和 animations
- 無框架依賴

### 3. 頁面說明

#### index.html（首頁）
包含以下區塊：
- Navigation（導航欄）
- Hero Section（英雄區）
- Features Section（6 個核心功能）
- Benefits Section（優勢說明）
- FAQ Section（5 個常見問答）
- Download Section（下載按鈕）
- Footer（頁尾）

#### privacy.html（隱私政策）
包含完整的隱私權政策內容，共 9 個主要章節。

#### changelog.html（更新日誌）
包含 v0.10.0 版本的更新內容，支援展開/收合功能。

## 部署說明

### 1. 直接部署到靜態主機
將整個 `n8nmanager` 資料夾上傳到您的網站根目錄下的 `/n8nmanager/` 位置。

例如：
```
your-website.com/
└── n8nmanager/
    ├── index.html
    ├── privacy.html
    ├── changelog.html
    ├── css/
    ├── js/
    └── images/
```

訪問網址：
- 首頁：`https://your-website.com/n8nmanager/`
- 隱私政策：`https://your-website.com/n8nmanager/privacy.html`
- 更新日誌：`https://your-website.com/n8nmanager/changelog.html`

### 2. 本地測試
使用任何靜態檔案伺服器進行本地測試：

#### 方法 1：使用 Python
```bash
cd n8nmanager
python3 -m http.server 8000
```
然後訪問：`http://localhost:8000/`

#### 方法 2：使用 Node.js (http-server)
```bash
npx http-server n8nmanager -p 8000
```
然後訪問：`http://localhost:8000/`

#### 方法 3：使用 VS Code Live Server
安裝 Live Server 擴展，右鍵點擊 `index.html` 選擇「Open with Live Server」。

### 3. 路徑說明
所有資源路徑都使用 `/n8nmanager/` 前綴：
- CSS：`/n8nmanager/css/styles.css`
- JS：`/n8nmanager/js/main.js`
- Images：`/n8nmanager/images/*`

如果您需要部署到不同的子目錄，請搜索並替換所有 `/n8nmanager/` 路徑。

## 瀏覽器兼容性

支援所有現代瀏覽器：
- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+
- iOS Safari 11+
- Chrome for Android 60+

主要使用的現代特性：
- CSS Grid 和 Flexbox
- CSS Custom Properties（CSS 變數）
- Intersection Observer API
- ES6 Arrow Functions 和 Template Literals

## 自定義說明

### 修改顏色
編輯 `css/styles.css`，搜索以下 CSS 變數：
- `--indigo-600`：主要品牌顏色
- `--purple-600`：次要品牌顏色
- `--slate-*`：灰階顏色

### 修改內容
直接編輯對應的 HTML 檔案即可。

### 添加新頁面
1. 複製 `privacy.html` 作為模板
2. 修改內容區域
3. 更新導航連結

## 性能優化

已實作的優化：
1. CSS 已壓縮（minified）
2. 使用 WebP 格式圖片（App Store badge）
3. 圖片已優化大小
4. 使用 Intersection Observer 延遲載入動畫
5. 字體使用 Google Fonts CDN

## 維護建議

1. 定期檢查所有外部連結是否有效
2. 更新 Google Play 連結（如有變動）
3. 添加新的更新日誌條目時，參考 `changelog.html` 的結構
4. 保持 Schema.org 結構化數據的更新

## 聯絡資訊

如有問題，請聯絡：
- Email：services@mail.frankchen.tw
- 部落格：https://blog.frankchen.tw/

---

轉換完成日期：2025 年 10 月 28 日
原始專案：n8n-management-tool-landing-page (Next.js 15)
