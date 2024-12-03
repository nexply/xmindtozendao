import pandas as pd
import os
from typing import List, Dict, Any

class CSVGenerator:
    def __init__(self, output_file: str):
        self.output_file = output_file

    def generate(self, test_cases: List[Dict[str, Any]]) -> None:
        """生成CSV文件"""
        # 检查文件是否存在
        if os.path.exists(self.output_file):
            while True:
                response = input(f"文件 '{self.output_file}' 已存在，是否覆盖？(y/n): ").lower()
                if response in ['y', 'n']:
                    if response == 'n':
                        print("操作已取消")
                        return
                    break
                print("请输入 y 或 n")

        # 创建DataFrame
        df = pd.DataFrame(test_cases)
        
        # 设置列顺序和中文列名
        columns = ['module', 'title', 'type', 'priority', 'precondition', 'steps', 'expects']
        chinese_columns = ['所属模块', '用例标题', '用例类型', '优先级', '前置条件', '步骤', '预期']
        
        # 确保所有必需的列都存在
        for col in columns:
            if col not in df.columns:
                df[col] = ''
        
        # 选择并重命名列
        df = df[columns]
        df.columns = chinese_columns

        # 保存为CSV
        df.to_csv(self.output_file, index=False, encoding='utf-8-sig') 