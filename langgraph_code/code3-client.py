import os
import sys
import asyncio
from typing import TypedDict, Literal
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
import re
import subprocess
from mcp.types import TextResourceContents

# MCP 客户端
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


# ======================
# 1. ReAct 状态
# ======================
class ReActState(TypedDict):
    math_question: str
    thought: str
    action: str
    observation: str
    final_answer: str
    now_tool: str

# ======================
# 2. LLM
# ======================
llm = ChatOpenAI(
    model="qwen3.5-flash", 
    temperature=0.2,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# ======================
# 3. MCP 客户端全局会话
# ======================
session: ClientSession | None = None
question_bank = None
answer_bank = None

async def llm_math_reason(state: ReActState) -> ReActState:
    global question_bank, answer_bank  # 声明使用全局变量
    state["now_tool"] = "llm"
    print(f"🤔 提问：{state['math_question']}")
    sys.stdout.flush()

    try:
        # ======================
        # 从 MCP 读取 题库资源
        # ======================
        if(question_bank is None or answer_bank is None):  # 缓存未初始化
            try:
                print("➡️ 正在读取知识库")
                sys.stdout.flush()
                q_res = await session.read_resource("file://math_question_bank.txt")
                a_res = await session.read_resource("file://math_answer_bank.txt")

                # 提取文本内容
                q_content = q_res.contents[0]
                a_content = a_res.contents[0]
                
                # # TextResourceContents 使用 text 字段
                question_bank = q_content.text if hasattr(q_content, 'text') else str(q_content)
                answer_bank = a_content.text if hasattr(a_content, 'text') else str(a_content)
                
            except Exception as resource_error:
                print(f"WARNING: Failed to read resources: {resource_error}", file=sys.stderr)
                # 降级方案：使用空字符串
                question_bank = ""
                answer_bank = ""

        # ======================
        # 从 MCP 获取提示词模板
        # ======================
        print("➡️ 正在获取 Prompt 模板")
        sys.stdout.flush()
        prompt_result = await session.get_prompt(
            "react_reason",
            arguments={
                "question": state["math_question"],
                "observation": state["observation"],
                "question_bank": question_bank,
                "answer_bank": answer_bank
            }
        )
        
        # 提取 Prompt 文本
        prompt_text = prompt_result.messages[0].content.text
        llm_response = llm.invoke(prompt_text).content
        
        # 解析 LLM 响应
        if "思考：" in llm_response and "；动作：" in llm_response:
            state["thought"] = llm_response.split("思考：")[1].split("；动作：")[0].strip()
            state["action"] = llm_response.split("；动作：")[1].strip()
        else:
            # 如果格式不对，强制结束
            state["thought"] = "LLM返回格式错误"
            state["action"] = "finish(无法解析答案)"
            
        state["observation"] = ""
        
    except Exception as e:
        print(f"❌ llm_math_reason 节点错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        state["thought"] = f"错误: {str(e)}"
        state["action"] = "finish(出错)"
        
    return state

# ======================
# 5. 执行节点：调用 MCP 工具 calc
# ======================
async def execute_math_action(state: ReActState) -> ReActState:
    state["now_tool"] = "action"
    current_action = state["action"]

    if session is None:
        raise RuntimeError("MCP Session 未初始化")

    if current_action.startswith("calc"):
        match = re.search(r'calc\((.*?)\)', current_action)
        math_exp = match.group(1).strip() if match else ""

        if not math_exp:
            state["observation"] = "错误：无效的数学表达式"
            return state

        try:
            # 调用 MCP 工具：calc
            result = await session.call_tool("calc", {
                "expression": math_exp
            })
            # 提取工具返回的文本
            if result.content and len(result.content) > 0:
                state["observation"] = result.structuredContent["text"]
            else:
                state["observation"] = "未得到结果"
        except Exception as e:
            state["observation"] = f"工具调用错误: {str(e)}"
            
        state["final_answer"] = ""

    elif current_action.startswith("finish"):
        match = re.search(r'finish\((.*?)\)', current_action)
        state["final_answer"] = match.group(1).strip() if match else ""

    else:
        state["observation"] = f"未知动作: {current_action}"

    return state

# ======================
# 6. 路由（完全不变）
# ======================
def math_route_loop(state: ReActState) -> Literal["llm_math_reason", END]:
    return END if state["final_answer"] else "llm_math_reason"

# ======================
# 7. 构建图
# ======================
workflow = StateGraph(ReActState)
workflow.add_node("llm_math_reason", llm_math_reason)
workflow.add_node("execute_math_action", execute_math_action)

workflow.add_edge(START, "llm_math_reason")
workflow.add_edge("llm_math_reason", "execute_math_action")
workflow.add_conditional_edges("execute_math_action", math_route_loop)

app = workflow.compile()

# ======================
# 8. 运行入口
# ======================
async def main_app():
    global session
    
    ques = {
        "math_question": "一个商店有100个苹果，第一天卖出30%，第二天卖出剩余的一半，请问还剩多少个苹果？",
        "now_tool": "",
        "thought": "",
        "action": "",
        "observation": "",
        "final_answer": ""
    }
    
    # 配置服务端启动参数
    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(current_dir, "code3-server.py")
    python_executable = sys.executable  # 获取Python解释器的绝对路径
    
    print(f"🔍 启动服务端...")

    async with stdio_client(
        StdioServerParameters(
            command=python_executable,
            args=[server_path]
        )
    ) as (read, write):
        async with ClientSession(read, write) as sess:
            print("😶‍🌫️ 请等待连接服务端...")
            try:
                # 设置更长的超时（30秒），给服务端更多启动时间
                await asyncio.wait_for(sess.initialize(), timeout=30.0)
                
                session = sess
                
                print("🤩 连接服务端成功")
                
                step_count = 0
                async for state in app.astream(ques):
                    step_count += 1
                    print(f"----- 第{step_count}轮 ReAct 迭代 -----")
                    for node_name, node_output in state.items():
                        if node_output.get("thought"):
                            print(f"🧠 思考：{node_output['thought']}")
                        if node_output.get("action"):
                            print(f"⚙️ 动作：{node_output['action']}")
                        if node_output.get("observation"):
                            print(f"📊 MCP 返回：{node_output['observation']}")
                        if node_output.get("final_answer"):
                            print(f"✅ 最终答案：{node_output['final_answer']}")
                    print()
                    
            except asyncio.TimeoutError:
                print("❌ 连接超时：服务端可能在启动时崩溃或输出混乱")
            except Exception as e:
                print(f"❌ 连接失败: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main_app())