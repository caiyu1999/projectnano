


import os
import sys
from pathlib import Path

from chardet import resultdict


# 将项目根目录添加到 sys.path
project_root = Path(__file__).parent.parent  # 假设 test_parser_files.py 在 test/ 目录下
sys.path.append(str(project_root))

# 现在可以正常导入 graph 模块
from graph.state.state import graph_state
from graph.node.parser_files import node_parser_files
from graph.templates.extract_data import get_template
from langgraph.graph import START,END,StateGraph
from graph.node.parser_files import graph_state
from test_LLM import llm
# file_path = file['path']
# file_size = file['size']
# file_type = file['type']
# file_name = file['name'] 

file_4fix_path = '/home/tianfang/project_Mat_new/4fix.xlsx'
file_4simply_path = '/home/tianfang/project_Mat_new/4simply.xlsx'


def get_file_info(file_path):
    file = Path(file_path)
    size = os.path.getsize(file_path)
    file_type = file.suffix.lower() if file.suffix else "Unknown"
    name = file.name
    return {
        "path": file_path,
        "size": size,
        "type": file_type,
        "name": name
    }




test_graph_state = graph_state(
    user_id = 'test_123',
    input = '帮我将4fix,4simply中的数据三维可视化 放在一张图片上',
    files = [get_file_info(file_4fix_path),get_file_info(file_4simply_path)],
    has_files = True,
    save_dir = '/home/tianfang/project_Mat_new'
)

graph_builder = StateGraph(
        state_schema=graph_state,
    )
    
graph_builder.add_node("node_parser_files", node_parser_files())
graph_builder.add_edge(START, "node_parser_files")
graph_builder.add_edge("node_parser_files", END)
graph = graph_builder.compile()

result = graph.invoke(test_graph_state)
result['status'] = 'generate_extract_code'
result = graph_state.from_dict(result)
# result_dict = result.to_dict()


prompt = get_template(result)
print(prompt.input_variables)#['file_format', 'format_requirements', 'num_files', 'purpose', 'save_dir', 'user_demand']

# print(prompt.invoke(
#     {
#         "file_format":result.file_format,
#         "format_requirements":result.format_requirements,
#         "num_files":result.num_files,
#         "purpose":result.purpose,
#         "save_dir":result.save_dir,
#         "user_demand":result.input
#     }
# ))


chain = prompt | llm

print(chain.invoke(
    {
        "file_format":result.file_format,
        "format_requirements":result.format_requirements,
        "num_files":result.num_files,
        "purpose":result.purpose,
        "save_dir":result.save_dir,
        "user_demand":result.input
    }
).content)