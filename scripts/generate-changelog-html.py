#!/usr/bin/env python3
"""
Changelog HTML Generator
自動從 markdown 文件生成完整的 changelog HTML 頁面

使用方法：
  python3 scripts/generate-changelog-html.py
"""

import re
import markdown
from pathlib import Path


def parse_frontmatter(content):
    """解析 YAML frontmatter"""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return {}, content

    frontmatter_str = match.group(1)
    markdown_content = match.group(2)
    metadata = {}

    for line in frontmatter_str.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip().replace('"', '').replace("'", '')

    return metadata, markdown_content.strip()


def parse_version(version_str):
    """解析版本號為可比較的元組"""
    version_str = str(version_str).lstrip('v')
    parts = version_str.split('.')
    return tuple(int(p) if p.isdigit() else 0 for p in parts)


def format_date(date_str):
    """格式化日期（2024-09-25 -> 2024年9月25日）"""
    year, month, day = date_str.split('-')
    return f"{year}年{int(month)}月{int(day)}日"


def markdown_to_html(md_content):
    """將 Markdown 轉換為 HTML"""
    md = markdown.Markdown(extensions=['extra', 'nl2br'])
    return md.convert(md_content)


def generate_changelog_item_html(metadata, content, is_first=False):
    """生成單個 changelog 項目的 HTML"""
    version = metadata.get('version', '')
    date = metadata.get('date', '')
    title = metadata.get('title', f'v{version}')

    formatted_date = format_date(date)
    html_content = markdown_to_html(content)

    # 第一個項目預設展開
    aria_expanded = 'true' if is_first else 'false'
    max_height_style = '' if is_first else ' style="max-height: 0;"'
    icon_rotation = ' style="transform: rotate(180deg);"' if is_first else ''

    return f'''      <div class="rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-300 bg-white border border-slate-200">
        <!-- Accordion Header -->
        <button class="changelog-button w-full p-6 text-left transition-colors duration-200 focus:outline-none hover:bg-slate-50" aria-expanded="{aria_expanded}">
          <div class="flex items-center justify-between">
            <div class="flex flex-col gap-5 flex-1">
              <div class="flex items-center gap-2">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-700">
                  v{version}
                </span>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-600">
                  {formatted_date}
                </span>
              </div>
              <h2 class="text-2xl font-bold text-slate-800">{title}</h2>
            </div>
            <div class="changelog-icon flex-shrink-0 ml-4 transform transition-transform duration-300"{icon_rotation}>
              <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        </button>

        <!-- Accordion Content -->
        <div class="changelog-answer overflow-hidden transition-all duration-300 ease-in-out"{max_height_style}>
          <div class="bg-gradient-to-r from-slate-50 to-slate-100 px-8 py-8 border-t border-slate-200">
            <div class="changelog-content space-y-6">
              {html_content}
            </div>
          </div>
        </div>
      </div>
'''


def process_markdown_file(filepath):
    """處理單個 markdown 文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        metadata, md_content = parse_frontmatter(content)

        if not metadata:
            print(f"  ⚠ {filepath.name}: 沒有找到 frontmatter")
            return None

        version = metadata.get('version', '')
        date = metadata.get('date', '')
        title = metadata.get('title', '')

        if not version or not date or not title:
            print(f"  ⚠ {filepath.name}: 缺少 version、date 或 title")
            return None

        return {
            'metadata': metadata,
            'content': md_content,
            'version': version,
            'file': filepath.name
        }

    except Exception as e:
        print(f"  ✗ {filepath.name}: {e}")
        return None


def main():
    print("=== Changelog HTML Generator ===\n")

    # 路徑配置
    script_dir = Path(__file__).parent.parent
    changelogs_dir = script_dir / 'n8nmanager' / 'changelogs'
    template_file = script_dir / 'templates' / 'changelog.template.html'
    output_file = script_dir / 'n8nmanager' / 'changelog.html'

    # 檢查目錄和模板
    if not changelogs_dir.exists():
        print(f"錯誤：目錄不存在 {changelogs_dir}")
        return 1

    if not template_file.exists():
        print(f"錯誤：模板文件不存在 {template_file}")
        return 1

    # 掃描所有 .md 文件
    markdown_files = list(changelogs_dir.glob('*.md'))

    if not markdown_files:
        print(f"警告：在 {changelogs_dir} 中沒有找到 .md 文件")
        return 1

    print(f"找到 {len(markdown_files)} 個 markdown 文件\n")

    # 處理所有文件
    changelogs = []
    for filepath in markdown_files:
        result = process_markdown_file(filepath)
        if result:
            changelogs.append(result)
            print(f"  ✓ {filepath.name} (v{result['version']})")

    if not changelogs:
        print("\n錯誤：沒有成功解析任何文件")
        return 1

    # 按版本號排序（從新到舊）
    changelogs.sort(key=lambda x: parse_version(x['version']), reverse=True)

    print(f"\n版本排序：")
    for cl in changelogs:
        print(f"  v{cl['version']}")

    # 生成 HTML 內容
    print(f"\n生成 HTML 內容...")
    html_items = []
    for i, cl in enumerate(changelogs):
        is_first = (i == 0)
        html = generate_changelog_item_html(cl['metadata'], cl['content'], is_first)
        html_items.append(html)

    changelogs_html = '\n'.join(html_items)

    # 讀取模板
    print(f"讀取模板: {template_file}")
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()

    # 注入內容
    if '{{CHANGELOGS_CONTENT}}' not in template:
        print("錯誤：模板中找不到 {{CHANGELOGS_CONTENT}} 佔位符")
        return 1

    final_html = template.replace('{{CHANGELOGS_CONTENT}}', changelogs_html)

    # 寫入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"\n✓ 已生成: {output_file}")
    print(f"✓ 總共 {len(changelogs)} 個版本")
    print(f"✓ 第一個版本（v{changelogs[0]['version']}）已設為預設展開")

    return 0


if __name__ == '__main__':
    exit(main())
