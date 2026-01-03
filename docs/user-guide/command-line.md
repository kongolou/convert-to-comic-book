# 命令行选项

## 基本语法

```
ccb [可选参数] <路径...>
```

## 位置参数

### `paths`

一个或多个文件夹或压缩包路径。

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

指定输入类型。

**可选值**: `folder`, `cbz`, `cbr`, `cb7`, `cbt`, `zip`, `rar`, `7z`, `tar`

**默认值**: 自动检测

**示例**:
```bash
ccb -f cb7 /path/to/comic.cb7
```

### `-t, --to-type`

指定输出类型。

**可选值**: `folder`, `cbz`, `cbr`, `cb7`, `cbt`

**默认值**: `cbz`

**示例**:
```bash
ccb -t cbr /path/to/folder
```

### `-o, --output`

指定输出目录。

**默认值**: 输入文件的目录

**示例**:
```bash
ccb /path/to/folder -o /path/to/output
```

### `-r, --recursive`

递归处理子文件夹。

**行为**:
- **普通模式**: 递归处理所有子文件夹
- **收集模式**: 递归搜索所有子文件夹中的压缩包

**示例**:
```bash
# 递归处理所有子文件夹
ccb -r /path/to/folders

# 递归收集压缩包
ccb -c -r /path/to/archives
```

### `-c, --collect`

收集模式：查找并转换可识别的压缩包。

在收集模式下，程序会自动查找并转换以下格式：
- `zip` → `cbz`
- `rar` → `cbr`
- `7z` → `cb7`
- `tar` → `cbt`

可以与 `-r` 组合使用以递归搜索。

**示例**:
```bash
# 收集当前目录下的压缩包
ccb -c /path/to/folder

# 递归收集所有子文件夹中的压缩包
ccb -c -r /path/to/folders
```

### `-q, --quiet`

静默模式：仅显示错误和摘要信息。

**示例**:
```bash
ccb -q /path/to/folder
```

### `--remove`

转换后删除源文件。

**警告**: 此操作不可逆，请谨慎使用！

**示例**:
```bash
ccb --remove /path/to/folder
```

### `-v, --version`

显示版本信息并退出。

**示例**:
```bash
ccb --version
```

## 组合使用

多个选项可以组合使用：

```bash
# 递归收集压缩包，转换为 CBZ，并删除源文件
ccb -c -r -t cbz --remove /path/to/archives

# 批量转换，静默模式
ccb -q -r /path/to/folders
```

## 路径处理

### Windows 路径

在 Windows PowerShell 中，包含空格的路径需要用引号包裹：

```powershell
ccb "C:\Users\Username\My Comics\comic folder"
```

### 多个路径

可以同时指定多个路径：

```bash
ccb /path/to/folder1 /path/to/folder2 /path/to/folder3
```

