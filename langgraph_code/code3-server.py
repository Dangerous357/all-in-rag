from mcp import Tool, Resource
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Prompt
from mcp.types import PromptMessage, TextContent, GetPromptResult
from mcp.types import TextResourceContents, ReadResourceResult, TextContent
import asyncio
import sys


# ======================================
# 1. 创建 MCP 服务
# ======================================
server = Server("math-mcp-demo")

#  1.1 工具能力：listTools + callTool
async def calc(expression: str):
    expression = expression.replace("%", "/100")
    try:
        return f"计算结果：{expression} = {eval(expression)}"
    except Exception as e:
        return f"表达式错误：{str(e)}，请重新拆解步骤"

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="calc",
            description="简单数学计算器",
            inputSchema={
                "type": "object",  # 固定为object
                "properties": {  # 定义每个参数的具体类型、描述和约束
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，例如: 100 * 0.7 / 2"
                    }
                },
                "required": ["expression"]
            }
        )
    ]



@server.call_tool()
async def call_tool(name, arguments):
    if name == "calc":
        result_text = await calc(arguments["expression"])
        return {"text": result_text}

#  1.2 资源能力：listResources + readResource
RESOURCES = {
    "math_question_bank.txt": """
应用题1：超市原有200kg大米，第一天卖出40%，第二天卖出剩下的3/4，最后还剩多少千克大米？
应用题2：班级共有45名学生，男生占总人数的60%，女生中有一半参加了文艺社团，求参加文艺社团的女生人数。
""",

    "math_answer_bank.txt": """
应用题1标准答案：
第一步：200 * 40% = 80kg
第二步：200 - 80 = 120kg
第三步：120 * 3/4 = 90kg
第四步：剩余 120 - 90 = 30kg
最终答案：还剩30千克大米

应用题2标准答案：
第一步：45 * 60% = 27人（男生）
第二步：45 - 27 = 18人（女生）
第三步：18 / 2 = 9人
最终答案：参加文艺社团的女生有9人
"""
}

@server.list_resources()
async def list_resources():
    return [
        Resource(
            uri="file://math_question_bank.txt",
            name="数学应用题题库",
            description="包含数学应用题的题库"
        ),
        Resource(
            uri="file://math_answer_bank.txt",
            name="应用题标准答案库",
            description="包含应用题的标准答案"
        )
    ]

@server.read_resource()
async def read_resource(uri: str):
    # uri 是 AnyUrl 对象，需要转换为字符串
    uri_str = str(uri)
    # 去掉 file:// 前缀和尾部斜杠，在资源库中查找原文
    resource_name = uri_str.replace("file://", "").rstrip("/")
    content_str = RESOURCES.get(resource_name, "")
    
    return content_str



#  1.3 Prompt 模板能力：listPrompts + callPrompt
PROMPTS = {
    "react_reason": """你是专业数学解题ReAct智能体，只做两件事：
1. 将问题分步骤、分解成数学表达式，根据上一步计算器返回结果完成下一步调用计算器：calc（数学表达式）
2. 所有分步计算全部完成后，整理答案结束答题：finish(最终完整解题答案)

你必须严格遵守规则：
只要遇到可以算数或者需要计算的步骤，必须调用计算器转换成数学表达式，绝对不能自己口算和提前进行下一步数学表达式的计算

当前数学应用题：{question}
上一步计算器返回结果：{observation}

你需要根据上一步计算器计算的内容，清楚判断当前已经算到哪一步了、接下来需要计算什么，根据用户问题判断是否计算完毕，不要循环计算。
你需要严格只返回下一步的固定格式二选一，不要多余废话，用一整行回答不能随便换行：
格式一： 思考：xxx（写清楚是否计算完毕？已经完成的步骤、当前要算哪一步、解题逻辑，但是禁止自己算下一步以及写算式的答案）；动作：calc(具体数学计算公式)
格式二： 思考：xxx（写清楚是否计算完毕？所有步骤计算完毕，汇总结果）；动作：finish(应用题最终完整答案)

数学题库参考（可选参考）：{question_bank}
题库对应答案参考（可选参考）：{answer_bank}
    """
}


@server.list_prompts()
async def list_prompts():
    return [
        Prompt(name="react_reason", description="ReAct思考模板")
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict):
    
    formatted_text = PROMPTS[name].format(**arguments)
    
    # 必须返回 GetPromptResult 对象
    return GetPromptResult(
        messages=[
            PromptMessage(
                role="user",  # 或者 "assistant"，视你的模板角色而定
                content=TextContent(type="text", text=formatted_text)
            )
        ]
    )

# ======================================
# 2 启动
# ======================================
async def main():
    # 使用 server.run() 方法启动 MCP 服务器
    # stdio_server() 会自动处理 stdin/stdout 的连接
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())