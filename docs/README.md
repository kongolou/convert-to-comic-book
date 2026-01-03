# 文档说明

本文档目录包含了 Convert to Comic Book 项目的完整文档。

## 文档结构

### 用户文档

- **快速开始** (`getting-started/`)
  - [安装](getting-started/installation.md)
  - [基本使用](getting-started/usage.md)
  - [使用示例](getting-started/examples.md)

- **用户指南** (`user-guide/`)
  - [命令行选项](user-guide/command-line.md)
  - [支持的格式](user-guide/formats.md)
  - [常见问题](user-guide/faq.md)

### 开发文档

- **开发文档** (`development/`)
  - [架构设计](development/architecture.md)
  - [API 参考](development/api.md)
  - [测试](development/testing.md)

- **API 文档**
  - [完整 API 文档](API.md) - 详细的 API 参考
  - [API 快速参考](api-reference.md) - API 概览

### 其他

- [贡献指南](contributing.md)

## ReadTheDocs

本项目使用 MkDocs 构建文档，并托管在 ReadTheDocs 上。

### 本地构建

安装文档依赖：

```bash
uv sync --group docs
```

构建文档：

```bash
mkdocs build
```

预览文档：

```bash
mkdocs serve
```

### 在线文档

文档在线地址：https://convert-to-comic-book.readthedocs.io/

## 文档更新

文档与代码同步更新。如果发现文档问题，请提交 Issue 或 Pull Request。
