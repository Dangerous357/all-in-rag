from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
import os
from langchain_openai import ChatOpenAI
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

from langchain.agents.middleware import AgentMiddleware, ToolCallRequest
from langchain_core.messages import ToolMessage, AIMessage, HumanMessage

def return_model_name(response: ModelResponse) -> str:
    """Helper function to extract model name from response metadata."""
    final_AIMessage = None
    for mesage in response["messages"]:
        if isinstance(mesage, AIMessage):
            final_AIMessage = mesage
    return final_AIMessage.response_metadata['model_name']

## 1. 定义工具
## 1.1 定义工具1(普通函数)
@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

## 1.2 定义工具运行时上下文结构
@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str

## 1.3 定义工具2(使用工具运行时)
@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "xian" if user_id == "1" else "beijing"

## 1.4 定义工具3（普通函数）
@tool
def calculate_temperature(city: str) -> str:
    """Calculate temperature based on user location."""
    return "25°C" if city == "xian" else "20°C"

## 1.5 定义动态选择工具中间件
class DynamicToolMiddleware(AgentMiddleware):
    """Middleware that registers and handles dynamic tools."""
    # 1.5.1 step1: 在模型调用前动态注册工具
    def wrap_model_call(self, request: ModelRequest, handler) -> ModelResponse:
        """Dynamic tools can be injected into tool list based on user intent."""
        user_message = "".join([m.content for m in request.state.get("messages", []) if isinstance(m, HumanMessage)])
        if "temperature" in user_message.lower():
            tools = [*request.tools, calculate_temperature]  # 仅当用户询问温度时才注入calculate_temperature工具
        else:
            tools = request.tools
        return handler(request.override(tools=tools))

    # 1.5.2 在工具调用前动态注册工具
    def wrap_tool_call(self, request: ToolCallRequest, handler) -> ToolMessage:
        """Intercept tool calls to handle dynamic tool logic."""
        if request.tool_call["name"] == "calculate_temperature":
            args = request.tool_call.get("args", {}) or {}
            city = args.get("city")
            if not city:  # 可能是用户直接询问温度而没有提供位置信息
                print("💡No city provided for temperature calculation, cannot proceed with calculate_temperature tool.")
                ctx = request.runtime.context
                args["city"] = get_user_location.func(runtime=ToolRuntime(context=ctx))  # 封装成Tool后的函数用.func调用
                return handler(request.override(tool_call={"args": args}, tool=calculate_temperature))  # 重新调用calculate_temperature工具
            else:  # 如果city存在，检查用户询问的位置是否在预设的位置列表中
                if city.lower() not in ["xian", "beijing"]:
                    print(f"💡City '{city}' is not supported for temperature calculation, cannot proceed with calculate_temperature tool.")
                    return ToolMessage(
                        content=f"Sorry, I can only calculate temperature for Xian and Beijing. '{city}' is not supported.",
                        tool_call_id=request.tool_call['id'],  # id必须保持不变以确保工具调用链的正确性
                    )
            return handler(request.override(tool=calculate_temperature))
        return handler(request)


## 2. 配置语言模型
## 2.1 普通模型
basic_model = ChatOpenAI(
	model="qwen-flash",
	temperature=0.7,
	max_tokens=1024,
	api_key=os.getenv("DASHSCOPE_API_KEY"),
	base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
## 2.2 高级模型
advanced_model = ChatOpenAI(
    model="qwen-flash-2025-07-28",
    temperature=0.7,
	max_tokens=1024,
	api_key=os.getenv("DASHSCOPE_API_KEY"),
	base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
## 2.3 模型选择逻辑
@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on conversation complexity."""
    message_count = len(request.state["messages"])
    if message_count > 10:
        new_model = advanced_model
    else:
        new_model = basic_model
    return handler(request.override(model=new_model))


## 3. 创建Agent
## 3.1 添加记忆
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
custom_serde = JsonPlusSerializer(
    allowed_msgpack_modules=[("__main__", "ResponseFormat")]
)
checkpointer = InMemorySaver(serde=custom_serde)
## 3.2 设置线程ID以启用记忆功能
config1 = {"configurable": {"thread_id": "1"}}
config2 = {"configurable": {"thread_id": "2"}}
config3 = {"configurable": {"thread_id": "3"}}
## 3.3 设置回答结构
@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    punny_response: str
    weather_conditions: str | None = None
## 3.4 创建Agent并指定回答结构
agent = create_agent(
    model=basic_model,  # 初始模型设置为basic_model，实际调用时会根据对话复杂度动态选择
    tools=[get_weather, get_user_location],
    middleware=[dynamic_model_selection, DynamicToolMiddleware()],  # 添加动态模型选择和动态工具中间件
    context_schema=Context,
    system_prompt="""You are a helpful assistant, 
        if a user asks question but doesn't specify a location, 
        use the get_user_location tool to find out where they are and provide the information that user cares about for that location.""",
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer,
)


## 4. 执行Agent
## 4.1 第一种对话
print("=== Conversation 1: Xian user asking about weather and temperature ===")
conversation1 = ["what is the weather outside?", "what about the temperature?", "thank you!"]
for msg in conversation1:  # 西安用户询问天气和温度，模型主动获取位置、主动获取温度
    print(f"User: {msg}")
    response = agent.invoke(
        {"messages": [{"role": "user", "content": msg}]},
        context=Context(user_id="1"),
        config=config1,
    )
    try:
        answer = response['structured_response']
    except Exception as e:
        answer = response["messages"][-1].content
    print(f"{return_model_name(response)}: {answer}")
## 4.2 第二种对话
print("\n=== Conversation 2: Beijing user asking about temperature without location ===")
conversation2 = ["what is the temperature tomorrow?", "thank you!"]
for msg in conversation2:  # 北京用户询问温度，模型动态注册计算温度工具、获取位置信息、计算温度
    print(f"User: {msg}")
    response = agent.invoke(
        {"messages": [{"role": "user", "content": msg}]},
        context=Context(user_id="2"),
        config=config2,
    )
    try:
        answer = response['structured_response']
    except Exception as e:
        answer = response["messages"][-1].content
    print(f"{return_model_name(response)}: {answer}")
## 4.3 第三种对话
print("\n=== Conversation 3: User asking about temperature in unsupported city like Shanghai ===")
conversation3 = ["what is the temperature in Shanghai?", "what about the weather there?", "thank you!"]
for msg in conversation3:  # 用户询问上海的温度，模型动态注册计算温度工具、检查用户提供的位置、返回错误提示
    print(f"User: {msg}")
    response = agent.invoke(
        {"messages": [{"role": "user", "content": msg}]},
        context=Context(user_id="1"),
        config=config3,
    )
    try:
        answer = response['structured_response']
    except Exception as e:
        answer = response["messages"][-1].content
    print(f"{return_model_name(response)}: {answer}")

