"""
命令行接口模块
"""

import argparse
import asyncio
import logging
from pathlib import Path
from typing import List, Optional
import time

from ccb import __version__
from ccb.converter import ComicBookConverter
from ccb.file_detector import detect_file_type, get_comic_format, is_archive_file
from ccb.exceptions import ComicBookError

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """
    解析命令行参数
    
    Returns:
        解析后的参数对象
    """
    parser = argparse.ArgumentParser(
        prog="Convert to Comic Book",
        description="Convert to Comic Book - 将图片文件夹或压缩包转换为漫画书格式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 转换单个图片文件夹为 cbz
  ccb /path/to/your/folder
  
  # 批量转换文件夹为 cbr
  ccb -t cbr -r /path/to/your/folders
  
  # 转换 cb7 为 cbt 并删除源文件
  ccb -f cb7 -t cbt /path/to/comic_book.cb7 --remove
  
  # 收集并转换压缩包
  ccb -c /path/to/your/folder
  
  # 递归收集并转换为 cbz
  ccb -c -r /path/to/your/folders -t cbz
        """
    )
    
    parser.add_argument(
        "paths",
        nargs="*",
        help="一个或多个文件夹或压缩包路径（支持 cbz, cbr, cb7, cbt, zip, rar, 7z, tar）"
    )
    
    parser.add_argument(
        "-f", "--from-type",
        choices=["folder", "cbz", "cbr", "cb7", "cbt", "zip", "rar", "7z", "tar"],
        default=None,
        help="指定输入类型（默认自动检测）"
    )
    
    parser.add_argument(
        "-t", "--to-type",
        choices=["folder", "cbz", "cbr", "cb7", "cbt"],
        default="cbz",
        help="指定输出类型（默认: cbz）"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="指定输出目录（默认: 输入文件的目录）"
    )
    
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="递归处理子文件夹（在收集模式下，递归搜索所有子文件夹中的压缩包）"
    )
    
    parser.add_argument(
        "-c", "--collect",
        action="store_true",
        help="收集模式：查找并转换可识别的压缩包（可与 -r 组合使用以递归搜索）"
    )
    
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="静默模式：仅显示错误和摘要"
    )
    
    parser.add_argument(
        "--remove",
        action="store_true",
        help="转换后删除源文件"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s v{__version__}",
        # version=f"Convert to Comic Book v{__version__}"
    )
    
    return parser.parse_args()


def collect_archives(path: Path, recursive: bool = False) -> List[Path]:
    """
    收集路径下的所有压缩包文件
    
    Args:
        path: 搜索路径
        recursive: 是否递归搜索子文件夹
    
    Returns:
        压缩包文件路径列表
    """
    archives = []
    
    if not path.exists():
        logger.warning(f"Path does not exist: {path}")
        return archives
    
    if path.is_file():
        if is_archive_file(path):
            archives.append(path)
    elif path.is_dir():
        try:
            if recursive:
                # 递归搜索，Path 对象已经正确处理包含空格的路径
                for file_path in path.rglob("*"):
                    if file_path.is_file() and is_archive_file(file_path):
                        archives.append(file_path)
            else:
                # 只搜索当前目录
                for file_path in path.iterdir():
                    if file_path.is_file() and is_archive_file(file_path):
                        archives.append(file_path)
        except (PermissionError, OSError) as e:
            logger.warning(f"Error accessing directory {path}: {e}")
            return archives
    
    return archives


async def convert_single(
    converter: ComicBookConverter,
    input_path: Path,
    from_type: Optional[str],
    to_type: str,
    output_dir: Optional[Path],
    remove_source: bool,
) -> Optional[Path]:
    """
    异步转换单个文件或文件夹
    
    Args:
        converter: 转换器实例
        input_path: 输入路径
        from_type: 输入类型（如果为None则自动检测）
        to_type: 输出类型
        output_dir: 输出目录
        remove_source: 是否删除源文件
    
    Returns:
        输出路径，如果失败返回None
    """
    try:
        # 如果指定了输入类型，需要验证
        if from_type:
            detected_type = detect_file_type(input_path)
            if detected_type != from_type:
                logger.warning(
                    f"Specified type '{from_type}' does not match detected type '{detected_type}' "
                    f"for {input_path}"
                )
        
        result = await asyncio.get_event_loop().run_in_executor(
            None,
            converter.convert,
            input_path,
            to_type,
            output_dir,
            remove_source,
        )
        return result
    except Exception as e:
        logger.error(f"Failed to convert {input_path}: {e}")
        return None


def process_paths(args: argparse.Namespace) -> None:
    """
    处理路径列表
    
    Args:
        args: 命令行参数
    """
    # 配置日志
    if args.quiet:
        logging.basicConfig(level=logging.ERROR, format="%(levelname)s %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    
    if not args.paths:
        logger.error("No input paths provided")
        return
    
    converter = ComicBookConverter()
    # 处理输出目录路径，移除可能的引号
    output_dir = Path(args.output.strip('"\'')) if args.output else None
    
    # 收集要处理的路径
    paths_to_process = []
    
    if args.collect:
        # 收集模式：查找压缩包
        for path_str in args.paths:
            # 处理路径字符串，移除可能的引号（Windows PowerShell 可能会保留引号）
            path_str = path_str.strip('"\'')
            path = Path(path_str)
            
            # 检查路径是否存在
            if not path.exists():
                logger.warning(f"Path does not exist: {path}")
                continue
            
            archives = collect_archives(path, args.recursive)
            if archives:
                paths_to_process.extend(archives)
                if not args.quiet:
                    logger.info(f"Found {len(archives)} archive(s) in: {path}")
            else:
                if not args.quiet:
                    logger.info(f"No archives found in: {path}")
    else:
        # 普通模式：处理指定的路径
        for path_str in args.paths:
            # 处理路径字符串，移除可能的引号（Windows PowerShell 可能会保留引号）
            path_str = path_str.strip('"\'')
            path = Path(path_str)
            
            # 检查路径是否存在
            if not path.exists():
                logger.warning(f"Path does not exist: {path}")
                continue
            
            if path.is_dir():
                if args.recursive:
                    # 递归处理子文件夹
                    try:
                        for subdir in path.rglob("*"):
                            # Path 对象已经正确处理包含空格的路径，无需额外处理
                            if subdir.is_dir():
                                paths_to_process.append(subdir)
                        # 也处理文件
                        for file in path.rglob("*"):
                            if file.is_file() and detect_file_type(file):
                                paths_to_process.append(file)
                    except (PermissionError, OSError) as e:
                        logger.warning(f"Error accessing path {path}: {e}")
                        continue
                else:
                    paths_to_process.append(path)
            elif path.is_file():
                paths_to_process.append(path)
            else:
                logger.warning(f"Invalid path (exists but is neither file nor directory): {path}")
    
    if not paths_to_process:
        logger.warning("No valid paths to process")
        return
    
    # 处理收集模式下的格式映射
    if args.collect:
        # 在收集模式下，标准格式自动映射到对应的漫画书格式
        # 但如果指定了输出类型，使用指定的类型
        pass
    
    # 异步处理所有路径
    start_time = time.time()
    
    async def process_all():
        tasks = []
        for input_path in paths_to_process:
            # 确定输入类型
            from_type = args.from_type
            if from_type is None:
                detected = detect_file_type(input_path)
                from_type = detected
            
            # 确定输出类型
            to_type = args.to_type
            if args.collect and from_type in ["zip", "rar", "7z", "tar"]:
                # 收集模式下，标准格式自动映射到对应的漫画书格式
                # 但如果用户指定了输出类型，使用用户指定的类型
                if to_type == "cbz":  # 默认值，使用映射
                    to_type = get_comic_format(from_type)
            
            task = convert_single(
                converter,
                input_path,
                from_type,
                to_type,
                output_dir,
                args.remove,
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results
    
    try:
        results = asyncio.run(process_all())
        elapsed_time = time.time() - start_time
        
        successful = sum(1 for r in results if r is not None)
        total = len(results)
        
        if not args.quiet:
            print(f"\nDone in {elapsed_time:.2f}s")
            print(f"Processed {successful}/{total} files successfully")
        elif successful < total:
            print(f"Processed {successful}/{total} files successfully")
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error during processing: {e}")


def main() -> None:
    """主程序入口"""
    args = parse_args()
    try:
        process_paths(args)
    except ComicBookError as e:
        logger.error(f"ComicBook error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        exit(1)


if __name__ == "__main__":
    main()

