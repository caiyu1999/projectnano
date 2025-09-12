'''
这个文件负责设计图的State
'''
# import pandas as pd 

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Annotated
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langgraph.graph.message import add_messages
from operator import add

# 文件信息
@dataclass 
class FileInfo:
    user_id:str
    id:str
    path:str
    size:int
    type:str
    name:str
    readable:bool
    reachable:bool
    data:List[Dict[str, Any]] #从这个文件中获取的data数据
    def to_dict(self):
        return self.__dict__ 
    
@dataclass
class DataInfo:
    parent_id:str #它所属的fileid
    id:str
    path:str
    size:int
    type:str
    name:str
    metadata:Dict[str,Any] #元数据 记录这个文件的一些额外信息 如这个data的shape mean std等 取决于它的用户
    annotation:str #对这个data的描述 如这个data是用来做什么的 它的意义是什么 等等 由LLM生成
    def to_dict(self):
        return self.__dict__


@dataclass
class GraphState:
    """
    用户的节点状态
    这个State类负责在图的节点之间传递数据。
    """

    # --- 用户身份与上下文 ---
    user_id: Optional[str] = None
    save_dir: str = ""
    purpose: str = "无目的"  # 论文, 笔记, 工作汇报, PPT, 申请书, 专利, 无目的
    format_requirements: str = "无要求"  # 用户对图片格式的要求

    # --- 对话管理 ---
    messages: Annotated[List[BaseMessage], add_messages] = field(default_factory=list)
    input: Optional[str] = None 
    chat_history: Annotated[List[BaseMessage], add_messages] = field(default_factory=list)

    # --- 文件与数据处理 ---
    files: List[FileInfo] = field(default_factory=list)
    has_files: bool = False
    data: List[DataInfo] = field(default_factory=list) # 建议: [{'name': 'data1', 'dataframe_json': '...', 'description': '...'}]
    data_requirement: List[Dict[str, Any]] = field(default_factory=list)

    # --- 代码与执行管理 (新增) ---
    extraction_code:Annotated[List[str],add] = field(default_factory=list)
    visualization_code: Annotated[List[str],add] = field(default_factory=list)
    code_execution_stdout: Annotated[List[str],add] = field(default_factory=list)
    code_execution_stderr: Annotated[List[str],add] = field(default_factory=list)

    # --- 最终产物 (新增) ---
    generated_images: List[Dict[str, Any]] = field(default_factory=list) # [{'path': '...', 'url': '...', 'description': '...'}]

    # --- 状态与流程控制 ---
    status: str = "init_state"
    goto: Annotated[list[str], add] = field(default_factory=list)
    agent_errors: Annotated[list[str], add] = field(default_factory=list) # 原 _std_error

    # --- 交互与迭代 (新增) ---
    clarification_question_to_user: Optional[str] = None
    is_final_answer: bool = False

    # --- 商业化与计费 (新增) ---
    billable_events: Annotated[List[str], add] = field(default_factory=list)
    cost: float = 0.0
    
    # --- Agent 工作区 (可保留) ---
    agent_scratchpad: List[BaseMessage] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)

    def to_dict(self):
        # 注意: BaseMessage 对象不能直接JSON序列化，需要转换
        # 这里只是一个示例，实际应用中需要处理 messages 和 chat_history
        serializable_dict = self.__dict__.copy()
        serializable_dict['messages'] = [msg.__dict__ for msg in self.messages] # 简化处理
        serializable_dict['chat_history'] = [msg.__dict__ for msg in self.chat_history] # 简化处理
        serializable_dict['files'] = [file.to_dict() for file in self.files]
        serializable_dict['data'] = [data.to_dict() for data in self.data]
        return serializable_dict



    

if __name__ =='__main__':
    test_state = GraphState(
        files=[FileInfo(user_id='test', id='1',path='test.xlsx',size=100,type='excel',name='test',readable=True,reachable=True,data=[])],
        data=[DataInfo(parent_id='1',id='1',path='test.xlsx',size=100,type='excel',name='test',metadata={},annotation='test')],
    )
    print(test_state.to_dict())








