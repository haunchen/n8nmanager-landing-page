#!/usr/bin/env python3
"""
Sitemap Updater - Homepage
自動更新 sitemap.xml 中主頁面的最後修改日期

使用方法：
  python3 scripts/update-sitemap-homepage.py
"""

from pathlib import Path
from datetime import datetime
from xml.etree import ElementTree as ET


def get_current_date():
    """獲取當前日期 (YYYY-MM-DD 格式)"""
    return datetime.now().strftime('%Y-%m-%d')


def update_sitemap(sitemap_file, homepage_date):
    """更新 sitemap.xml 中主頁面的 lastmod"""
    try:
        # 註冊命名空間
        ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')

        # 解析 XML
        tree = ET.parse(sitemap_file)
        root = tree.getroot()

        # 命名空間
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # 查找主頁面的 <url> 元素
        homepage_updated = False
        for url in root.findall('sm:url', ns):
            loc = url.find('sm:loc', ns)
            if loc is not None and loc.text.endswith('/n8nmanager'):
                lastmod = url.find('sm:lastmod', ns)
                if lastmod is not None:
                    old_date = lastmod.text
                    lastmod.text = homepage_date
                    homepage_updated = True
                    print(f"  ✓ 主頁面: {old_date} → {homepage_date}")
                break

        if not homepage_updated:
            print("  ⚠ 未找到主頁面的 URL")
            return False

        # 寫回文件
        tree.write(sitemap_file, encoding='utf-8', xml_declaration=True)

        return True

    except Exception as e:
        print(f"  ✗ 更新 sitemap.xml 失敗: {e}")
        return False


def main():
    print("=== Sitemap Updater - Homepage ===\n")

    # 路徑配置
    script_dir = Path(__file__).parent.parent
    sitemap_file = script_dir / 'n8nmanager' / 'sitemap.xml'

    # 檢查文件
    if not sitemap_file.exists():
        print(f"錯誤：文件不存在 {sitemap_file}")
        return 1

    # 1. 獲取當前日期
    current_date = get_current_date()
    print(f"1. 當前日期: {current_date}")

    # 2. 更新 sitemap.xml
    print("\n2. 更新 sitemap.xml...")
    success = update_sitemap(sitemap_file, current_date)

    if success:
        print(f"\n✓ sitemap.xml 已更新")
        return 0
    else:
        print(f"\n✗ 更新失敗")
        return 1


if __name__ == '__main__':
    exit(main())
