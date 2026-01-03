# Convert to Comic Book (CCB) 漫画转转转

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

一个强大的命令行工具，用于将图片文件夹或压缩包转换为漫画书格式（CBZ、CBR、CB7、CBT）。

## 特性

- 🔄 **多格式支持**: 支持文件夹、CBZ、CBR、CB7、CBT、ZIP、RAR、7Z、TAR 之间的相互转换
- 🚀 **高性能**: 使用异步处理，支持批量转换
- 📦 **灵活配置**: 支持递归处理、收集模式、自定义输出等
- 🛡️ **安全可靠**: 完善的错误处理和日志记录
- 🌍 **跨平台**: 支持 Windows、Linux、macOS

## 快速开始

### 安装

推荐使用 `uv` 进行安装：

```bash
# 最小安装（仅支持 ZIP/TAR 格式）
uv tool install ccb

# 或使用标准安装
uv tool install ccb[standard]

# 完整安装（包含 RAR 和 7Z 支持）
uv tool install ccb[full]
```

**注意**: 完整安装需要以下可选依赖：
- `rarfile >= 4.0`: 用于 RAR/CBR 支持
- `py7zr >= 0.21.0`: 用于 7Z/CB7 支持

### 基本使用

```bash
# 转换单个图片文件夹为 CBZ
ccb /path/to/your/folder

# 批量转换文件夹为 CBR（递归处理所有子文件夹）
ccb -t cbr -r /path/to/your/folders

# 转换 CB7 为 CBT 并删除源文件
ccb -f cb7 -t cbt /path/to/comic_book.cb7 --remove

# 收集并转换压缩包（仅当前目录）
ccb -c /path/to/your/folder

# 递归收集并转换为 CBZ（搜索所有子文件夹）
ccb -c -r /path/to/your/folders -t cbz
```

## 支持的格式

### 输入格式
- 文件夹 (folder)
- 漫画书格式: CBZ, CBR, CB7, CBT
- 标准压缩格式: ZIP, RAR, 7Z, TAR

### 输出格式
- 文件夹 (folder)
- 漫画书格式: CBZ, CBR, CB7, CBT

### 转换关系

| 输入格式 | 可转换为 |
|---------|---------|
| `folder` | `cbz`, `cbr`, `cb7`, `cbt` |
| `cbz` | `folder`, `cbr`, `cb7`, `cbt` |
| `cbr` | `folder`, `cbz`, `cb7`, `cbt` |
| `cb7` | `folder`, `cbz`, `cbr`, `cbt` |
| `cbt` | `folder`, `cbz`, `cbr`, `cb7` |
| `zip` | `folder`, `cbz`, `cbr`, `cb7`, `cbt` |
| `rar` | `folder`, `cbz`, `cbr`, `cb7`, `cbt` |
| `7z` | `folder`, `cbz`, `cbr`, `cb7`, `cbt` |
| `tar` | `folder`, `cbz`, `cbr`, `cb7`, `cbt` |

**收集模式自动映射**:
- `zip` → `cbz`
- `rar` → `cbr`
- `7z` → `cb7`
- `tar` → `cbt`

## 命令行选项

```
ccb [可选参数] <路径...>

位置参数:
  paths                  一个或多个文件夹或压缩包路径

选项:
  -h, --help             显示帮助信息
  -f, --from-type        指定输入类型（默认自动检测）
  -t, --to-type          指定输出类型（默认: cbz）
  -o, --output           指定输出目录（默认: 输入文件的目录）
  -r, --recursive        递归处理子文件夹
  -c, --collect          收集模式：查找并转换可识别的压缩包
  -q, --quiet            静默模式：仅显示错误和摘要
  --remove               转换后删除源文件
  -v, --version          显示版本信息
```

### 参数说明

- `-f, --from-type`: 指定输入类型，可选值: `folder`, `cbz`, `cbr`, `cb7`, `cbt`, `zip`, `rar`, `7z`, `tar`
- `-t, --to-type`: 指定输出类型，可选值: `folder`, `cbz`, `cbr`, `cb7`, `cbt`（默认: `cbz`）
- `-o, --output`: 指定输出目录，如果不指定则使用输入文件的目录
- `-r, --recursive`: 递归处理子文件夹
  - 在普通模式下：递归处理所有子文件夹
  - 在收集模式下：递归搜索所有子文件夹中的压缩包
- `-c, --collect`: 收集模式，自动查找并转换可识别的压缩包
- `-q, --quiet`: 静默模式，仅显示错误和摘要信息
- `--remove`: 转换后删除源文件（请谨慎使用）

## 使用示例

