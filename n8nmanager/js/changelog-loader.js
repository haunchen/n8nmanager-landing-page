/**
 * Changelog Loader - 纯浏览器端实现
 * 使用 fetch + marked.js 动态加载和渲染 changelog
 */

class ChangelogLoader {
  constructor() {
    this.changelogsDir = '/n8nmanager/changelogs/';
    this.indexUrl = this.changelogsDir + 'index.json';
  }

  /**
   * 解析 Frontmatter（YAML 格式）
   * 支持简单的 key: value 格式
   */
  parseFrontmatter(content) {
    const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/;
    const match = content.match(frontmatterRegex);

    if (!match) {
      return { metadata: {}, content: content };
    }

    const [, frontmatterStr, markdownContent] = match;
    const metadata = {};

    // 逐行解析 frontmatter
    frontmatterStr.split('\n').forEach(line => {
      const colonIndex = line.indexOf(':');
      if (colonIndex > 0) {
        const key = line.substring(0, colonIndex).trim();
        const value = line.substring(colonIndex + 1).trim().replace(/['"]/g, '');
        metadata[key] = value;
      }
    });

    return { metadata, content: markdownContent.trim() };
  }

  /**
   * 加载索引文件
   */
  async loadIndex() {
    try {
      const response = await fetch(this.indexUrl);
      if (!response.ok) {
        throw new Error(`Failed to load index: ${response.status}`);
      }
      const data = await response.json();
      return data.changelogs || [];
    } catch (error) {
      console.error('Error loading changelog index:', error);
      return [];
    }
  }

  /**
   * 加载单个 markdown 文件
   */
  async loadMarkdownFile(filename) {
    try {
      const url = this.changelogsDir + filename;
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Failed to load ${filename}: ${response.status}`);
      }
      const content = await response.text();
      return this.parseFrontmatter(content);
    } catch (error) {
      console.error(`Error loading ${filename}:`, error);
      return null;
    }
  }

  /**
   * 格式化日期（2024-09-25 -> 2024年9月25日）
   */
  formatDate(dateStr) {
    const [year, month, day] = dateStr.split('-');
    return `${year}年${parseInt(month)}月${parseInt(day)}日`;
  }

  /**
   * 将 Markdown 转换为 HTML
   * 使用 marked.js（通过 CDN 加载）
   */
  async markdownToHtml(markdown) {
    // 确保 marked 已加载
    if (typeof marked === 'undefined') {
      console.error('marked.js is not loaded');
      return markdown;
    }

    // 配置 marked
    marked.setOptions({
      breaks: true,
      gfm: true
    });

    return marked.parse(markdown);
  }

  /**
   * 生成单个 changelog 的 HTML
   */
  async generateChangelogHtml(changelogData, markdownContent) {
    const html = await this.markdownToHtml(markdownContent);
    const formattedDate = this.formatDate(changelogData.date);

    return `
      <div class="rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-300 bg-white border border-slate-200">
        <!-- Accordion Header -->
        <button class="changelog-button w-full p-6 text-left transition-colors duration-200 focus:outline-none hover:bg-slate-50" aria-expanded="false">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4 flex-1">
              <h2 class="text-2xl font-bold text-indigo-600">v${changelogData.version}</h2>
              <time class="text-slate-500 text-sm font-medium">${formattedDate}</time>
            </div>
            <div class="changelog-icon flex-shrink-0 ml-4 transform transition-transform duration-300">
              <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        </button>

        <!-- Accordion Content -->
        <div class="changelog-answer overflow-hidden transition-all duration-300 ease-in-out" style="max-height: 0;">
          <div class="bg-gradient-to-r from-slate-50 to-slate-100 px-8 py-8 border-t border-slate-200">
            <div class="changelog-content space-y-6">
              ${html}
            </div>
          </div>
        </div>
      </div>
    `;
  }

  /**
   * 初始化 accordion 功能
   */
  initAccordions() {
    const changelogButtons = document.querySelectorAll('.changelog-button');

    changelogButtons.forEach((button) => {
      button.addEventListener('click', function() {
        const answer = this.nextElementSibling;
        const icon = this.querySelector('.changelog-icon');
        const isExpanded = this.getAttribute('aria-expanded') === 'true';

        // Toggle current changelog
        if (isExpanded) {
          answer.style.maxHeight = '0';
          icon.style.transform = 'rotate(0deg)';
          this.setAttribute('aria-expanded', 'false');
        } else {
          answer.style.maxHeight = answer.scrollHeight + 'px';
          icon.style.transform = 'rotate(180deg)';
          this.setAttribute('aria-expanded', 'true');
        }
      });
    });
  }

  /**
   * 主加载函数
   */
  async load() {
    const container = document.getElementById('changelog-list');
    if (!container) {
      console.error('Changelog container not found');
      return;
    }

    // 显示加载状态
    container.innerHTML = '<div class="text-center py-8 text-slate-600">正在載入更新日誌...</div>';

    try {
      // 1. 加载索引
      const changelogs = await this.loadIndex();

      if (changelogs.length === 0) {
        container.innerHTML = '<div class="text-center py-8 text-slate-600">暫無更新日誌</div>';
        return;
      }

      // 2. 加载所有 markdown 文件
      const htmlParts = [];
      for (const changelog of changelogs) {
        const result = await this.loadMarkdownFile(changelog.file);
        if (result) {
          const html = await this.generateChangelogHtml(changelog, result.content);
          htmlParts.push(html);
        }
      }

      // 3. 渲染到页面
      container.innerHTML = htmlParts.join('');

      // 4. 初始化 accordion
      this.initAccordions();

      console.log(`✓ Loaded ${changelogs.length} changelog(s)`);

    } catch (error) {
      console.error('Error loading changelogs:', error);
      container.innerHTML = '<div class="text-center py-8 text-red-600">載入失敗，請稍後重試</div>';
    }
  }
}

// 页面加载完成后自动执行
document.addEventListener('DOMContentLoaded', function() {
  const loader = new ChangelogLoader();
  loader.load();
});
