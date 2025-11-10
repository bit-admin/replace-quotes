# replace-quotes
将 .tex, .txt, .md 文件中的所有引号替换为配对的中文引号。

```bash
# 查看帮助
python3 replace_quotes.py --help

# 处理单个文件（会自动创建 .bak 备份）
python3 replace_quotes.py chapters/1_chapter1.tex

# 处理单个文件，不创建备份
python3 replace_quotes.py chapters/2_chapter2.tex --no-backup

# 处理多个文件
python3 replace_quotes.py file1.tex file2.txt file3.md

# 处理所有 .tex 文件
python3 replace_quotes.py chapters/*.tex
```
