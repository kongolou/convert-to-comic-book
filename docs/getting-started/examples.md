# 使用示例

假设一位 Linux 用户的 Home 目录下具有如下结构：
```
~
├──awesome one.cbr
└──comic_books/
   ├──comic_book1.zip
   ├──comic_book2/
   └──comic_book3/
      ├──chapter1.7z
      ├──chapter2.cbt
      └──chapter3/
```
## 示例 1: 将 comic_book1.zip 文件夹转换为 comic_book1.cbz

```bash
ccb ~/comic_books/comic_book1.zip
```

输出文件: 
- `~/comic_books/comic_book1.cbz`

## 示例 2: 将 comic_book2 文件夹转换为 comic_book2.cbz

```bash
ccb ~/comic_books/comic_book2
```

输出文件: 
- `~/comic_books/comic_book2.cbz`

## 示例 3: 批量转换 chapter1.7z、chapter2.cbt chapter3 文件夹到 cbt 格式

```bash
ccb -t cbt \
    ~/comic_books/comic_book3/chapter1.7z \
    ~/comic_books/comic_book3/chapter2.cbt \
    ~/comic_books/comic_book3/chapter3
```

输出文件: 
- `~/comic_books/comic_book3/chapter1.cbt`
- `~/comic_books/comic_book3/chapter3.cbt`

注意到 chapter2.cbt 不发生转换

## 示例 4: 批量转换 chapter1.7z、chapter2.cbt chapter3 文件夹到 comic_books 下后删除

```bash
ccb ~/comic_books/comic_book3/chapter1.7z \
    ~/comic_books/comic_book3/chapter2.cbt \
    ~/comic_books/comic_book3/chapter3 \
    -o ~/comic_books \
    -R
```
执行后目录：
```
~
├──awesome one.cbr
└──comic_books/
   ├─*chapter1.cbz
   ├─*chapter2.cbz
   ├─*chapter3.cbz
   ├──comic_book1.zip
   ├──comic_book2/
   └──comic_book3/
      └──.
```

## 示例 5：批量转换 comic_books 下的源后删除，静默输出

```bash
ccb -c ~/comic_books -q -R
```
执行后目录：
```
~
├──awesome one.cbr
└──comic_books/
   ├─*comic_book1.cbz
   ├─*comic_book2.cbz
   └──comic_book3/
      ├─*chapter1.cbz
      ├─*chapter2.cbz
      └─*chapter3.cbz
```
可以看到，使用 `-c` 参数后，命令变简洁了，实际上，上述命令等价于
```
ccb ~/comic_books/comic_book1.zip \
    ~/comic_books/comic_book2 \
    ~/comic_books/comic_book3/chapter1.7z \
    ~/comic_books/comic_book3/chapter2.cbt \
    ~/comic_books/comic_book3/chapter3 \
    -q -R
```

## 示例 6: 处理包含空格的路径 

使用引号包裹即可：

```bash
ccb "~/awesome one.cbr"
```
输出文件: 
- ~/awesome one.cbz
