'''
配置类

'''
from dataclasses import dataclass,field 
from typing import List , Optional


# {'eps': 'Encapsulated Postscript', 'jpg': 'Joint Photographic Experts Group', 'jpeg': 'Joint Photographic Experts Group', 'pdf': 'Portable Document Format', 'pgf': 'PGF code for LaTeX', 'png': 'Portable Network Graphics', 'ps': 'Postscript', 'raw': 'Raw RGBA bitmap', 'rgba': 'Raw RGBA bitmap', 'svg': 'Scalable Vector Graphics', 'svgz': 'Scalable Vector Graphics', 'tif': 'Tagged Image File Format', 'tiff': 'Tagged Image File Format', 'webp': 'WebP Image Format'}


@dataclass
class UserConfig:
    '''
    配置类 随着项目推荐逐渐增加能够处理的数据类型
    之后按照用户等级分配可使用的功能以及可使用的数据类型
    '''
    runtime_path:Optional[str] = field(default="")
    # 这个用户的存储路径
    accept_file_type:List[str] = field(default_factory=list) 
    # 目前可接受的文件类型
    # excel csv txt npy npz pkl json 
    accept_data_type:List[str] = field(default_factory=list)
    # 目前可接受的extract数据类型
    # npy pkl npz
    accept_image_type:List[str] = field(default_factory=list)
    # 目前可接受的输出图片类型
    # eps jpg jpeg pdf pgf png ps raw rgba svg svgz tif tiff webp
   
    def to_dict(self):
        return self.__dict__






if __name__ == "__main__": 
    config = UserConfig() 
    print(config.to_dict())
    











