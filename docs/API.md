# Convert to Comic Book API 文档

## 概述

本文档描述了 Convert to Comic Book (CCB) 项目的所有公共 API 接口。

## 模块索引

- [ccb.converter](#ccbconverter) - 核心转换模块
- [ccb.file_detector](#ccbfile_detector) - 文件类型检测模块
- [ccb.archive_handler](#ccbarchive_handler) - 压缩/解压处理模块
- [ccb.utils](#ccbutils) - 工具函数模块
- [ccb.exceptions](#ccbexceptions) - 异常类
- [ccb.cli](#ccbcli) - 命令行接口

---

## ccb.converter

### ComicBookConverter

核心转换器类，负责执行各种格式之间的转换。

#### 方法

##### `__init__(self)`

初始化转换器实例。

**参数**: 无

**返回**: 无

---

##### `convert(self, input_path: Path, output_type: str, output_dir: Optional[Path] = None, remove_source: bool = False) -> Path`

执行格式转换。

**参数**:
- `input_path` (Path): 输入文件或文件夹路径
- `output_type` (str): 输出类型，可选值: `"folder"`, `"cbz"`, `"cbr"`, `"cb7"`, `"cbt"`
- `output_dir` (Optional[Path]): 输出目录，如果为 None 则使用输入文件的目录
- `remove_source` (bool): 是否在转换后删除源文件，默认为 False

**返回**: `Path` - 输出文件或文件夹路径

**异常**:
- `ConversionError`: 转换失败时抛出
- `UnsupportedFormatError`: 不支持的输出格式时抛出

**示例**:
```python
from pathlib import Path
from ccb.converter import ComicBookConverter

converter = ComicBookConverter()
output = converter.convert(
    Path("/path/to/folder"),
    "cbz",
    remove_source=False
)
```

---

##### `convert_folder_to_archive(self, folder_path: Path, archive_type: str, output_path: Path) -> Path`

将文件夹转换为压缩包。

**参数**:
- `folder_path` (Path): 文件夹路径
- `archive_type` (str): 压缩包类型，可选值: `"cbz"`, `"cbr"`, `"cb7"`, `"cbt"`
- `output_path` (Path): 输出压缩包路径

**返回**: `Path` - 输出压缩包路径

**异常**:
- `ArchiveError`: 压缩失败时抛出

---

##### `convert_archive_to_folder(self, archive_path: Path, output_path: Path) -> Path`

将压缩包转换为文件夹。

**参数**:
- `archive_path` (Path): 压缩包路径
- `output_path` (Path): 输出文件夹路径

**返回**: `Path` - 输出文件夹路径

**异常**:
- `ArchiveError`: 解压失败时抛出
- `ConversionError`: 无法检测压缩包类型时抛出

---

##### `convert_archive_to_archive(self, input_path: Path, output_type: str, output_path: Path) -> Path`

将压缩包转换为另一种压缩包格式。

**参数**:
- `input_path` (Path): 输入压缩包路径
- `output_type` (str): 输出压缩包类型，可选值: `"cbz"`, `"cbr"`, `"cb7"`, `"cbt"`
- `output_path` (Path): 输出压缩包路径

**返回**: `Path` - 输出压缩包路径

**异常**:
- `ArchiveError`: 解压或压缩失败时抛出
- `ConversionError`: 无法检测输入压缩包类型时抛出

---

## ccb.file_detector

### 函数

##### `detect_file_type(path: Path) -> Optional[str]`

检测文件或文件夹的类型。

**参数**:
- `path` (Path): 文件或文件夹路径

**返回**: `Optional[str]` - 类型字符串，可能的值:
- `"folder"`: 文件夹
- `"cbz"`, `"cbr"`, `"cb7"`, `"cbt"`: 漫画书格式
- `"zip"`, `"rar"`, `"7z"`, `"tar"`: 标准压缩格式
- `None`: 无法识别

**示例**:
```python
from pathlib import Path
from ccb.file_detector import detect_file_type

file_type = detect_file_type(Path("/path/to/file.cbz"))
# 返回: "cbz"
```

---

##### `is_image_file(path: Path) -> bool`

判断文件是否为图片文件。

**参数**:
- `path` (Path): 文件路径

**返回**: `bool` - 如果是图片文件返回 True

**支持的图片格式**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.tiff`, `.tif`, `.ico`, `.svg`, `.avif`, `.heic`

---

##### `is_archive_file(path: Path) -> bool`

判断文件是否为压缩包文件。

**参数**:
- `path` (Path): 文件路径

**返回**: `bool` - 如果是压缩包文件返回 True

---

##### `get_comic_format(standard_format: str) -> str`

将标准压缩格式转换为对应的漫画书格式。

**参数**:
- `standard_format` (str): 标准格式 (`"zip"`, `"rar"`, `"7z"`, `"tar"`)

**返回**: `str` - 对应的漫画书格式 (`"cbz"`, `"cbr"`, `"cb7"`, `"cbt"`)

**映射关系**:
- `"zip"` → `"cbz"`
- `"rar"` → `"cbr"`
- `"7z"` → `"cb7"`
- `"tar"` → `"cbt"`

---

##### `is_valid_comic_format(format_type: str) -> bool`

检查格式是否为有效的漫画书格式。

**参数**:
- `format_type` (str): 格式字符串

**返回**: `bool` - 如果是有效格式返回 True

**有效格式**: `"folder"`, `"cbz"`, `"cbr"`, `"cb7"`, `"cbt"`

---

## ccb.archive_handler

### ArchiveHandler

压缩包处理器抽象基类。所有具体的处理器都继承自此类。

#### 抽象方法

##### `extract(self, archive_path: Path, output_path: Path) -> None`

解压压缩包。

**参数**:
- `archive_path` (Path): 压缩包路径
- `output_path` (Path): 输出目录路径

**异常**:
- `ArchiveError`: 解压失败时抛出

---

##### `compress(self, source_path: Path, archive_path: Path) -> None`

压缩文件或文件夹。

**参数**:
- `source_path` (Path): 源文件或文件夹路径
- `archive_path` (Path): 输出压缩包路径

**异常**:
- `ArchiveError`: 压缩失败时抛出

---

##### `is_valid(self, archive_path: Path) -> bool`

验证压缩包是否有效。

**参数**:
- `archive_path` (Path): 压缩包路径

**返回**: `bool` - 如果有效返回 True

---

### 具体实现类

#### ZipHandler

处理 ZIP 和 CBZ 格式。

**示例**:
```python
from pathlib import Path
from ccb.archive_handler import ZipHandler

handler = ZipHandler()
handler.compress(Path("/path/to/folder"), Path("/path/to/output.cbz"))
handler.extract(Path("/path/to/file.cbz"), Path("/path/to/output"))
```

#### TarHandler

处理 TAR 和 CBT 格式。

#### RarHandler

处理 RAR 和 CBR 格式。需要安装 `rarfile` 库。

#### SevenZipHandler

处理 7Z 和 CB7 格式。需要安装 `py7zr` 库。

---

### 函数

##### `get_handler(archive_type: str) -> ArchiveHandler`

根据压缩包类型获取对应的处理器实例。

**参数**:
- `archive_type` (str): 压缩包类型，可选值: `"zip"`, `"cbz"`, `"rar"`, `"cbr"`, `"7z"`, `"cb7"`, `"tar"`, `"cbt"`

**返回**: `ArchiveHandler` - 对应的处理器实例

**异常**:
- `ArchiveError`: 不支持的压缩包类型时抛出

**示例**:
```python
from ccb.archive_handler import get_handler

handler = get_handler("cbz")
handler.compress(source, output)
```

---

## ccb.utils

### 函数

##### `safe_remove(path: Path) -> None`

安全删除文件或文件夹。

**参数**:
- `path` (Path): 要删除的路径

**异常**: 删除失败时会记录错误日志

---

##### `ensure_output_dir(path: Path) -> None`

确保输出目录存在，如果不存在则创建。

**参数**:
- `path` (Path): 输出目录路径（如果是文件路径，则使用其父目录）

---

##### `get_output_path(input_path: Path, output_type: str, output_dir: Optional[Path] = None) -> Path`

生成输出文件路径。

**参数**:
- `input_path` (Path): 输入文件路径
- `output_type` (str): 输出类型 (`"folder"`, `"cbz"`, `"cbr"`, `"cb7"`, `"cbt"`)
- `output_dir` (Optional[Path]): 输出目录，如果为 None 则使用输入文件的目录

**返回**: `Path` - 输出文件路径

**示例**:
```python
from pathlib import Path
from ccb.utils import get_output_path

output = get_output_path(
    Path("/path/to/folder"),
    "cbz",
    Path("/output/dir")
)
# 返回: Path("/output/dir/folder.cbz")
```

---

## ccb.exceptions

### ComicBookError

所有 CCB 异常的基类。

继承自: `Exception`

---

### UnsupportedFormatError

不支持的格式异常。

继承自: `ComicBookError`

---

### ArchiveError

压缩包处理错误。

继承自: `ComicBookError`

---

### ConversionError

转换错误。

继承自: `ComicBookError`

---

## ccb.cli

### 函数

##### `parse_args() -> argparse.Namespace`

解析命令行参数。

**返回**: `argparse.Namespace` - 解析后的参数对象

---

##### `main() -> None`

主程序入口。解析命令行参数并执行转换操作。

**异常**:
- `ComicBookError`: CCB 相关错误
- `Exception`: 其他未预期的错误

---

##### `collect_archives(path: Path, recursive: bool = False) -> List[Path]`

收集路径下的所有压缩包文件。

**参数**:
- `path` (Path): 搜索路径
- `recursive` (bool): 是否递归搜索子文件夹，默认为 False

**返回**: `List[Path]` - 压缩包文件路径列表

---

##### `process_paths(args: argparse.Namespace) -> None`

处理路径列表，执行转换操作。

**参数**:
- `args` (argparse.Namespace): 命令行参数对象

---

## 使用示例

### 基本转换

```python
from pathlib import Path
from ccb.converter import ComicBookConverter

converter = ComicBookConverter()

# 文件夹转 CBZ
output = converter.convert(
    Path("/path/to/folder"),
    "cbz"
)

# CBZ 转文件夹
output = converter.convert(
    Path("/path/to/comic.cbz"),
    "folder"
)

# CBZ 转 CBT
output = converter.convert(
    Path("/path/to/comic.cbz"),
    "cbt"
)
```

### 文件类型检测

```python
from pathlib import Path
from ccb.file_detector import detect_file_type, is_image_file

# 检测文件类型
file_type = detect_file_type(Path("/path/to/file.cbz"))
print(file_type)  # 输出: "cbz"

# 检查是否为图片
is_image = is_image_file(Path("/path/to/image.jpg"))
print(is_image)  # 输出: True
```

### 直接使用压缩处理器

```python
from pathlib import Path
from ccb.archive_handler import get_handler

# 获取 ZIP 处理器
handler = get_handler("cbz")

# 压缩文件夹
handler.compress(
    Path("/path/to/folder"),
    Path("/path/to/output.cbz")
)

# 解压文件
handler.extract(
    Path("/path/to/file.cbz"),
    Path("/path/to/output")
)
```

---

## 版本信息

- **当前版本**: 0.1.0
- **Python 要求**: >= 3.10

## 依赖

### 必需依赖
- Python 标准库

### 可选依赖（完整功能）
- `rarfile >= 4.0`: 用于 RAR/CBR 支持
- `py7zr >= 0.21.0`: 用于 7Z/CB7 支持

