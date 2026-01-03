# 基本使用

## 最简单的用法

转换单个图片文件夹为 CBZ 格式：

```bash
ccb /path/to/your/folder
```

输出文件将保存在同一目录下：`/path/to/your/folder.cbz`

## 指定输出格式

使用 `-t` 参数指定输出格式：

```bash
# 转换为 CBR
ccb -t cbr /path/to/your/folder

# 转换为 CB7
ccb -t cb7 /path/to/your/folder

# 转换为 CBT
ccb -t cbt /path/to/your/folder
```

## 批量转换

使用 `-r` 参数递归处理所有子文件夹：

```bash
ccb -r /path/to/your/folders
```

这将递归处理指定目录下的所有子文件夹。

## 收集模式

使用 `-c` 参数启用收集模式，自动查找并转换压缩包：

```bash
# 收集当前目录下的压缩包
ccb -c /path/to/your/folder

# 递归收集所有子文件夹中的压缩包
ccb -c -r /path/to/your/folders
```

收集模式会自动将标准压缩格式转换为对应的漫画书格式：
- `zip` → `cbz`
- `rar` → `cbr`
- `7z` → `cb7`
- `tar` → `cbt`

## 指定输出目录

使用 `-o` 参数指定输出目录：

```bash
ccb /path/to/folder -o /path/to/output
```

## 删除源文件

使用 `--remove` 参数在转换后删除源文件（请谨慎使用）：

```bash
ccb -f cb7 -t cbt /path/to/comic.cb7 --remove
```

## 静默模式

使用 `-q` 参数启用静默模式，仅显示错误和摘要：

```bash
ccb -q /path/to/folder
```

## 查看帮助

使用 `-h` 或 `--help` 查看完整的帮助信息：

```bash
ccb -h
```

## 下一步

查看[使用示例](examples.md)了解更多高级用法。

