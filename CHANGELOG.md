# CHANGELOG

## [2.3.0] - 2026-07-14

### Added
- 新增 `-d`/`--depth` 命令行参数，用于仅处理输入目录指定深度层级的子目录或归档文件（0=输入路径本身，1=直接子目录，以此类推）
- 新增 `-c`/`--collect` 与 `-d`/`--depth` 的冲突校验，两者不可同时使用
- 创建 `scripts/pre-commit.sh` 脚本，用于在 `git commit` 前执行格式化、测试和构建

### Updated
- 更新 `README.md`、命令行文档、使用示例和测试用例以覆盖新参数
- 版本号升级到 2.3.0

## [2.2.0] - 2026-01-20
### Added
- 解决了[issues#2 Can't convert to cbr](https://github.com/26350/convert-to-comic-book/issues/2)

## [2.1.0] - 2026-01-18
### Added
- 解决了[issues#1 空文件夹被识别为有效的源](https://github.com/26350/convert-to-comic-book/issues/1)
- 修复项目文件

## [2.0.11] - 2026-01-11
### Updated
- 解决安装后`ccb`命令无法找到模块的问题

## [2.0.10] - 2026-01-11
### Updated
- 更改项目名称为`ccb-cli`

## [2.0.9] - 2026-01-11
### Updated
- 去除`cli.py`中指令帮助信息的句号
- 更新了 Google 风格的代码注释

## [2.0.8] - 2026-01-10
### Updated
- 更新`README.md`和`cli.py`中指令的帮助信息

## [2.0.7] - 2026-01-10
### Updated
- 新增`package-dir = {"" = "src"}`配置，支持src布局
- 修复Hatchling构建配置，将`packages = ["src/ccb"]`改为`sources = ["src"]`

## [2.0.0] - 2026-01-08

### Deleted
- 删除`-r`或`--recursive`参数
- 删除`--output`参数

### Added
- 新增`-R`参数，对应`--remove`参数
- 新增`-F`或`--force`参数，强制替换存在同名文件
- `-f`或`--from-type`参数新增`auto`选项，且默认值改为`auto`
- 新增`--output-dir`参数
- 更新文档与测试

### Updated
- 更改`-c`或`--collect`参数执行逻辑
- 修复使用`--remove`参数不能删除文件夹的问题
- 调整项目结构，将`ccb`目录迁移至`src`目录下，采用src布局

## [1.0.0] - 2026-01-02

### Added
- 初始版本发布
