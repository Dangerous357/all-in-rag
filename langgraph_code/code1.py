from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class BasicState(TypedDict):
    node_input: str
    node_output: str
    node_count: int

workflow = StateGraph(BasicState)

def process_node_1(state: BasicState) -> BasicState:
    # 处理逻辑
    state["node_output"] += f"Hello, {state['node_input']}! "
    state["node_count"] += 1
    return state

def process_node_2(state: BasicState) -> BasicState:
    # 处理逻辑
    state["node_output"] += "How are you? "
    state["node_count"] += 1
    return state

def process_node_3(state: BasicState) -> BasicState:
    # 处理逻辑
    state["node_output"] += "You are so cool！ "
    state["node_count"] += 1
    return state

# 添加节点
workflow.add_node("hello", process_node_1)
workflow.add_node("greeting", process_node_2)
workflow.add_node("praise", process_node_3)

# 无条件边
workflow.add_edge(START, "hello")
workflow.add_edge("greeting", END)

# 条件路由函数
def condition_function(state: BasicState) -> str:
	text = state["node_input"].lower()
	if "dangerous" in text:
		return "praise_branch"
	return "greeting_branch"

# 条件边
workflow.add_conditional_edges(
    "hello",  # 起点
    condition_function,  # 判断条件的函数，例如：输入state，返回字符串“praise_branch”或“greeting_branch”
    {
        "praise_branch": "praise",  # 下一个节点的路线
        "greeting_branch": "greeting"
    }
)
workflow.add_edge("praise", "greeting")

app = workflow.compile()

print("=== 执行完整流程 ===")
result = app.invoke({
    	"node_input": "Bob",
    	"node_output": "",
    	"node_count": 0
	})
print(result)

# 流式执行，获取中间结果
print("\n=== 流式执行 ===")
for step in app.stream({"node_input": "Dangerous", "node_output": "", "node_count": 0}):
    print(f"Step: {step}")

print("\n=== 异步执行 ===")
import asyncio
async def async_example():
    # 异步调用
    result = await app.ainvoke({
        "node_input": "Async",
        "node_output": "",
        "node_count": 0
    })
    print(result)
# 运行异步函数
asyncio.run(async_example())

