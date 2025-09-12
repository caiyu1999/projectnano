


import os
import sys
from pathlib import Path


# 将项目根目录添加到 sys.path
project_root = Path(__file__).parent.parent  # 假设 test_parser_files.py 在 test/ 目录下
sys.path.append(str(project_root))

# 现在可以正常导入 graph 模块
from graph.state.state import graph_state
from graph.node.parser_files import node_parser_files
from langgraph.graph import START,END,StateGraph

def get_file_info(file_path):
    # 使用Path对象
    file = Path(file_path)
    
    # 获取文件大小（字节）
    size = os.path.getsize(file_path)
    
    # 获取文件类型（通过扩展名判断）
    file_type = file.suffix.lower() if file.suffix else "Unknown"
    
    # 获取文件名（不含路径）
    name = file.name
    
    return {
        "path": file_path,
        "size": size,
        "type": file_type,
        "name": name
    }



# file_path = file['path']
#             file_size = file['size']
#             file_type = file['type']
#             file_name = file['name']     

def test_node_parser_files(test_file_path):
    # 获取文件信息
    test_list = []
    for file in test_file_path:
        file_info = {
            "path": file,
            "size": os.path.getsize(file), #  
            "type": Path(file).suffix.lower() if Path(file).suffix else "Unknown",
            "name": Path(file).name
        }
        test_list.append(file_info)
        
    
    test_state = graph_state(
        user_id="user123",
        messages=[],
        agent_scratchpad=[],
        input=None,
        chat_history=[],
        files=test_list,  # 直接使用file_info字典
        data=[]
    )
    
    graph_builder = StateGraph(
        state_schema=graph_state,
    )
    
    graph_builder.add_node("node_parser_files", node_parser_files())
    graph_builder.add_edge(START, "node_parser_files")
    graph_builder.add_edge("node_parser_files", END)
    graph = graph_builder.compile()
    
    result = graph.invoke(test_state)

    print(result)







if __name__ == '__main__':
    test_node_parser_files(['/home/tianfang/project_Mat_new/test.xlsx','/home/tianfang/project_Mat_new/test.md'])



























