# 命令行选项

通过 `ccb -h` 或 `ccb --help` 获取完整的帮助信息如下：
```
usage: ccb [-h] [-f {auto,folder,cbz,cbr,cb7,cbt,zip,rar,7z,tar}] [-t {folder,cbz,cbr,cb7,cbt}] [-o OUTPUT_DIR] [-c] [-d DEPTH]
           [-q] [-R] [-F] [-v]
           [paths ...]

Convert to Comic Book - Convert image folders or archives to comic book formats.

positional arguments:
  paths                 Input files or directories (supports cbz, cbr, cb7, cbt, zip, rar, 7z, tar)

options:
  -h, --help            show this help message and exit
  -f, --from-type {auto,folder,cbz,cbr,cb7,cbt,zip,rar,7z,tar}
                        Source type (default: auto)
  -t, --to-type {folder,cbz,cbr,cb7,cbt}
                        Target type (default: cbz)
  -o, --output-dir OUTPUT_DIR
                        Output directory (default: source directory)
  -c, --collect         Collect leaf sources under given paths, and use them as new input
  -d DEPTH, --depth DEPTH
                        Only process directories or archives at the specified depth level relative to each input path (0=the path itself, 1=immediate subdirectories, ...)
  -q, --quiet           Quiet mode: show only errors
  -R, --remove          Remove sources after processing (excluding already matching targets)
  -F, --force           Force replace existing targets
  -v, --version         show program's version number and exit


Examples:
  ccb /path/to/source
  # Remove the whole source when done
  ccb /path/to/source -R

  ccb -c /path/to/root_folder
  # Remove leaf sources under the root folder when done
  ccb -c /path/to/root_folder -R

  ccb -f cbz -t folder comic1.cbz comic2.zip

  ccb /path/to/source -o /dir/to/output -F

  # Convert only immediate subdirectories/archives (depth 1)
  ccb /path/to/root_folder -d 1

  # Convert the source folder itself (depth 0)
  ccb /path/to/source -d 0
```
