# CHANGELOG

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
