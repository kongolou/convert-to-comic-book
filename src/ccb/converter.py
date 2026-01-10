"""
核心转换模块
"""

import shutil
from pathlib import Path
from typing import Optional
import logging
import tempfile

from .file_detector import detect_file_type, get_comic_format, is_valid_comic_format
from .archive_handler import get_handler
from .utils import get_output_path, safe_remove
from .exceptions import ConversionError, UnsupportedFormatError

logger = logging.getLogger(__name__)


class ComicBookConverter:
    """漫画书格式转换器"""
    
    def __init__(self):
        """初始化转换器"""
        self.temp_dirs = []  # 跟踪临时目录，用于清理
    
    def convert(
        self,
        input_path: Path,
        output_type: str,
        output_dir: Optional[Path] = None,
        remove_source: bool = False,
        force: bool = False,
    ) -> Path:
        """
        执行转换
        
        Args:
            input_path: 输入文件或文件夹路径
            output_type: 输出类型 (folder, cbz, cbr, cb7, cbt)
            output_dir: 输出目录，如果为None则使用输入文件的目录
            remove_source: 是否删除源文件
            force: 是否强制替换同名的输出文件或目录
        
        Returns:
            输出文件路径
        """
        if not input_path.exists():
            raise ConversionError(f"Input path does not exist: {input_path}")
        
        if not is_valid_comic_format(output_type):
            raise UnsupportedFormatError(f"Unsupported output format: {output_type}")
        
        input_type = detect_file_type(input_path)
        if input_type is None:
            raise ConversionError(f"Cannot detect input file type: {input_path}")
        
        logger.info(f"Converting {input_path} ({input_type}) to {output_type}")
        
        # 如果输入和输出类型相同，直接返回
        if input_type == output_type:
            logger.info(f"Input and output types are the same, skipping conversion")
            return input_path
        
        # 生成输出路径
        output_path = get_output_path(input_path, output_type, output_dir)
        
        # 检查输出路径是否存在
        if output_path.exists():
            if force:
                logger.info(f"Force replacing existing output: {output_path}")
                safe_remove(output_path)
            else:
                # 默认行为是覆盖，所以这里不需要做任何操作
                logger.info(f"Output already exists, will overwrite: {output_path}")
        
        try:
            # 根据转换类型选择处理方法
            if input_type == "folder" and output_type != "folder":
                # 文件夹 -> 压缩包
                result = self.convert_folder_to_archive(input_path, output_type, output_path)
            elif input_type != "folder" and output_type == "folder":
                # 压缩包 -> 文件夹
                result = self.convert_archive_to_folder(input_path, output_path)
            elif input_type != "folder" and output_type != "folder":
                # 压缩包 -> 压缩包
                result = self.convert_archive_to_archive(input_path, output_type, output_path)
            else:
                # folder -> folder (不应该发生)
                result = input_path
            
            # 删除源文件
            if remove_source and result != input_path:
                safe_remove(input_path)
                logger.info(f"Removed source file: {input_path}")
            
            logger.info(f"Conversion completed: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            raise ConversionError(f"Failed to convert {input_path}: {e}")
        finally:
            # 清理临时目录
            self._cleanup_temp_dirs()
    
    def convert_folder_to_archive(
        self,
        folder_path: Path,
        archive_type: str,
        output_path: Path,
    ) -> Path:
        """
        将文件夹转换为压缩包
        
        Args:
            folder_path: 文件夹路径
            archive_type: 压缩包类型 (cbz, cbr, cb7, cbt)
            output_path: 输出压缩包路径
        
        Returns:
            输出压缩包路径
        """
        handler = get_handler(archive_type)
        handler.compress(folder_path, output_path)
        return output_path
    
    def convert_archive_to_folder(
        self,
        archive_path: Path,
        output_path: Path,
    ) -> Path:
        """
        将压缩包转换为文件夹
        
        Args:
            archive_path: 压缩包路径
            output_path: 输出文件夹路径
        
        Returns:
            输出文件夹路径
        """
        archive_type = detect_file_type(archive_path)
        if archive_type is None:
            raise ConversionError(f"Cannot detect archive type: {archive_path}")
        
        handler = get_handler(archive_type)
        handler.extract(archive_path, output_path)
        return output_path
    
    def convert_archive_to_archive(
        self,
        input_path: Path,
        output_type: str,
        output_path: Path,
    ) -> Path:
        """
        将压缩包转换为另一种压缩包格式
        
        Args:
            input_path: 输入压缩包路径
            output_type: 输出压缩包类型 (cbz, cbr, cb7, cbt)
            output_path: 输出压缩包路径
        
        Returns:
            输出压缩包路径
        """
        # 创建临时目录
        temp_dir = tempfile.mkdtemp(prefix="ccb_")
        self.temp_dirs.append(temp_dir)
        temp_path = Path(temp_dir)
        
        try:
            # 先解压到临时目录
            input_type = detect_file_type(input_path)
            if input_type is None:
                raise ConversionError(f"Cannot detect input archive type: {input_path}")
            
            input_handler = get_handler(input_type)
            input_handler.extract(input_path, temp_path)
            
            # 再压缩为目标格式
            output_handler = get_handler(output_type)
            output_handler.compress(temp_path, output_path)
            
            return output_path
        except Exception as e:
            logger.error(f"Archive to archive conversion failed: {e}")
            raise
    
    def _cleanup_temp_dirs(self) -> None:
        """清理临时目录"""
        for temp_dir in self.temp_dirs:
            try:
                shutil.rmtree(temp_dir)
                logger.debug(f"Cleaned up temp directory: {temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temp directory {temp_dir}: {e}")
        self.temp_dirs.clear()

