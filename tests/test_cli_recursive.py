"""
命令行接口递归处理测试
"""

import pytest
from pathlib import Path
import tempfile
import zipfile

from ccb.cli import collect_archives


class TestCLIRecursive:
    """CLI 递归处理测试类"""
    
    def test_collect_archives_recursive_with_spaces(self):
        """测试递归收集包含空格的子文件夹中的压缩包"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建包含空格的子文件夹
            parent_folder = Path(tmpdir) / "parent folder"
            parent_folder.mkdir()
            
            sub_folder = parent_folder / "sub folder with spaces"
            sub_folder.mkdir()
            
            # 在子文件夹中创建 ZIP 文件
            zip_file = sub_folder / "test archive.zip"
            with zipfile.ZipFile(zip_file, 'w') as zipf:
                zipf.writestr("test.txt", "test content")
            
            # 测试递归收集
            archives = collect_archives(parent_folder, recursive=True)
            assert len(archives) == 1
            assert archives[0] == zip_file
    
    def test_collect_archives_nested_spaces(self):
        """测试嵌套的包含空格的文件夹"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建多层嵌套的包含空格的文件夹
            level1 = Path(tmpdir) / "level 1"
            level1.mkdir()
            
            level2 = level1 / "level 2 with spaces"
            level2.mkdir()
            
            level3 = level2 / "level 3 folder"
            level3.mkdir()
            
            # 在最深层创建 ZIP 文件
            zip_file = level3 / "archive file.zip"
            with zipfile.ZipFile(zip_file, 'w') as zipf:
                zipf.writestr("test.txt", "test content")
            
            # 测试递归收集
            archives = collect_archives(level1, recursive=True)
            assert len(archives) == 1
            assert archives[0] == zip_file
    
    def test_collect_archives_multiple_archives_with_spaces(self):
        """测试收集多个包含空格的压缩包"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建多个包含空格的文件夹
            folder1 = Path(tmpdir) / "folder one"
            folder1.mkdir()
            
            folder2 = Path(tmpdir) / "folder two"
            folder2.mkdir()
            
            # 在每个文件夹中创建 ZIP 文件
            zip1 = folder1 / "archive one.zip"
            with zipfile.ZipFile(zip1, 'w') as zipf:
                zipf.writestr("test1.txt", "test content 1")
            
            zip2 = folder2 / "archive two.zip"
            with zipfile.ZipFile(zip2, 'w') as zipf:
                zipf.writestr("test2.txt", "test content 2")
            
            # 测试递归收集
            archives = collect_archives(Path(tmpdir), recursive=True)
            assert len(archives) == 2
            assert zip1 in archives
            assert zip2 in archives

