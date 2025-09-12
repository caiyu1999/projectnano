'''
大模型生成解析文件代码
'''
from graph.state.state import graph_state 
from langchain.prompts import ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate

## 身份定义
TEMPLATE_EXTRACT_DATA_IDENTIFY= """你是一个专业的Python数据处理代码助手,精通pandas,numpy,scipy,scikit等常用数据分析工具\n"""

# 你的任务是根据发送给你的数据结构、数据信息以及用户的问题，生成纯粹的数据提取和处理代码，
# 从数据中提取出用户要求可视化的数据，处理后将数据保存在本地。
# 之后另一个智能助手将会使用你的数据编写可视化代码。

#====================================================

## 任务定义

# 生成提取代码
TEMPLATE_EXTRACT_DATA_TASK_GENERATE= """你的任务是生成Python代码提取出文件中的数据并保存在本地以供可视化助手使用\n用户的需求是{user_demand}\n用户对图片的需求是{purpose}\n用户对图片格式的要求是{format_requirements}"""
# 提取报错纠正 
TEMPLATE_EXTRACT_DATA_TASK_REGENERATE= """你的任务是纠正提取代码中的错误并生成新的提取代码\n目前的报错信息是{std_error}\n产生报错的提取代码是{code}\n请改正产生报错的提取代码重新提取数据(错误代码提取的数据已被删除)"""
# 提取数据补充
TEMPLATE_EXTRACT_DATA_TASK_COMPLEMENT= """你的任务是补充提取代码中的数据并生成新的提取代码\n目前的提取代码是{code}\n目前缺少的数据是{data_requirement}\n请生成新的提取代码重新提取数据(最初的数据已经被删除)"""

# 文件信息
TEMPLATE_EXTRACT_DATA_FILE_INFO="""用户目前上传了{num_files}个文件,文件信息是{file_format}\n这些文件被保存在{save_dir}"""

# 代码要求
TEMPLATE_EXTRACT_DATA_TASK_GENERATE_REQUIREMENT= """你的代码需要满足以下要求:
1. 代码需要简洁明了,易于理解
2. 尽可能使用numpy的数据格式保存在{save_dir},并合理规范保存名称
3. 添加注释便于调试与理解
4. 使用Python语言

"""
TEMPLATE_EXTRACT_DATA_TASK_REGENERATE_REQUIREMENT= """你的代码需要满足以下要求:
1. 代码需要简洁明了,易于理解
2. 尽可能使用numpy的数据格式保存在{save_dir},并合理规范保存名称
3. 添加注释便于调试与理解
4. 使用Python语言
5. 完整的重新生成代码,而不是改正旧代码的一个部分,旧的代码和数据已经被删除
"""

TEMPLATE_EXTRACT_DATA_TASK_COMPLEMENT_REQUIREMENT= """你的代码需要满足以下要求:
1. 代码需要简洁明了,易于理解
2. 尽可能使用numpy的数据格式保存在{save_dir},并合理规范保存名称
3. 添加注释便于调试与理解
4. 使用Python语言
5. 完整的重新生成代码,而不是改正旧代码的一个部分,旧的代码和数据已经被删除
"""



# 辅助信息  从RAG中获取 待定




# 返回格式
TEMPLATE_EXTRACT_DATA_TASK_GENERATE_RETURN= """你的返回有以下两点:
1. 返回一个Python代码 如
```python
import pandas as pd 
#读取文件
file_1 = ...
```

2. 返回一个list[Dict[str,Any]]格式的数据记录 记录你的代码产生的数据的来源、用途、保存地址、数据内容 
e.g. 用户输入的文件["user_input_1.xlsx","user_input_2.xlsx"],用户的需求:"帮我将user_input_1与user_input_2中12月份的房屋出售数量在同一张图片中展示为折线图"
你应该返回[{{"source":"user_input_1.xlsx","purpose":"可视化数据","save_address":"save_dir/save_name_1.npy","data_content":"user_input_1中12月份的房屋出售情况"}},{{"source":"user_input_2.xlsx","purpose":"可视化数据","save_address":"save_dir/save_name_2.npy","data_content":"user_input_2中12月份的房屋出售情况"}}]
"""

