#!/usr/bin/env python3
"""
将文件中的所有引号替换为配对的中文引号 " 和 "
支持的文件类型: .tex, .txt, .md, .markdown, .rst, .org
"""

import sys
import os
import argparse

# 支持的文件扩展名
SUPPORTED_EXTENSIONS = {'.tex', '.txt', '.md', '.markdown', '.rst', '.org'}

# 使用 Unicode 码点定义所有可能的引号类型
QUOTES_TO_REPLACE = [
    '\u201C',  # " (left double quotation mark)
    '\u201D',  # " (right double quotation mark)
    '\u201E',  # „ (double low-9 quotation mark)
    '\u201F',  # ‟ (double high-reversed-9 quotation mark)
    '\u2033',  # ″ (double prime)
    '\u301D',  # 〝 (reversed double prime quotation mark)
    '\u301E',  # 〞 (double prime quotation mark)
    '\uFF02',  # ＂ (fullwidth quotation mark)
]

# 定义目标引号（使用 Unicode 码点）
LEFT_QUOTE = '\u201C'   # "
RIGHT_QUOTE = '\u201D'  # "


def replace_quotes_in_file(filepath, backup=True):
    """
    替换文件中的引号

    Args:
        filepath: 文件路径
        backup: 是否创建备份文件

    Returns:
        tuple: (成功, 消息)
    """
    # 检查文件是否存在
    if not os.path.exists(filepath):
        return False, f"错误: 文件不存在: {filepath}"

    # 检查文件扩展名
    _, ext = os.path.splitext(filepath)
    if ext.lower() not in SUPPORTED_EXTENSIONS:
        return False, f"错误: 不支持的文件类型 '{ext}'。支持的类型: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"

    # 创建备份
    if backup:
        backup_path = filepath + '.bak'
        try:
            import shutil
            shutil.copy2(filepath, backup_path)
            print(f"已创建备份文件: {backup_path}")
        except Exception as e:
            return False, f"错误: 无法创建备份文件: {e}"

    # 读取文件
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"错误: 无法读取文件: {e}"

    # 将所有类型的引号统一为 ASCII 引号
    for quote in QUOTES_TO_REPLACE:
        content = content.replace(quote, '"')

    # 统计原始引号数量
    original_quote_count = content.count('"')

    # 全局替换所有引号为配对的中文引号
    result = []
    is_opening = True
    for char in content:
        if char == '"':
            if is_opening:
                result.append(LEFT_QUOTE)
                is_opening = False
            else:
                result.append(RIGHT_QUOTE)
                is_opening = True
        else:
            result.append(char)

    content = ''.join(result)

    # 写回文件
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        return False, f"错误: 无法写入文件: {e}"

    # 验证结果
    ascii_quote_count = content.count('"')
    left_quote_count = content.count(LEFT_QUOTE)
    right_quote_count = content.count(RIGHT_QUOTE)

    message = f"""替换完成！
原始引号数量: {original_quote_count}
左引号 " 数量: {left_quote_count}
右引号 " 数量: {right_quote_count}
剩余 ASCII 引号: {ascii_quote_count}"""

    return True, message


def main():
    parser = argparse.ArgumentParser(
        description='将文件中的所有引号替换为配对的中文引号 " 和 "',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
支持的文件类型:
  {', '.join(sorted(SUPPORTED_EXTENSIONS))}

示例:
  %(prog)s file.tex                    # 替换 file.tex 中的引号（会创建备份）
  %(prog)s file.txt --no-backup        # 替换 file.txt 中的引号（不创建备份）
  %(prog)s *.tex                       # 替换所有 .tex 文件
"""
    )

    parser.add_argument('files', nargs='+', help='要处理的文件路径')
    parser.add_argument('--no-backup', action='store_true', help='不创建备份文件')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

    # 处理每个文件
    total_files = len(args.files)
    success_count = 0

    for filepath in args.files:
        print(f"\n{'='*60}")
        print(f"处理文件: {filepath}")
        print('='*60)

        success, message = replace_quotes_in_file(filepath, backup=not args.no_backup)

        if success:
            success_count += 1
            print(message)
        else:
            print(message, file=sys.stderr)

    # 总结
    print(f"\n{'='*60}")
    print(f"处理完成: {success_count}/{total_files} 个文件成功")
    print('='*60)

    # 如果有失败的文件，返回非零退出码
    sys.exit(0 if success_count == total_files else 1)


if __name__ == '__main__':
    main()
