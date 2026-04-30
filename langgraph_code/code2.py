import os

from typing import TypedDict, Literal
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
import re

# ======================
# 1. ReAct专属状态
# ======================
class ReActState(TypedDict):
    math_question: str  # 用户数学应用题原题
    thought: str        # LLM自主解题思路、步骤拆解
    action: str         # LLM决定执行：计算表达式 / 结束答题
    observation: str    # 计算器返回的每一步计算结果
    final_answer: str   # 数学题最终标准答案
    now_tool: str

# ======================
# 2. 初始化LLM（仅负责逻辑推理，不负责计算）
# ======================
llm = ChatOpenAI(
    model="qwen-flash", 
    temperature=0.2,
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# ======================
# 3. 唯一核心真实工具：精准数学计算器
# ======================
def math_calculator(expression: str) -> str:
    """专门处理数学数值运算，LLM只拆逻辑，计算全靠它，杜绝口算出错"""
    try:
        expression = expression.replace("%", "/100")
        calc_result = eval(expression)
        return f"中间计算结果：{expression} = {calc_result}"
    except Exception as e:
        return f"计算表达式错误：{str(e)}，请重新拆解步骤"

# ======================
# 4. ReAct核心节点1：LLM思考推理（只拆解题步骤，不做计算）
# ======================
def llm_math_reason(state: ReActState) -> ReActState:
    state["now_tool"] = "llm"
    prompt = f"""
你是专业数学解题ReAct智能体，只做两件事：
1. 将问题分步骤、分解成数学表达式，根据上一步计算器返回结果完成下一步调用计算器：calc（数学表达式）
2. 所有分步计算全部完成后，整理答案结束答题：finish(最终完整解题答案)

你必须严格遵守规则：
只要遇到可以算数或者需要计算的步骤，必须调用计算器转换成数学表达式，绝对不能自己口算和提前进行下一步数学表达式的计算

当前数学应用题：{state['math_question']}
上一步计算器返回结果：{state['observation']}

你需要根据上一步计算器计算的内容，清楚判断当前已经算到哪一步了、接下来需要计算什么，根据用户问题判断是否计算完毕，不要循环计算。
你需要严格只返回下一步的固定格式二选一，不要多余废话，用一整行回答不能随便换行：
格式一： 思考：xxx（写清楚是否计算完毕？已经完成的步骤、当前要算哪一步、解题逻辑，但是禁止自己算下一步以及写算式的答案）；动作：calc(具体数学计算公式)
格式二： 思考：xxx（写清楚是否计算完毕？所有步骤计算完毕，汇总结果）；动作：finish(应用题最终完整答案)

例如：
用户提问：“我今年25岁，我的男朋友比我小一岁，他每个月的工资（单位：万元）是他年龄的2倍，他的工资是多少？”
你根据指定的规则会依次生成：
“思考：计算男朋友的年龄是我的年龄减一；动作：calc(25-1)”
“思考：已经得到男朋友的年龄为24，计算男朋友每个月的工资是他年龄的2倍；动作：calc(24*2)”
“思考：所有步骤计算完毕，根据计算器结果可知，他的工资是48万元/月；动作：finish(他的工资是48万元/月)”
绝对不能出现自己口算：“思考：计算男朋友的年龄是我的年龄减一，为24；动作：calc(25-1)”
"""
    # LLM自主生成解题思考+下一步动作决策
    llm_response = llm.invoke(prompt).content
    state["thought"] = llm_response.split("思考：")[1].split("；动作：")[0].strip()
    state["action"] = llm_response.split("动作：")[1].strip()
    state["observation"] = ""
    return state

# ======================
# 5. ReAct核心节点2：执行计算动作 / 结束解题
# ======================
def execute_math_action(state: ReActState) -> ReActState:
    state["now_tool"] = "anay"
    current_action = state["action"]
    # 执行数学计算动作
    if current_action.startswith("calc"):
        # 提取LLM拆解的数学表达式，交给工具计算
        match = re.search(r'calc\((.*?)\)', current_action)
        math_exp = match.group(1).strip() if match else ""
        state["observation"] = math_calculator(math_exp)
        state["final_answer"] = ""
    # 所有步骤完成，输出最终数学答案
    elif current_action.startswith("finish"):
        match = re.search(r'finish\((.*?)\)', current_action)
        state["final_answer"] = match.group(1).strip() if match else ""
    return state

# ======================
# 6. ReAct循环条件判断：没算完继续推理，算完直接结束
# ======================
def math_route_loop(state: ReActState) -> Literal["llm_math_reason", END]:
    state["now_tool"] = "route"
    return "END" if state["final_answer"] else "llm_math_reason"

# ======================
# 7. LangGraph搭建ReAct数学解题工作流
# ======================
workflow = StateGraph(ReActState)
workflow.add_node("llm_math_reason", llm_math_reason)
workflow.add_node("execute_math_action", execute_math_action)

# 固定核心流程：开始推理→执行计算→条件循环迭代解题
workflow.add_edge(START, "llm_math_reason")
workflow.add_edge("llm_math_reason", "execute_math_action")
workflow.add_conditional_edges(
    "execute_math_action", 
    math_route_loop,
    {
        "llm_math_reason": "llm_math_reason",
        "END": END
    }
    )

# 编译工作流
app = workflow.compile()

# ======================
# 运行测试：经典苹果库存数学应用题
# ======================
if __name__ == "__main__":
    question_exp = "一个商店有100个苹果，第一天卖出30%，第二天卖出剩余的一半，请问还剩多少个苹果？"
    ques = {
        "math_question": question_exp,
        "now_tool": "",
        "thought": "",
        "action": "",
        "observation": "",
        "final_answer": ""
    }

    # 开启stream流式迭代，逐节点实时输出
    for step, state in enumerate(app.stream(ques), 1):
        print(f"----- 第{step}轮ReAct迭代 -----")
        # 遍历每一轮执行的节点和对应状态
        for node_name, node_state in state.items():
            if node_state.get("math_question"):
                print(f"👩‍💻 用户原始提问：{node_state['math_question']}")
            # if node_state.get("now_tool"):
            #     print(f"👀 当前流经节点：{node_state['now_tool']}")
            if node_state.get("thought"):
                print(f"🧠 LLM推理思考：{node_state['thought']}")
            if node_state.get("action"):
                print(f"⚙️ 执行动作指令：{node_state['action']}")
            if node_state.get("observation"):
                print(f"📊 工具观测结果：{node_state['observation']}")
            if node_state.get("final_answer"):
                print(f"✅ 最终解题答案：{node_state['final_answer']}")
        print()