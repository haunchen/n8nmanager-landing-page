#!/usr/bin/env python3
"""
Sitemap Updater
自動更新 sitemap.xml 中 changelog.html 的最後修改日期

使用方法：
  python3 scripts/update-sitemap.py
"""

import re
from pathlib import Path
from xml.etree import ElementTree as ET


def parse_frontmatter(content):
    """解析 YAML frontmatter"""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return {}

    frontmatter_str = match.group(1)
    metadata = {}

    for line in frontmatter_str.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip().replace('"', '').replace("'", '')

    return metadata


def parse_version(version_str):
    """解析版本號為可比較的元組"""
    version_str = str(version_str).lstrip('v')
    parts = version_str.split('.')
    return tuple(int(p) if p.isdigit() else 0 for p in parts)


def get_latest_changelog_date(changelogs_dir):
    """從 markdown 檔案獲取最新的 changelog 日期"""
    try:
        markdown_files = list(changelogs_dir.glob('*.md'))

        if not markdown_files:
            print("  ⚠ 沒有找到任何 markdown 檔案")
            return None

        changelogs = []
        for filepath in markdown_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            metadata = parse_frontmatter(content)
            if metadata and 'version' in metadata and 'date' in metadata:
                changelogs.append({
                    'version': metadata['version'],
                    'date': metadata['date']
                })

        if not changelogs:
            print("  ⚠ 沒有找到有效的 changelog")
            return None

        # 按版本排序（從新到舊）
        changelogs.sort(key=lambda x: parse_version(x['version']), reverse=True)

        # 取第一個（最新的）
        latest = changelogs[0]
        return latest['date']

    except Exception as e:
        print(f"  ✗ 讀取 changelog 失敗: {e}")
        return None


def update_sitemap(sitemap_file, changelog_date):
    """更新 sitemap.xml 中 changelog.html 的 lastmod"""
    try:
        # 註冊命名空間
        ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')

        # 解析 XML
        tree = ET.parse(sitemap_file)
        root = tree.getroot()

        # 命名空間
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # 查找包含 changelog.html 的 <url> 元素
        changelog_updated = False
        for url in root.findall('sm:url', ns):
            loc = url.find('sm:loc', ns)
            if loc is not None and 'changelog.html' in loc.text:
                lastmod = url.find('sm:lastmod', ns)
                if lastmod is not None:
                    old_date = lastmod.text
                    lastmod.text = changelog_date
                    changelog_updated = True
                    print(f"  ✓ changelog.html: {old_date} → {changelog_date}")
                break

        if not changelog_updated:
            print("  ⚠ 未找到 changelog.html 的 URL")
            return False

        # 寫回文件
        tree.write(sitemap_file, encoding='utf-8', xml_declaration=True)

        return True

    except Exception as e:
        print(f"  ✗ 更新 sitemap.xml 失敗: {e}")
        return False


def main():
    print("=== Sitemap Updater ===\n")

    # 路徑配置
    script_dir = Path(__file__).parent.parent
    changelogs_dir = script_dir / 'n8nmanager' / 'changelogs'
    sitemap_file = script_dir / 'n8nmanager' / 'sitemap.xml'

    # 檢查文件
    if not changelogs_dir.exists():
        print(f"錯誤：目錄不存在 {changelogs_dir}")
        return 1

    if not sitemap_file.exists():
        print(f"錯誤：文件不存在 {sitemap_file}")
        return 1

    # 1. 獲取最新 changelog 日期
    print("1. 讀取最新 changelog 日期...")
    changelog_date = get_latest_changelog_date(changelogs_dir)

    if not changelog_date:
        print("\n✗ 無法獲取 changelog 日期")
        return 1

    print(f"  最新 changelog 日期: {changelog_date}")

    # 2. 更新 sitemap.xml
    print("\n2. 更新 sitemap.xml...")
    success = update_sitemap(sitemap_file, changelog_date)

    if success:
        print(f"\n✓ sitemap.xml 已更新")
        return 0
    else:
        print(f"\n✗ 更新失敗")
        return 1


if __name__ == '__main__':
    exit(main())
