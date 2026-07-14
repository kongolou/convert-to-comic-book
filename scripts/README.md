# Scripts

本目录包含项目开发过程中使用的辅助脚本。

## pre-commit.sh

在 `git commit` 前执行格式化、测试和构建检查：

```bash
./scripts/pre-commit.sh
```

该脚本会依次运行：

1. `uv format` - 格式化代码
2. `uv run pytest` - 运行测试
3. `uv build` - 构建包

如果任何一步失败，脚本会立即退出并返回非零状态码。
