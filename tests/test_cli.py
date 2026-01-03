"""
命令行接口模块的单元测试
"""

import pytest
from pathlib import Path
import tempfile
import os

from ccb.cli import collect_archives


class TestCLI:
    """CLI 测试类"""
    
    def test_collect_archives_with_spaces(self):
        """测试收集包含空格的路径"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建包含空格的文件夹
            test_folder = Path(tmpdir) / "test folder with spaces"
            test_folder.mkdir()
            
            # 创建测试 ZIP 文件
            zip_file = test_folder / "test.zip"
            zip_file.touch()
            
            # 测试收集
            archives = collect_archives(test_folder, recursive=False)
            assert len(archives) == 1
            assert archives[0] == zip_file
    
    def test_path_with_quotes(self):
        """测试带引号的路径处理"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建包含空格的文件夹
            test_folder = Path(tmpdir) / "test folder"
            test_folder.mkdir()
            
            # 模拟带引号的路径字符串
            path_str = f'"{test_folder}"'
            # 移除引号
            clean_path = path_str.strip('"\'')
            path = Path(clean_path)
            
            assert path.exists()
            assert path.is_dir()

