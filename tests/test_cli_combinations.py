"""
命令行参数组合测试
"""

import pytest
from pathlib import Path
import tempfile
import zipfile
import argparse

from ccb.cli import collect_archives, process_paths


class TestCLICombinations:
    """CLI 参数组合测试类"""
    
    def test_collect_with_recursive(self):
        """测试 -c -r 组合：递归收集压缩包"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建多层目录结构
            root = Path(tmpdir) / "root"
            root.mkdir()
            
            # 在根目录创建 ZIP
            zip1 = root / "archive1.zip"
            with zipfile.ZipFile(zip1, 'w') as zipf:
                zipf.writestr("test1.txt", "content1")
            
            # 在子目录创建 ZIP
            subdir = root / "subdir"
            subdir.mkdir()
            zip2 = subdir / "archive2.zip"
            with zipfile.ZipFile(zip2, 'w') as zipf:
                zipf.writestr("test2.txt", "content2")
            
            # 在更深层创建 ZIP
            deepdir = subdir / "deep"
            deepdir.mkdir()
            zip3 = deepdir / "archive3.zip"
            with zipfile.ZipFile(zip3, 'w') as zipf:
                zipf.writestr("test3.txt", "content3")
            
            # 测试不递归（应该只找到根目录的）
            archives_non_recursive = collect_archives(root, recursive=False)
            assert len(archives_non_recursive) == 1
            assert zip1 in archives_non_recursive
            
            # 测试递归（应该找到所有层级的）
            archives_recursive = collect_archives(root, recursive=True)
            assert len(archives_recursive) == 3
            assert zip1 in archives_recursive
            assert zip2 in archives_recursive
            assert zip3 in archives_recursive
    
    def test_collect_with_spaces_and_recursive(self):
        """测试 -c -r 组合处理包含空格的路径"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建包含空格的目录结构
            root = Path(tmpdir) / "root folder"
            root.mkdir()
            
            # 在包含空格的子目录创建 ZIP
            subdir = root / "sub folder with spaces"
            subdir.mkdir()
            zip_file = subdir / "archive file.zip"
            with zipfile.ZipFile(zip_file, 'w') as zipf:
                zipf.writestr("test.txt", "content")
            
            # 测试递归收集
            archives = collect_archives(root, recursive=True)
            assert len(archives) == 1
            assert archives[0] == zip_file

