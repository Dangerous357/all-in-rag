from langchain.agents import create_agent
import os
from langchain_openai import ChatOpenAI
# from langchain_core.tools import tool

from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime


## 1. 定义工具
## 1.1 定义工具(普通函数)
@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

## 1.2 定义工具运行时上下文结构
@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str

## 1.3 定义工具(使用工具运行时)
@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "xian" if user_id == "1" else "beijing"


## 2. 配置语言模型
llm = ChatOpenAI(
	model="qwen-flash",
	temperature=0.7,
	max_tokens=1024,
	api_key=os.getenv("DASHSCOPE_API_KEY"),
	base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1")


## 3. 创建Agent
agent = create_agent(
    model=llm,
    tools=[get_weather, get_user_location],  # 将工具运行时上下文工具也加入工具列表
    system_prompt="""You are a helpful assistant, 
        if a user asks about the weather but doesn't specify a location, 
        use the get_user_location tool to find out where they are and provide the weather for that location.""",
        # 这里的system_prompt中明确告诉Agent在用户没有指定位置时要调用get_user_location工具来获取用户位置
)


## 4. 执行Agent
print(agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
    context=Context(user_id="2")  # 传入工具运行时上下文
))