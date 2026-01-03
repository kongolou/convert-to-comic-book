# 架构设计

## 项目概述

Convert to Comic Book (CCB) 是一个将图片文件夹或压缩包转换为漫画书格式的工具。项目采用模块化设计，具有良好的可扩展性和可维护性。

## 模块划分

```
ccb/
├── __init__.py              # 包初始化
├── cli.py                   # 命令行接口
├── converter.py             # 核心转换逻辑
├── file_detector.py         # 文件类型检测
├── archive_handler.py       # 压缩/解压处理
├── utils.py                 # 工具函数
└── exceptions.py            # 自定义异常
```

## 核心模块说明

### file_detector.py

**职责**: 检测文件类型（folder, cbz, cbr, cb7, cbt, zip, rar, 7z, tar）

**主要函数**:
- `detect_file_type(path: Path) -> Optional[str]`: 根据文件扩展名检测类型
- `is_image_file(path: Path) -> bool`: 判断是否为图片文件
- `is_archive_file(path: Path) -> bool`: 判断是否为压缩包
- `get_comic_format(standard_format: str) -> str`: 标准格式到漫画书格式映射
- `is_valid_comic_format(format_type: str) -> bool`: 验证漫画书格式

### archive_handler.py

**职责**: 处理各种压缩格式的读写操作

**主要类**:
- `ArchiveHandler`: 抽象基类
- `ZipHandler`: 处理 ZIP/CBZ（使用标准库）
- `TarHandler`: 处理 TAR/CBT（使用标准库）
- `RarHandler`: 处理 RAR/CBR（需要 rarfile）
- `SevenZipHandler`: 处理 7Z/CB7（需要 py7zr）

**主要方法**:
- `extract(archive_path: Path, output_path: Path) -> None`: 解压
- `compress(source_path: Path, archive_path: Path) -> None`: 压缩
- `is_valid(archive_path: Path) -> bool`: 验证文件有效性

### converter.py

**职责**: 核心转换逻辑

**主要类**:
- `ComicBookConverter`: 转换器主类

**主要方法**:
- `convert(input_path: Path, output_type: str, output_dir: Optional[Path], remove_source: bool) -> Path`: 执行转换
- `convert_folder_to_archive(folder_path: Path, archive_type: str, output_path: Path) -> Path`: 文件夹转压缩包
- `convert_archive_to_folder(archive_path: Path, output_path: Path) -> Path`: 压缩包转文件夹
- `convert_archive_to_archive(input_path: Path, output_type: str, output_path: Path) -> Path`: 压缩包互转

### cli.py

**职责**: 命令行参数解析和主程序入口

**主要函数**:
- `parse_args() -> argparse.Namespace`: 解析命令行参数
- `main() -> None`: 主程序入口
- `collect_archives(path: Path, recursive: bool) -> List[Path]`: 收集压缩包
- `process_paths(args: argparse.Namespace) -> None`: 处理路径列表
- `convert_single(...) -> Optional[Path]`: 异步转换单个文件

### utils.py

**职责**: 通用工具函数

**主要函数**:
- `safe_remove(path: Path) -> None`: 安全删除文件/文件夹
- `ensure_output_dir(path: Path) -> None`: 确保输出目录存在
- `get_output_path(input_path: Path, output_type: str, output_dir: Optional[Path]) -> Path`: 生成输出路径

### exceptions.py

**职责**: 自定义异常类

**异常类**:
- `ComicBookError`: 基础异常
- `UnsupportedFormatError`: 不支持的格式
- `ArchiveError`: 压缩包处理错误
- `ConversionError`: 转换错误

## 数据流设计

### 转换流程

```
输入路径 → 类型检测 → 选择处理方式 → 执行转换 → 输出文件
```

### 转换路径

1. **文件夹 → 压缩包**: 直接压缩
2. **压缩包 → 文件夹**: 解压到目标目录
3. **压缩包 → 压缩包**: 解压到临时目录 → 重新压缩为目标格式

## 依赖管理

### 必需依赖
- Python 3.10+
- 标准库: `zipfile`, `tarfile`, `pathlib`, `argparse`, `asyncio`, `logging`

### 可选依赖（用于完整功能）
- `rarfile >= 4.0`: 处理 RAR/CBR 格式
- `py7zr >= 0.21.0`: 处理 7Z/CB7 格式

## 错误处理

- 所有文件操作使用 try-except 捕获异常
- 提供清晰的错误信息
- 支持静默模式（-q）减少输出
- 自定义异常类提供更好的错误分类

## 性能优化

- 使用异步处理提高并发性能
- 大文件处理使用流式操作
- 支持批量处理多个文件
- 临时文件自动清理

## 测试策略

### 单元测试
- 文件类型检测测试
- 压缩/解压功能测试
- 转换逻辑测试
- 工具函数测试

### 集成测试
- 端到端转换测试
- 批量处理测试
- 错误场景测试

