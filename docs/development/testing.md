# 测试

## 运行测试

### 运行所有测试

```bash
pytest tests/
```

### 运行特定测试文件

```bash
pytest tests/test_converter.py
```

### 运行特定测试

```bash
pytest tests/test_converter.py::TestComicBookConverter::test_convert_folder_to_cbz
```

### 查看测试覆盖率

```bash
pytest --cov=ccb tests/
```

生成覆盖率报告：

```bash
pytest --cov=ccb --cov-report=html tests/
```

## 测试结构

```
tests/
├── __init__.py
├── test_file_detector.py      # 文件类型检测测试
├── test_archive_handler.py    # 压缩/解压处理测试
├── test_converter.py          # 核心转换测试
├── test_utils.py              # 工具函数测试
├── test_cli.py                # CLI 测试
├── test_cli_recursive.py      # CLI 递归处理测试
└── test_cli_combinations.py   # CLI 参数组合测试
```

## 测试覆盖

所有核心模块都有对应的单元测试：
- 文件类型检测：100% 覆盖
- 压缩/解压处理：ZIP 和 TAR 格式完整测试
- 转换逻辑：主要转换路径都有测试
- 工具函数：所有函数都有测试
- CLI 接口：基本功能和参数组合测试

## 编写新测试

### 测试文件命名

测试文件应以 `test_` 开头，例如 `test_new_feature.py`。

### 测试类命名

测试类应以 `Test` 开头，例如 `TestNewFeature`。

### 测试函数命名

测试函数应以 `test_` 开头，例如 `test_new_functionality`。

### 示例

```python
import pytest
from pathlib import Path
from ccb.converter import ComicBookConverter

class TestNewFeature:
    """新功能测试类"""
    
    def test_new_functionality(self):
        """测试新功能"""
        converter = ComicBookConverter()
        # 测试代码
        assert True
```

## 持续集成

项目使用 GitHub Actions 进行持续集成，自动运行测试。

