# 開發指南

## 目錄結構

```
n8nmanager/
├── index.html          # 首頁（Landing Page）
├── privacy.html        # 隱私權政策頁面
├── changelog.html      # 更新日誌頁面
├── css/
│   └── styles.css      # 編譯後的完整 CSS（Tailwind + 自定義樣式）
├── js/
│   ├── main.js         # 主要交互功能
│   └── changelog-loader.js  # 更新日誌載入器
├── images/             # 圖片資源
└── sitemap.xml         # 網站地圖（自動生成）

changelogs/             # 更新日誌 Markdown 檔案
├── index.json          # 自動生成的更新日誌索引
└── *.md               # 各版本更新日誌
```

## 技術實作

- 純 HTML5 + CSS3 + ES6 JavaScript
- Tailwind CSS（編譯版本）
- 原生 Intersection Observer API
- CSS transitions 和 animations
- 無框架依賴
- 響應式設計（桌面版 + 行動版）
- 完整的 SEO 優化（Meta 標籤 + Schema.org 結構化數據）

## 本地開發

### 使用 Python

```bash
cd n8nmanager
python3 -m http.server 8000
```

然後訪問：`http://localhost:8000/`

### 使用 Node.js (http-server)

```bash
npx http-server n8nmanager -p 8000
```

然後訪問：`http://localhost:8000/`

### 使用 VS Code Live Server

安裝 Live Server 擴展，右鍵點擊 `index.html` 選擇「Open with Live Server」。

## 瀏覽器兼容性

支援所有現代瀏覽器：
- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+
- iOS Safari 11+
- Chrome for Android 60+
