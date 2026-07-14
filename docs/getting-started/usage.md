# 基本使用

## 最简单的用法

转换单个文件夹为 CBZ 格式：

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

## 指定输出目录

使用 `-o` 参数指定输出目录：

```bash
ccb /path/to/source -o /dir/to/output
```

## 指定深度处理

当传入一个目录时，使用 `-d` 参数只处理该目录下特定层级的子目录或归档文件：

```bash
# 仅处理根目录下的直接子目录/归档文件（第 1 层）
ccb /path/to/root_folder -d 1

# 仅处理根目录本身（第 0 层），与直接传入该目录效果相同
ccb /path/to/root_folder -d 0
```

注意：`-d/--depth` 与 `-c/--collect` 不能同时使用。

## 查看帮助

使用 `-h` 或 `--help` 查看完整的帮助信息：

```bash
ccb -h
```

## 下一步

查看[使用示例](examples.md)了解更多高级用法。

