from langchain.chat_models import init_chat_model



llm = init_chat_model(
    model = 'gpt-4o-mini',
    base_url = 'https://api.chatanywhere.tech/v1',
    api_key = 'sk-Maf9m5KxsypZQ76kF2qQ6lsqLs3PL0cm2Bs3XeOD1yl6Lk86'
    
)


# # 假设你使用的国内模型支持 with_structured_output
# from langchain_community.chat_models import  # 假设存在类似封装
# from pydantic import BaseModel, Field

# # 1. 定义输出结构
# class Joke(BaseModel):
#     setup: str = Field(description="笑话的铺垫")
#     punchline: str = Field(description="笑话的笑点")

# # 2. 初始化模型并绑定输出结构
# # 注意：此方法需要模型底层支持，请查阅你所用模型的LangChain封装文档
# llm = ChatDeepSeek(model="deepseek-chat", api_key="your_api_key")
# structured_llm = llm.with_structured_output(Joke) # 核心代码

# # 3. 直接调用
# result = structured_llm.invoke("讲一个关于编程的笑话")
# print(result.setup)
# print(result.punchline)
# # 输出: Joke(setup='为什么程序员总是分不清万圣节和圣诞节？', punchline='因为 Oct 31 == Dec 25！')