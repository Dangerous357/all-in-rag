from langchain.agents import create_react_agent, AgentExecutor
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool


## 1. 定义工具
@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


## 2. 设计prompt(需要按照ReAct的格式来设计prompt)
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)


## 3. 配置语言模型
llm = ChatOpenAI(
	model="qwen-flash",
	temperature=0.7,
	max_tokens=1024,
	api_key=os.getenv("DASHSCOPE_API_KEY"),
	base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1")


## 4. 创建ReAct Agent
agent = create_react_agent(
    llm=llm,
    tools=[get_weather],
    prompt=prompt,
)

agent_executor = AgentExecutor(
    agent=agent, 
    tools=[get_weather], 
    verbose=True,
    handle_parsing_errors=True
)


## 5. 执行Agent
agent_executor.invoke(
    {"input": "what is the weather in xian?"}
)