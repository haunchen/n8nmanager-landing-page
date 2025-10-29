#!/usr/bin/env python3
"""
Changelog Index Generator
自動掃描 markdown 文件並生成 index.json

使用方法：
  python3 scripts/generate-changelog-index.py
"""

import re
import json
from pathlib import Path


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
    # 移除 'v' 前綴
    version_str = str(version_str).lstrip('v')
    # 分割並轉換為整數
    parts = version_str.split('.')
    return tuple(int(p) if p.isdigit() else 0 for p in parts)


def process_markdown_file(filepath):
    """處理單個 markdown 文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        metadata = parse_frontmatter(content)

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
            'version': version,
            'date': date,
            'title': title,
            'file': filepath.name
        }

    except Exception as e:
        print(f"  ✗ {filepath.name}: {e}")
        return None


def main():
    print("=== Changelog Index Generator ===\n")

    # 路徑配置
    script_dir = Path(__file__).parent.parent
    changelogs_dir = script_dir / 'n8nmanager' / 'changelogs'
    output_file = changelogs_dir / 'index.json'

    # 檢查目錄
    if not changelogs_dir.exists():
        print(f"錯誤：目錄不存在 {changelogs_dir}")
        return 1

    # 掃描所有 .md 文件
    markdown_files = list(changelogs_dir.glob('*.md'))

    if not markdown_files:
        print(f"警告：在 {changelogs_dir} 中沒有找到 .md 文件")
        # 生成空的 index.json
        output_data = {'changelogs': []}
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"\n✓ 已生成空的 index.json")
        return 0

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
        print(f"  v{cl['version']} ({cl['date']})")

    # 生成 JSON
    output_data = {
        'changelogs': changelogs
    }

    # 寫入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ 已生成: {output_file}")
    print(f"✓ 總共 {len(changelogs)} 個版本")

    return 0


if __name__ == '__main__':
    exit(main())
