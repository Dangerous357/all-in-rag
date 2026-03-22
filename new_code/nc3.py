from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
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
## 3.1 设置回答结构
@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    punny_response: str  # A punny response
    weather_conditions: str | None = None  # Any interesting information about the weather if available
## 3.2 创建Agent并指定回答结构
agent = create_agent(
    model=llm,
    tools=[get_weather, get_user_location],
    context_schema=Context,
    system_prompt="""You are a helpful assistant, 
        if a user asks about the weather but doesn't specify a location, 
        use the get_user_location tool to find out where they are and provide the weather for that location.""",
    response_format=ToolStrategy(ResponseFormat),  # 指定Agent的回答结构
)


## 4. 执行Agent
print(agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
    context=Context(user_id="1")
))