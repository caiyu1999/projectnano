'''
这个文件负责设计图的State
'''
# import pandas as pd 

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from operator import add 
from typing import Annotated

from pydantic.v1.errors import cls_kwargs



@dataclass 
class graph_state:
    '''
    用户的节点状态
    
    这个State类负责在图的节点之间传递数据。
    '''
    
    # --- 用户身份信息 ---
    user_id: Optional[str] = None  # need before init 初始化之前就要确定
    """用户的唯一标识，例如微信的OpenID。"""

    # --- 对话管理 ---
    messages: Annotated[List[BaseMessage], add_messages] = field(default_factory=list)
    """
    完整的对话历史。
    langgraph会使用add_messages函数来自动合并新的消息。
    """

    # --- Agent 工作区 ---
    agent_scratchpad: List[BaseMessage] = field(default_factory=list)
    """Agent在执行过程中的中间步骤（如工具调用、思考过程）"""

    # --- 任务信息 ---
    input: Optional[str] = None # need before init
    """当前用户的输入。"""
    
    chat_history: List[BaseMessage] = field(default_factory=list)
    """主要用于需要明确 `chat_history` 参数的Chain。"""

    num_files:int = field(default = 0)
    """用户上传的文件数量"""
    
    # --- 文件与数据 ---
    files: List[Dict[str, Any]] = field(default_factory=list) # need before init
    
    """
    处理过程中涉及的文件列表。
    每个字典可以包含文件名、路径、类型等信息。
    例如: [{'name': 'report.pdf', 'path': '/tmp/report.pdf'}]
    """
    
    file_format:List[Dict[str,Any]] = field(default_factory=list)
    '''
    初步解析获得的文件格式数据
    
    '''
    
    num_data:int = field(default = 0)
    """提取出来的数据数量"""
    data: List[Dict[str, Any]] = field(default_factory=list)
    """
    处理过程中涉及的数据列表。
    每个字典可以包含数据名、数据类型等信息。
    例如: [{'name': 'data1', 'type': 'data'}]
    """
    
    has_files: bool = False # need before init
    """
    用户是否上传了文件 用户可能会不需要文件数据来生成可视化
    """
    
    data_requirement:List[Dict[str, Any]] = field(default_factory=list)
    '''需要补充的data列表'''
    
    _std_error:Annotated[list[str],add] = field(default_factory=list)
    """
    标准错误列表 用于记录错误信息 用于debug
    """
    save_dir:str = field(default = "") # need before init 
    purpose:str = field(default = "无目的") # 论文 笔记 工作汇报 PPT汇报 申请书 专利 无目的 # need before init
    
    format_requirements :str = field(default = "无要求") # 用户对图片格式的要求 # need before init 
    
    status:str = field(default = "init state")
    
    goto:Annotated[list[str],add] = field(default_factory=list) #下一个将要去往的节点
    
    @classmethod
    def from_dict(cls,data:Dict[str,Any]):
        return cls(**data)
    
    
    def to_dict(self):
        return self.__dict__
    
    """
    当前处于哪个阶段
    - init state
    - extract data stage I  第一阶段的提取 
    - generate_extract_code  生成extract代码
    - execute_extract_code  执行extract代码
    - regenerate_extract_code 重新生成extract代码
    - complement_extract_code 补充提取代码

    """

     


if __name__ == '__main__':
    from langchain.schema import HumanMessage
    from langgraph.graph import StateGraph, START, END
    
    def update_message(state: graph_state):
        return {"messages": [HumanMessage(content=f"Hello, how are you?")]}
    
    # 初始化 graph_state
    test_state = graph_state(
        user_id="user123",
        messages=[],
        agent_scratchpad=[],
        input=None,
        chat_history=[],
        files=[],
        data = []

    )
    
    graph_builder = StateGraph(
        state_schema=graph_state,
    )
    
    graph_builder.add_node("update_message", update_message)
    graph_builder.add_node("update_message2", update_message)
    graph_builder.add_edge(START, "update_message")
    graph_builder.add_edge("update_message", "update_message2")
    graph_builder.add_edge("update_message2", END)
    graph = graph_builder.compile()
    
    result = graph.invoke(test_state)
    print(result['messages'])
    
    










