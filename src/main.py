#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from typing import Dict, Any

# 获取程序运行时的目录
if getattr(sys, 'frozen', False):
    # 如果是打包后的exe在运行
    application_path = os.path.dirname(sys.executable)
else:
    # 如果是python脚本在运行
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

from core.xmind_parser import XMindParser
from core.node_processor import NodeProcessor
from utils.csv_generator import CSVGenerator

def get_output_filename(xmind_file: str) -> str:
    """根据xmind文件名生成输出文件名，保持在同一目录下"""
    # 获取输入文件的目录
    dir_path = os.path.dirname(os.path.abspath(xmind_file))
    # 获取文件名（不含扩展名）
    base_name = os.path.splitext(os.path.basename(xmind_file))[0]
    # 在同一目录下生成csv文件路径
    return os.path.join(dir_path, f"{base_name}.csv")

def process_topic(processor: NodeProcessor, topic: Dict[str, Any]) -> None:
    """递归处理主题及其子主题"""
    processor.process_node(topic)
    # 处理子主题
    if 'topics' in topic:
        for subtopic in topic['topics']:
            process_topic(processor, subtopic)

def main():
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("使用方法: python main.py <输入的xmind文件> [输出的csv文件]")
        print("注意: 如果不指定输出文件名，将在xmind文件所在目录下生成同名csv文件")
        sys.exit(1)

    xmind_file = sys.argv[1]
    
    # 如果没有提供输出文件名，自动生成（保持在同一��录）
    csv_file = sys.argv[2] if len(sys.argv) > 2 else get_output_filename(xmind_file)

    if not os.path.exists(xmind_file):
        print(f"错误: 找不到XMind文件 '{xmind_file}'")
        sys.exit(1)

    try:
        # 解析XMind文件
        parser = XMindParser(xmind_file)
        data = parser.parse()

        # 处理节点
        processor = NodeProcessor()
        # 从topics开始处理，跳过根节点
        if data and 'topic' in data[0] and 'topics' in data[0]['topic']:
            for topic in data[0]['topic']['topics']:
                process_topic(processor, topic)
        else:
            raise Exception("无效的XMind文件格式")

        if not processor.test_cases:
            raise Exception("未找到任何测试用例")

        # 生成CSV文件
        generator = CSVGenerator(csv_file)
        generator.generate(processor.test_cases)

        print(f"转换成功! 已生成CSV文件: {csv_file}")
        print(f"共转换 {len(processor.test_cases)} 个测试用例")

    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 