'''
这个文件负责初步解析节点
'''
import time 
from graph.state.state import GraphState
from dataclasses import dataclass,field 
from uuid import uuid4 
from datetime import datetime
import chardet 
from utils.excel_ import comprehensive_excel_analysis
# @dataclass
# class file_format:
#     ''' 文件格式 单个文件 '''
#     file_id:str #文件id
#     file_path:str 
#     file_size:int #以字节为淡纹
#     file_type:str #文件类型 excel,pdf,docx,txt,etc
#     file_name:str #文件名
#     file_encoding:str #文件编码
#     parse_timestamp: datetime  # 解析时间戳
#     processing_time: float  # 处理耗时
#     file_metedata:dict #文件元数据 这里由大模型生成代码提取


class node_parser_files:
    '''
    这个节点填写FileInfo 
    
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
    
    这个节点负责将输入的文件进行初步解析
    
    '''
    def __init__(self) -> None:
        pass 
    
    
    def __call__(self,state:GraphState):
         
         # 获取filelist列表
        file_list = state.files 
        
        
        # 鉴空
        if file_list == [] and state.has_files:
            # 这里直接结束并跳转到END节点 返回错误信息
            return {
                "agent_errors":["文件列表为空"],
                "status":"extract data stage I",
                "goto":["FORCE_OUT"] # 返回强制退出节点
            } #直接返回空字典 由路由边决定下一步 
        
        
        file_format = []
        for file_index,file in enumerate(file_list):
            
            start_time = time.time()
            # 访问每一个文件 获取初步信息
            # 生成一个文件id
            
            file_id = str(uuid4())
            file_path = file['path']
            file_size = file['size']
            file_type = file['type']
            file_name = file['name']        
            
            
            # 获取文件编码
            try:
                with open(file_path, 'rb') as f:
                    raw_data = f.read(1000)
                    result = chardet.detect(raw_data)
                    file_encoding = result['encoding']
            except Exception as e:
                file_encoding = "Unknown"
            
            # 时间戳 
            parse_timestamp = datetime.now().strftime("%Y-%m-%d-%H")
            
            # 元数据
            file_metedata = {}
            
            # 处理时间
            processing_time = time.time() - start_time
            
            file_format_ = {
                "file_id":file_id,
                "file_path":file_path,
                "file_size":file_size,
                "file_type":file_type,
                "file_name":file_name,
                "file_format":parser_file(file_path,file_type),
                "file_encoding":file_encoding,
                "parse_timestamp":parse_timestamp,
                "processing_time":processing_time,
                "file_metedata":file_metedata
            }
            
            file_format.append(file_format_)
            
        return {
            "file_format":file_format,
            "num_files":len(file_format),
            "status":"extract data stage I",
            "goto":["generate_extract_code"]
        }
            
            
        
        
        
        
        
        
    # @dataclass
# class file_format:
#     ''' 文件格式 单个文件 '''
#     file_id:str 
#     file_path:str 
#     file_size:int #以字节为淡纹
#     file_type:str #文件类型 excel,pdf,docx,txt,etc
#     file_name:str #文件名
#     file_encoding:str #文件编码
#     parse_timestamp: datetime  # 解析时间戳
#     processing_time: float  # 处理耗时
#     file_metedata:dict #文件元数据 这里由大模型生成代码提取    
        
        
            
            
    
    
    