### 示例 1: 转换单个文件夹

```bash
ccb /path/to/comic/folder
# 输出: /path/to/comic/folder.cbz
```

### 示例 2: 批量转换并指定格式

```bash
ccb -t cbr -r /path/to/folders
# 递归转换所有子文件夹为 CBR 格式
```

### 示例 3: 收集并转换压缩包

```bash
ccb -c /path/to/archives
# 查找当前目录下的 zip, rar, 7z, tar 文件并转换为对应的漫画书格式
```

### 示例 4: 递归收集并统一格式

```bash
ccb -c -r /path/to/archives -t cbz
# 递归搜索所有子文件夹中的压缩包，统一转换为 CBZ 格式
```

### 示例 5: 转换并删除源文件

```bash
ccb -f cb7 -t cbt /path/to/comic.cb7 --remove
# 转换 CB7 为 CBT，并删除源文件
```

### 示例 6: 指定输出目录

```bash
ccb /path/to/folder -o /path/to/output
# 转换文件夹为 CBZ，输出到指定目录
```

## 项目结构

```
convert-to-comic-book/
├── ccb/                    # 主包
│   ├── __init__.py
│   ├── cli.py            # 命令行接口
│   ├── converter.py      # 核心转换逻辑
│   ├── file_detector.py  # 文件类型检测
│   ├── archive_handler.py # 压缩/解压处理
│   ├── utils.py          # 工具函数
│   └── exceptions.py     # 自定义异常
├── tests/                 # 单元测试
├── docs/                  # 文档
├── main.py               # 主入口
└── pyproject.toml        # 项目配置
```

## 开发

### 环境要求

- Python 3.10+
- uv (推荐) 或 pip

### 安装开发依赖

```bash
# 使用 uv
uv sync --group dev

# 或使用 pip
pip install -e ".[dev]"
```

### 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试文件
pytest tests/test_converter.py

# 查看测试覆盖率
pytest --cov=ccb tests/
```

### 代码质量

```bash
# 运行 linter
ruff check ccb/

# 格式化代码
ruff format ccb/
```

## 架构设计

### 核心模块

1. **file_detector.py**: 文件类型检测
   - 检测文件类型（文件夹、压缩包等）
   - 判断是否为图片文件
   - 格式验证和映射

2. **archive_handler.py**: 压缩/解压处理
   - 抽象基类 `ArchiveHandler`
   - 具体实现: `ZipHandler`, `TarHandler`, `RarHandler`, `SevenZipHandler`
   - 支持压缩、解压、验证操作

3. **converter.py**: 核心转换逻辑
   - `ComicBookConverter` 类
   - 支持文件夹 ↔ 压缩包转换
   - 支持压缩包格式互转

4. **cli.py**: 命令行接口
   - 参数解析
   - 路径处理
   - 异步批量处理

5. **utils.py**: 工具函数
   - 安全删除文件/文件夹
   - 路径处理
   - 目录管理

### 转换流程

```
输入路径 → 类型检测 → 选择处理方式 → 执行转换 → 输出文件
```

1. **文件夹 → 压缩包**: 直接压缩
2. **压缩包 → 文件夹**: 解压到目标目录
3. **压缩包 → 压缩包**: 解压到临时目录 → 重新压缩为目标格式

## 错误处理

程序提供了完善的错误处理机制：

- **ComicBookError**: 基础异常类
- **UnsupportedFormatError**: 不支持的格式
- **ArchiveError**: 压缩包处理错误
- **ConversionError**: 转换错误

所有错误都会记录详细的日志信息，方便调试和问题排查。

## 性能优化

- ✅ 异步处理支持，提高并发性能
- ✅ 临时文件自动清理
- ✅ 流式处理大文件
- ✅ 批量处理多个文件

## 常见问题

### Q: 如何处理包含空格的路径？

A: 在 Windows PowerShell 中，使用引号包裹路径：
```powershell
ccb "C:\path with spaces\folder"
```

### Q: 如何递归处理子文件夹？

A: 使用 `-r` 参数：
```bash
ccb -r /path/to/folders
```

### Q: 收集模式如何工作？

A: 使用 `-c` 参数，程序会自动查找并转换可识别的压缩包：
```bash
ccb -c /path/to/folder
```

### Q: 如何查看详细日志？

A: 默认情况下会显示 INFO 级别的日志。使用 `-q` 参数可以静默模式运行。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目使用 [MIT License](LICENSE) 开源协议。

## 相关链接

- [完整文档](https://convert-to-comic-book.readthedocs.io/)
- [API 参考](docs/api.md)
- [设计文档](docs/design.md)
