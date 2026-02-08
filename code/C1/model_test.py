import os
import asyncio
from openai import AsyncOpenAI
import platform

# 创建异步客户端实例
client = AsyncOpenAI(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

# 定义异步任务列表
async def task(question):
    print(f"发送问题: {question}")
    response = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant." },
            {"role": "user", "content": question}
        ],
        model="qwen-flash",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    )
    print(f"模型回复: {response.choices[0].message.content}")

# 主异步函数
async def main():
    questions = ["你是谁？", "你会什么？", "天气怎么样？"]
    tasks = [task(q) for q in questions]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    # 设置事件循环策略
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # 运行主协程
    asyncio.run(main(), debug=False)
