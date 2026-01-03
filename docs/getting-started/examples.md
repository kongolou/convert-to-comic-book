# 使用示例

## 示例 1: 转换单个文件夹

```bash
ccb /path/to/comic/folder
```

**输出**: `/path/to/comic/folder.cbz`

## 示例 2: 批量转换并指定格式

```bash
ccb -t cbr -r /path/to/folders
```

递归转换所有子文件夹为 CBR 格式。

## 示例 3: 收集并转换压缩包

```bash
ccb -c /path/to/archives
```

查找当前目录下的 `zip`, `rar`, `7z`, `tar` 文件并转换为对应的漫画书格式。

## 示例 4: 递归收集并统一格式

```bash
ccb -c -r /path/to/archives -t cbz
```

递归搜索所有子文件夹中的压缩包，统一转换为 CBZ 格式。

## 示例 5: 转换并删除源文件

```bash
ccb -f cb7 -t cbt /path/to/comic.cb7 --remove
```

转换 CB7 为 CBT，并删除源文件。

## 示例 6: 指定输出目录

```bash
ccb /path/to/folder -o /path/to/output
```

转换文件夹为 CBZ，输出到指定目录。

## 示例 7: 处理包含空格的路径（Windows）

在 Windows PowerShell 中，使用引号包裹路径：

```powershell
ccb "C:\Users\Username\My Comics\comic folder"
```

## 示例 8: 批量处理多个路径

```bash
ccb /path/to/folder1 /path/to/folder2 /path/to/folder3
```

同时处理多个路径。

## 示例 9: 组合使用多个选项

```bash
ccb -c -r -t cbz --remove /path/to/archives
```

递归收集所有压缩包，转换为 CBZ 格式，并删除源文件。

## 示例 10: 使用静默模式

```bash
ccb -q -r /path/to/folders
```

静默模式下仅显示错误和摘要信息。

