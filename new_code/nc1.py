from langchain.agents import create_agent
import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


## 1. 定义工具
@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


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
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)


## 4. 执行Agent
print(agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in Xian?"}]}
))