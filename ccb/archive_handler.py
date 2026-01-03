"""
压缩/解压处理模块
"""

import zipfile
import tarfile
import shutil
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional
import logging
import tempfile

from ccb.exceptions import ArchiveError

logger = logging.getLogger(__name__)


class ArchiveHandler(ABC):
    """压缩包处理器抽象基类"""
    
    @abstractmethod
    def extract(self, archive_path: Path, output_path: Path) -> None:
        """
        解压压缩包
        
        Args:
            archive_path: 压缩包路径
            output_path: 输出目录路径
        """
        pass
    
    @abstractmethod
    def compress(self, source_path: Path, archive_path: Path) -> None:
        """
        压缩文件或文件夹
        
        Args:
            source_path: 源文件或文件夹路径
            archive_path: 输出压缩包路径
        """
        pass
    
    @abstractmethod
    def is_valid(self, archive_path: Path) -> bool:
        """
        验证压缩包是否有效
        
        Args:
            archive_path: 压缩包路径
        
        Returns:
            如果有效返回True
        """
        pass


class ZipHandler(ArchiveHandler):
    """ZIP/CBZ 处理器"""
    
    def extract(self, archive_path: Path, output_path: Path) -> None:
        """解压 ZIP/CBZ 文件"""
        try:
            output_path.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                zipf.extractall(output_path)
            logger.debug(f"Extracted {archive_path} to {output_path}")
        except Exception as e:
            raise ArchiveError(f"Failed to extract ZIP archive {archive_path}: {e}")
    
    def compress(self, source_path: Path, archive_path: Path) -> None:
        """压缩为 ZIP/CBZ 文件"""
        try:
            # 确保输出目录存在
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            # 如果输出文件已存在，先删除（Windows 上可能需要）
            if archive_path.exists():
                archive_path.unlink()
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if source_path.is_file():
                    zipf.write(source_path, source_path.name)
                elif source_path.is_dir():
                    for file_path in source_path.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(source_path)
                            zipf.write(file_path, arcname)
            logger.debug(f"Compressed {source_path} to {archive_path}")
        except Exception as e:
            raise ArchiveError(f"Failed to create ZIP archive {archive_path}: {e}")
    
    def is_valid(self, archive_path: Path) -> bool:
        """验证 ZIP/CBZ 文件是否有效"""
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                zipf.testzip()
            return True
        except Exception:
            return False


class TarHandler(ArchiveHandler):
    """TAR/CBT 处理器"""
    
    def extract(self, archive_path: Path, output_path: Path) -> None:
        """解压 TAR/CBT 文件"""
        try:
            output_path.mkdir(parents=True, exist_ok=True)
            with tarfile.open(archive_path, 'r:*') as tar:
                tar.extractall(output_path)
            logger.debug(f"Extracted {archive_path} to {output_path}")
        except Exception as e:
            raise ArchiveError(f"Failed to extract TAR archive {archive_path}: {e}")
    
    def compress(self, source_path: Path, archive_path: Path) -> None:
        """压缩为 TAR/CBT 文件"""
        try:
            # 确保输出目录存在
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            # 如果输出文件已存在，先删除（Windows 上可能需要）
            if archive_path.exists():
                archive_path.unlink()
            with tarfile.open(archive_path, 'w') as tar:
                if source_path.is_file():
                    tar.add(source_path, arcname=source_path.name)
                elif source_path.is_dir():
                    tar.add(source_path, arcname=source_path.name, recursive=True)
            logger.debug(f"Compressed {source_path} to {archive_path}")
        except Exception as e:
            raise ArchiveError(f"Failed to create TAR archive {archive_path}: {e}")
    
    def is_valid(self, archive_path: Path) -> bool:
        """验证 TAR/CBT 文件是否有效"""
        try:
            with tarfile.open(archive_path, 'r:*') as tar:
                tar.getmembers()
            return True
        except Exception:
            return False


