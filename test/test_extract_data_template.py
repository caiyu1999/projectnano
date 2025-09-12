


import os
import sys
from pathlib import Path


# 将项目根目录添加到 sys.path
project_root = Path(__file__).parent.parent  # 假设 test_parser_files.py 在 test/ 目录下
sys.path.append(str(project_root))

from graph.templates.extract_data import get_template
from graph.state.state import graph_state

def test_get_template():
    state = graph_state(
        status="generate_extract_code"
    )
    template = get_template(state)
    print("="*100)
    print("stage : generate_extract_code")
    print("="*100)
    print(template)
    
    state = graph_state(
        status="regenerate_extract_code"
    )
    template = get_template(state)
    print("="*100)
    print("stage : regenerate_extract_code")
    print("="*100)
    print(template)
    
    state = graph_state(
        status="complement_extract_code"
    )
    template = get_template(state)
    print("="*100)
    print("stage : complement_extract_code")
    print("="*100)
    print(template)
    
    

test_get_template()









