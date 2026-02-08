# actions/ai-inference 配置说明

## 概述
`actions/ai-inference` 是 GitHub 官方提供的 AI 推理 Action，用于在 GitHub Actions 中直接调用各种大语言模型。

## 使用方式

### 1. 在 GitHub Actions Workflow 中使用

参考 `.github/workflows/analyze-article.yml` 文件中的配置：

```yaml
- name: 调用 AI 分析文章
  uses: actions/ai-inference@v1
  with:
    model: deepseek/deepseek-r1:latest
    prompt: |
      你的提示词内容...
    api-key: ${{ secrets.DEEPSEEK_API_KEY }}
```

### 2. 需要配置的环境变量

在 GitHub 仓库的 Settings -> Secrets and variables -> Actions 中添加：

- `DEEPSEEK_API_KEY`: DeepSeek API 密钥

## 支持的模型

- DeepSeek 系列：`deepseek/deepseek-r1:latest`, `deepseek/deepseek-chat:latest`
- 其他模型请参考官方文档：https://github.com/actions/ai-inference

## 注意事项

1. 确保 API Key 有足够的配额
2. 注意 Prompt 的格式，要求输出纯 JSON
3. 输出内容会被后续脚本处理，需严格按照指定格式

## 参考资料

- [官方文档](https://github.com/actions/ai-inference)
- [DeepSeek API 文档](https://platform.deepseek.com/)
