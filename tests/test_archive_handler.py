"""
压缩/解压处理模块的单元测试
"""

import pytest
from pathlib import Path
import tempfile
import zipfile
import tarfile
import os

from ccb.archive_handler import (
    ZipHandler,
    TarHandler,
    get_handler,
    ArchiveError,
)


class TestZipHandler:
    """ZIP 处理器测试类"""
    
    def test_compress_folder(self):
        """测试压缩文件夹"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建测试文件夹和文件
            test_folder = Path(tmpdir) / "test_folder"
            test_folder.mkdir()
            (test_folder / "test.txt").write_text("test content")
            
            # 压缩
            output_zip = Path(tmpdir) / "test.zip"
            handler = ZipHandler()
            handler.compress(test_folder, output_zip)
            
            # 验证
            assert output_zip.exists()
            assert zipfile.is_zipfile(output_zip)
    
    def test_extract_zip(self):
        """测试解压 ZIP 文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建测试 ZIP 文件
            zip_path = Path(tmpdir) / "test.zip"
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                zipf.writestr("test.txt", "test content")
            
            # 解压
            output_dir = Path(tmpdir) / "extracted"
            handler = ZipHandler()
            handler.extract(zip_path, output_dir)
            
            # 验证
            assert output_dir.exists()
            assert (output_dir / "test.txt").exists()
            assert (output_dir / "test.txt").read_text() == "test content"
    
    def test_is_valid_zip(self):
        """测试 ZIP 文件验证"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建有效 ZIP
            zip_path = Path(tmpdir) / "test.zip"
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                zipf.writestr("test.txt", "content")
            
            handler = ZipHandler()
            assert handler.is_valid(zip_path) is True
            
            # 创建无效文件
            invalid_path = Path(tmpdir) / "invalid.zip"
            invalid_path.write_text("not a zip")
            assert handler.is_valid(invalid_path) is False


class TestTarHandler:
    """TAR 处理器测试类"""
    
    def test_compress_folder(self):
        """测试压缩文件夹为 TAR"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建测试文件夹
            test_folder = Path(tmpdir) / "test_folder"
            test_folder.mkdir()
            (test_folder / "test.txt").write_text("test content")
            
            # 压缩
            output_tar = Path(tmpdir) / "test.tar"
            handler = TarHandler()
            handler.compress(test_folder, output_tar)
            
            # 验证
            assert output_tar.exists()
            assert tarfile.is_tarfile(output_tar)
    
    def test_extract_tar(self):
        """测试解压 TAR 文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建测试 TAR 文件
            tar_path = Path(tmpdir) / "test.tar"
            with tarfile.open(tar_path, 'w') as tar:
                test_file = Path(tmpdir) / "test.txt"
                test_file.write_text("test content")
                tar.add(test_file, arcname="test.txt")
            
            # 解压
            output_dir = Path(tmpdir) / "extracted"
            handler = TarHandler()
            handler.extract(tar_path, output_dir)
            
            # 验证
            assert output_dir.exists()
            assert (output_dir / "test.txt").exists()
            assert (output_dir / "test.txt").read_text() == "test content"


class TestGetHandler:
    """处理器获取测试类"""
    
    def test_get_zip_handler(self):
        """测试获取 ZIP 处理器"""
        handler = get_handler("zip")
        assert isinstance(handler, ZipHandler)
        
        handler = get_handler("cbz")
        assert isinstance(handler, ZipHandler)
    
    def test_get_tar_handler(self):
        """测试获取 TAR 处理器"""
        handler = get_handler("tar")
        assert isinstance(handler, TarHandler)
        
        handler = get_handler("cbt")
        assert isinstance(handler, TarHandler)
    
    def test_get_invalid_handler(self):
        """测试获取无效处理器"""
        with pytest.raises(ArchiveError):
            get_handler("invalid")

