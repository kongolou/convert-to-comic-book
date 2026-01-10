# 命令行选项

## 基本语法

```
ccb [可选参数] <源列表>
```

## 位置参数

### `源列表`

叶子文件或目录。

**支持的格式**:
- 文件夹 (folder)
- 漫画书格式: CBZ, CBR, CB7, CBT
- 标准压缩格式: ZIP, RAR, 7Z, TAR

**示例**:
```bash
ccb /path/to/folder
ccb /path/to/comic.cbz /path/to/another.cbr
```

## 选项

### `-h, --help`

显示帮助信息并退出。

### `-f, --from-type`

指定源类型。

**可选值**: `auto`, `folder`, `cbz`, `cbr`, `cb7`, `cbt`, `zip`, `rar`, `7z`, `tar`

**默认值**: `auto`（自动识别除了`to-type`外所有可能的类型）

**示例**:
```bash
ccb -f cb7 /path/to/comic.cb7
```

### `-t, --to-type`

指定目标类型，将`from-type`所指定的类型转换为`to-type`。

**可选值**: `folder`, `cbz`, `cbr`, `cb7`, `cbt`

**默认值**: `cbz`

**示例**:
```bash
ccb -t cbr /path/to/folder
```

### `-o, --output-dir`

重定向导出目录。

**默认值**: 将文件导出到源文件所在目录

**示例**:
```bash
ccb /path/to/folder -o /path/to/output
```

### `-c, --collect`

搜集源列表中所有非`to-type`类型的叶子文件（或不含叶子文件的叶子目录），并作为新的源列表。

**示例**:
```bash
# 收集当前目录下的压缩包
ccb -c /path/to/folder

# 收集并转换为指定格式
ccb -c -t cbz /path/to/folders
```

### `-q, --quiet`

静默模式：仅显示错误和摘要信息。

**示例**:
```bash
ccb -q /path/to/folder
```

### `-R, --remove`

处理完成后删除源列表中的所有源！

**警告**: 此操作不可逆，请谨慎使用！

**示例**:
```bash
ccb -R /path/to/folder
```

### `-F, --force`

强制替换同名的叶子文件或目录（默认行为是覆盖）！

**示例**:
```bash
ccb -F /path/to/folder
```

### `-v, --version`

显示版本信息并退出。

**示例**:
```bash
ccb --version
```

## 带空格的路径（引号）

在 Windows PowerShell 或其他 shell 中，路径中包含空格时通常需要用引号包裹，例如:

```powershell
ccb "C:\Program Files\My Comic"
```

`ccb` 会自动处理带引号的路径——在内部会移除路径字符串的引号并正确识别目录或文件。因此你可以放心地在命令行中使用带引号的路径，CLI 的收集与处理逻辑会正确解析它们。
