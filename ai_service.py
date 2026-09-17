from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

REQUIREMENT_FIELDS = [
    "学科年级",
    "教材版本",
    "课题",
    "课时时长",
    "教学目标",
    "教学重点",
    "教学难点",
    "学生学情",
    "互动与风格",
]


class AIServiceError(RuntimeError):
    pass


def ai_is_configured() -> bool:
    return bool(os.getenv("DEEPSEEK_API_KEY", "").strip())


def _client() -> OpenAI:
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        raise AIServiceError("尚未填写 DeepSeek API 密钥，请先配置 .env 文件。")
    return OpenAI(
        api_key=api_key,
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").strip(),
        timeout=75.0,
        max_retries=1,
    )


def _parse_json(content: str) -> dict[str, Any]:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip(), flags=re.I)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.S)
        if not match:
            raise AIServiceError("模型返回格式异常，请再试一次。")
        try:
            value = json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            raise AIServiceError("模型返回格式异常，请再试一次。") from exc
    if not isinstance(value, dict):
        raise AIServiceError("模型没有返回有效的结构化内容。")
    return value


def _completion(messages: list[dict[str, str]], temperature: float = 0.3) -> dict[str, Any]:
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-flash").strip() or "deepseek-flash"
    try:
        response = _client().chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"},
            stream=False,
        )
        content = response.choices[0].message.content or ""
        return _parse_json(content)
    except AIServiceError:
        raise
    except Exception as exc:
        message = str(exc)
        if "401" in message or "Authentication" in message:
            raise AIServiceError("API 密钥无效，请检查 .env 中是否完整粘贴。") from exc
        if "402" in message or "balance" in message.lower():
            raise AIServiceError("DeepSeek 账户余额不足，请充值后重试。") from exc
        raise AIServiceError(f"连接 DeepSeek 失败：{message[:180]}") from exc


def interview(
    conversation: list[dict[str, str]], current_requirements: dict[str, str]
) -> tuple[str, dict[str, str], bool]:
    system_prompt = f"""
你是面向中学教师的“课研助手”，任务是通过简短访谈准确了解一节课的备课需求。
规则：
1. 每次最多追问两个最重要的问题，不要一次罗列很多问题。
2. 已经明确的信息不要重复询问；不确定的信息保留“待确认”，不得臆造。
3. 语言自然、简洁，像有经验的教研老师，不说空话。
4. 需要逐步确认这些字段：{REQUIREMENT_FIELDS}。
5. 只返回合法 JSON，不要 Markdown，格式必须是：
{{"reply":"给教师的回复", "requirements":{{"字段":"更新后的值"}}, "ready":false}}
ready 仅在课题、年级、教材版本、课时时长、学情和互动偏好基本明确时设为 true。
当前确认单：{json.dumps(current_requirements, ensure_ascii=False)}
""".strip()
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation[-12:])
    result = _completion(messages)
    reply = str(result.get("reply", "请继续补充本节课的要求。"))
    updates = result.get("requirements", {})
    merged = current_requirements.copy()
    if isinstance(updates, dict):
        for field in REQUIREMENT_FIELDS:
            value = updates.get(field)
            if value is not None and str(value).strip():
                merged[field] = str(value).strip()
    return reply, merged, bool(result.get("ready", False))


def generate_lesson_plan(
    requirements: dict[str, str], knowledge_context: list[dict[str, str]]
) -> dict[str, Any]:
    context_text = "\n\n".join(
        f"资料{index}｜{item['title']}｜{item['source']}\n{item['text']}"
        for index, item in enumerate(knowledge_context, start=1)
    )
    system_prompt = """
你是一名严谨、务实的中学教研员。请根据教师需求和提供的本地资料设计一节可执行的课。
不得把资料中没有依据的内容说成教材原文；发现信息不足时采用稳妥表述。
只返回合法 JSON，不要 Markdown。必须包含：
{
  "lesson_title":"课题",
  "summary":"设计思路，80字以内",
  "teaching_goals":["目标1","目标2","目标3"],
  "key_points":["重点"],
  "difficult_points":["难点"],
  "teaching_process":[
    {"phase":"环节", "duration":"5分钟", "teacher":"教师活动", "student":"学生活动", "purpose":"设计意图"}
  ],
  "ppt_outline":[{"page":"01", "title":"页面标题", "content":"核心内容"}],
  "interactive_activity":{"name":"活动名", "rules":"活动规则", "feedback":"评价与反馈方式"},
  "homework":{"basic":"基础任务", "advanced":"提升任务"},
  "quiz":[{"question":"题目", "options":["选项A","选项B","选项C"], "answer_index":0, "explanation":"解析"}],
  "references":["使用到的资料标题"]
}
教学过程总时长应与需求一致；PPT大纲控制在8至12页；活动必须能在普通教室实施；quiz生成3道题，answer_index从0开始。
""".strip()
    user_prompt = (
        "教师需求：\n"
        + json.dumps(requirements, ensure_ascii=False, indent=2)
        + "\n\n本地知识库检索片段：\n"
        + context_text
    )
    return _completion(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.45,
    )


def revise_lesson_plan(
    plan: dict[str, Any], requirements: dict[str, str], instruction: str
) -> dict[str, Any]:
    system_prompt = """
你是一名中学教研员。请根据教师的修改意见调整教学方案，同时保留未被要求改变的内容。
修改后必须返回完整方案，不得只返回修改片段。只返回合法 JSON，不要 Markdown。
完整方案必须保留这些字段：lesson_title、summary、teaching_goals、key_points、difficult_points、teaching_process、ppt_outline、interactive_activity、homework、quiz、references。
teaching_process 中保留 phase、duration、teacher、student、purpose；ppt_outline 中保留 page、title、content；quiz 中保留 question、options、answer_index、explanation。
检查数学表达和答案，避免前后矛盾；PPT大纲控制在8至12页。
""".strip()
    user_prompt = (
        "课程需求：\n"
        + json.dumps(requirements, ensure_ascii=False, indent=2)
        + "\n\n当前完整方案：\n"
        + json.dumps(plan, ensure_ascii=False, indent=2)
        + "\n\n教师修改意见：\n"
        + instruction.strip()
    )
    return _completion(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.35,
    )