TEMPLATE_EXTRACT_DATA_TASK_REGENERATE_RETURN= """你的返回有以下两点:
1. 返回一个Python代码 如
```python
import pandas as pd 
#读取文件
file_1 = ...
```

2. 返回一个list[Dict[str,Any]]格式的数据记录 记录你的代码产生的数据的来源、用途、保存地址、数据内容 
e.g. 用户输入的文件["user_input_1.xlsx","user_input_2.xlsx"],用户的需求:"帮我将user_input_1与user_input_2中12月份的房屋出售数量在同一张图片中展示为折线图"
你应该返回[{{"source":"user_input_1.xlsx","purpose":"可视化数据","save_address":"save_dir/save_name_1.npy","data_content":"user_input_1中12月份的房屋出售情况"}},{{"source":"user_input_2.xlsx","purpose":"可视化数据","save_address":"save_dir/save_name_2.npy","data_content":"user_input_2中12月份的房屋出售情况"}}]
"""

TEMPLATE_EXTRACT_DATA_TASK_COMPLEMENT_RETURN= """你的返回有以下两点:
1. 返回一个Python代码 如
```python
import pandas as pd 
#读取文件
file_1 = ...
```

2. 返回一个list[Dict[str,Any]]格式的数据记录 记录你的代码产生的数据的来源、用途、保存地址、数据内容 
e.g. 用户输入的文件["user_input_1.xlsx","user_input_2.xlsx"],用户的需求:"帮我将user_input_1与user_input_2中12月份的房屋出售数量在同一张图片中展示为折线图"
你应该返回[{{"source":"user_input_1.xlsx","purpose":"可视化数据","save_address":"save_dir/save_name_1.npy","data_content":"user_input_1中12月份的房屋出售情况"}},{{"source":"user_input_2.xlsx","purpose":"可视化数据","save_address":"save_dir/save_name_2.npy","data_content":"user_input_2中12月份的房屋出售情况"}}]
"""


WARNING = """
WARNING:
注意事项:
1. 代码中出现的所有路径必须为绝对路径
2. 你不需要可视化这个图片 ,只需要保存文件在本地即可

"""








def get_template(state:graph_state):
    # 根据当前处于哪个阶段 
    now_status = state.status
    system_template = TEMPLATE_EXTRACT_DATA_IDENTIFY
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    if now_status == "generate_extract_code":
        human_template = TEMPLATE_EXTRACT_DATA_TASK_GENERATE+TEMPLATE_EXTRACT_DATA_FILE_INFO+TEMPLATE_EXTRACT_DATA_TASK_GENERATE_REQUIREMENT+TEMPLATE_EXTRACT_DATA_TASK_GENERATE_RETURN+WARNING
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        return ChatPromptTemplate.from_messages([system_message_prompt,human_message_prompt])
    
    elif now_status == "regenerate_extract_code":
        human_template = TEMPLATE_EXTRACT_DATA_TASK_REGENERATE+TEMPLATE_EXTRACT_DATA_FILE_INFO+TEMPLATE_EXTRACT_DATA_TASK_REGENERATE_REQUIREMENT+TEMPLATE_EXTRACT_DATA_TASK_REGENERATE_RETURN+WARNING
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        return ChatPromptTemplate.from_messages([system_message_prompt,human_message_prompt])
    
    elif now_status == "complement_extract_code":
        human_template = TEMPLATE_EXTRACT_DATA_TASK_COMPLEMENT+TEMPLATE_EXTRACT_DATA_FILE_INFO+TEMPLATE_EXTRACT_DATA_TASK_COMPLEMENT_REQUIREMENT+TEMPLATE_EXTRACT_DATA_TASK_COMPLEMENT_RETURN+WARNING
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        return ChatPromptTemplate.from_messages([system_message_prompt,human_message_prompt])
    
    else:# 如果是其他节点进入 那么可能出现了问题
        return None 