class RarHandler(ArchiveHandler):
    """RAR/CBR 处理器（需要 rarfile 库）"""
    
    def __init__(self):
        self._has_rarfile = False
        try:
            import rarfile
            self.rarfile = rarfile
            self._has_rarfile = True
        except ImportError:
            logger.warning("rarfile not installed, RAR/CBR support unavailable")
    
    def extract(self, archive_path: Path, output_path: Path) -> None:
        """解压 RAR/CBR 文件"""
        if not self._has_rarfile:
            raise ArchiveError("rarfile library is required for RAR/CBR support")
        try:
            output_path.mkdir(parents=True, exist_ok=True)
            with self.rarfile.RarFile(archive_path) as rar:
                rar.extractall(output_path)
            logger.debug(f"Extracted {archive_path} to {output_path}")
        except Exception as e:
            raise ArchiveError(f"Failed to extract RAR archive {archive_path}: {e}")
    
    def compress(self, source_path: Path, archive_path: Path) -> None:
        """压缩为 RAR/CBR 文件"""
        # RAR 格式通常需要外部工具，这里使用临时 ZIP 然后重命名
        # 或者提示用户需要安装 WinRAR/7-Zip
        raise ArchiveError("RAR compression requires external tools. Use ZIP/CBZ instead.")
    
    def is_valid(self, archive_path: Path) -> bool:
        """验证 RAR/CBR 文件是否有效"""
        if not self._has_rarfile:
            return False
        try:
            with self.rarfile.RarFile(archive_path) as rar:
                rar.testrar()
            return True
        except Exception:
            return False


class SevenZipHandler(ArchiveHandler):
    """7Z/CB7 处理器（需要 py7zr 库）"""
    
    def __init__(self):
        self._has_py7zr = False
        try:
            import py7zr
            self.py7zr = py7zr
            self._has_py7zr = True
        except ImportError:
            logger.warning("py7zr not installed, 7Z/CB7 support unavailable")
    
    def extract(self, archive_path: Path, output_path: Path) -> None:
        """解压 7Z/CB7 文件"""
        if not self._has_py7zr:
            raise ArchiveError("py7zr library is required for 7Z/CB7 support")
        try:
            output_path.mkdir(parents=True, exist_ok=True)
            with self.py7zr.SevenZipFile(archive_path, mode='r') as archive:
                archive.extractall(output_path)
            logger.debug(f"Extracted {archive_path} to {output_path}")
        except Exception as e:
            raise ArchiveError(f"Failed to extract 7Z archive {archive_path}: {e}")
    
    def compress(self, source_path: Path, archive_path: Path) -> None:
        """压缩为 7Z/CB7 文件"""
        if not self._has_py7zr:
            raise ArchiveError("py7zr library is required for 7Z/CB7 support")
        try:
            # 确保输出目录存在
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            # 如果输出文件已存在，先删除（Windows 上可能需要）
            if archive_path.exists():
                archive_path.unlink()
            with self.py7zr.SevenZipFile(archive_path, mode='w') as archive:
                if source_path.is_file():
                    archive.write(source_path, source_path.name)
                elif source_path.is_dir():
                    for file_path in source_path.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(source_path)
                            archive.write(file_path, arcname)
            logger.debug(f"Compressed {source_path} to {archive_path}")
        except Exception as e:
            raise ArchiveError(f"Failed to create 7Z archive {archive_path}: {e}")
    
    def is_valid(self, archive_path: Path) -> bool:
        """验证 7Z/CB7 文件是否有效"""
        if not self._has_py7zr:
            return False
        try:
            with self.py7zr.SevenZipFile(archive_path, mode='r') as archive:
                archive.getnames()
            return True
        except Exception:
            return False


def get_handler(archive_type: str) -> ArchiveHandler:
    """
    根据压缩包类型获取对应的处理器
    
    Args:
        archive_type: 压缩包类型 (cbz, cbr, cb7, cbt, zip, rar, 7z, tar)
    
    Returns:
        对应的处理器实例
    """
    handler_map = {
        "zip": ZipHandler,
        "cbz": ZipHandler,
        "rar": RarHandler,
        "cbr": RarHandler,
        "7z": SevenZipHandler,
        "cb7": SevenZipHandler,
        "tar": TarHandler,
        "cbt": TarHandler,
    }
    
    handler_class = handler_map.get(archive_type.lower())
    if handler_class is None:
        raise ArchiveError(f"Unsupported archive type: {archive_type}")
    
    return handler_class()



