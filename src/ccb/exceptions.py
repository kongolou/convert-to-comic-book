"""
自定义异常类
"""


class ComicBookError(Exception):
    """基础异常类"""

    pass


class UnsupportedFormatError(ComicBookError):
    """不支持的格式异常"""

    pass


class ArchiveError(ComicBookError):
    """压缩包处理错误"""

    pass


class ConversionError(ComicBookError):
    """转换错误"""

    pass
