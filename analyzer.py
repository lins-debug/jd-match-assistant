"""简历与 JD 匹配分析：一次 LLM 调用输出结构化 MatchReport。"""

import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

# 输出 JSON Schema（写进 prompt 约束 LLM）
SCHEMA = """{
  "match_score": 0-100 的匹配度分数,
  "risk_level": "low" 或 "medium" 或 "high",
  "matched_skills": ["简历和 JD 都有的技能"],
  "missing_skills": [
    {
      "skill": "技能名",
      "priority": "high" 或 "medium" 或 "low",
      "补课建议": "如何快速入门的一两句话"
    }
  ],
  "projects_to_build": [
    {
      "项目名称": "名称",
      "涵盖技能": ["技能列表"],
      "为什么值得做": "一句话说明对求职的价值"
    }
  ],
  "interview_risks": [
    {
      "风险点": "面试官可能追问的点",
      "应对建议": "怎么准备"
    }
  ],
  "简历改写建议": {
    "当前问题": "简历的主要不足",
    "建议突出": "应该强调什么",
    "建议淡化": "应该弱化什么"
  }
}"""


def _get_client() -> OpenAI:
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def analyze(resume: str, jd: str) -> dict:
    """分析简历和 JD 的匹配度，返回结构化报告。"""
    client = _get_client()

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            {
                "role": "system",
                "content": (
                    "你是资深技术招聘顾问。对比简历和 JD，输出 JSON 格式的匹配报告。\n\n"
                    "要求：\n"
                    "- 严格返回 JSON，不要 markdown 代码块标记\n"
                    "- missing_skills 按优先级排序（high 在前）\n"
                    "- 建议要具体可执行，不要空泛\n"
                    "- 只输出 JSON，不要任何其他文字\n\n"
                    f"输出格式：\n{SCHEMA}"
                ),
            },
            {
                "role": "user",
                "content": f"## 简历\n{resume}\n\n## JD\n{jd}",
            },
        ],
        temperature=0.3,
    )

    raw = response.choices[0].message.content.strip()
    # 清理可能的 markdown 代码块标记
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "JSON 解析失败", "raw": raw}