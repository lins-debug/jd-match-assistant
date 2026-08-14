# 简历与 JD 匹配助手

输入简历和 JD，DeepSeek 自动分析匹配度，输出缺口技能、补课项目建议、面试风险点和简历优化建议。

## 功能

- **匹配分析**：0-100 分匹配度 + risk_level 风险定级
- **缺口技能**：按 high/medium/low 优先级列出，附具体补课建议
- **项目补强**：推荐可做的项目及其对求职的价值
- **面试风险**：预判面试官可能追问的点 + 应对策略
- **简历优化**：指出当前问题，建议突出什么、淡化什么
- **多 JD 对比**：前端预置 3 份 JD 模板，一键切换对比

## 技术栈

| 组件 | 技术 |
|---|---|
| LLM | DeepSeek V4 Flash（OpenAI 兼容） |
| 输出格式 | 结构化 JSON（prompt 内置 schema） |
| 后端 | FastAPI |
| 前端 | 原生 HTML/CSS/JS |

## 设计决策

- **结构化输出**：JSON schema 写进 system prompt，约束 LLM 输出格式
- **为什么不用 LangChain 解析器**：直接 prompt 约束 + json.loads 更可控，减少依赖
- **temperature=0.3**：比 SQL 生成高，匹配建议需要一定创造性但不能过高导致 JSON 格式乱

## 快速开始

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 API Key

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python -m uvicorn server:app --host 127.0.0.1 --port 8002
```

打开 http://127.0.0.1:8002，粘贴简历和 JD 进行分析。

## Docker 部署

```bash
docker build -t jd-match-assistant .
docker run -p 8002:8002 jd-match-assistant
```

## 评测指标

| 指标 | 说明 |
|---|---|
| JSON 合法率 | LLM 输出是否可成功 parse |
| 字段完整率 | 7 个顶层字段是否都有值 |
| 同 JD 输出稳定性 | 多次调用结果的一致性 |
| 建议可执行度 | 建议是否具体、可操作 |

## 项目结构

```
├── analyzer.py         # 核心：prompt 拼装 + JSON 解析
├── server.py           # FastAPI /match 接口
├── static/index.html   # 前端（含 3 份 JD 模板）
└── jds/                # JD 文件存放目录
```
