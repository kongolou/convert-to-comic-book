# API 参考

本文档提供了 Convert to Comic Book (CCB) 项目的 API 快速参考。

完整的 API 文档请参考 [完整 API 文档](../api-reference.md) 或 [API.md](../API.md)。

## 模块索引

- [ccb.converter](#ccbconverter) - 核心转换模块
- [ccb.file_detector](#ccbfile_detector) - 文件类型检测模块
- [ccb.archive_handler](#ccbarchive_handler) - 压缩/解压处理模块
- [ccb.utils](#ccbutils) - 工具函数模块
- [ccb.exceptions](#ccbexceptions) - 异常类
- [ccb.cli](#ccbcli) - 命令行接口

## 快速参考

### 基本使用

```python
from pathlib import Path
from ccb.converter import ComicBookConverter

# 创建转换器
converter = ComicBookConverter()

# 转换文件夹为 CBZ
output = converter.convert(
    Path("/path/to/folder"),
    "cbz",
    remove_source=False
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

## 详细文档

完整的 API 文档包含所有类和函数的详细说明，包括：
- 参数说明
- 返回值
- 异常说明
- 使用示例

请查看 [完整 API 文档](../api-reference.md) 获取更多信息。

