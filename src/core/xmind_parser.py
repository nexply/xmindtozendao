from xmindparser import xmind_to_dict
from typing import Dict, List, Any

class XMindParser:
    def __init__(self, xmind_file: str):
        self.xmind_file = xmind_file
        self.data = None

    def parse(self) -> List[Dict[str, Any]]:
        """解析XMind文件为字典格式"""
        try:
            self.data = xmind_to_dict(self.xmind_file)
            return self.data
        except Exception as e:
            raise Exception(f"解析XMind文件失败: {str(e)}")

    def get_root_topic(self) -> Dict[str, Any]:
        """获取根主题"""
        if not self.data or not self.data[0].get('topic'):
            raise Exception("无效的XMind文件格式")
        return self.data[0]['topic'] 