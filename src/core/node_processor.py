from typing import Dict, List, Any, Optional

class NodeProcessor:
    """
    XMind节点处理器类
    用于将XMind思维导图中的测试用例节点转换为结构化的测试用例数据
    """
    def __init__(self):
        self.test_cases = []  # 存储所有处理后的测试用例
        self.current_module = ""  # 当前正在处理的模块名称
        self.debug = False  # 调试模式开关
        self.processed_cases = set()  # 用于存储已处理的用例ID，防止重复处理

    def process_node(self, node: Dict[str, Any], parent_path: List[str] = None, parent_note: str = "", parent_labels: List[str] = None) -> None:
        """
        处理单个XMind节点
        
        Args:
            node: XMind节点数据
            parent_path: 父节点路径列表
            parent_note: 父节点的备注
            parent_labels: 父节点的标签列表
        """
        # 初始化参数
        if parent_path is None:
            parent_path = []
        if parent_labels is None:
            parent_labels = []

        # 获取当前节点标题
        title = node.get('title', '').strip()
        
        if self.debug:
            print(f"处理节点: {title}")

        # 忽略注释节点（以#开头）及其子节点
        if title.startswith('#'):
            return

        # 构建当前节点的完整路径
        current_path = parent_path.copy()
        if title:  # 所有节点都加入路径，包括模块节点
            current_path.append(title)

        # 处理模块节点（以/开头）
        if title.startswith('/'):
            self.current_module = title  # 保留完整模块名（包含/）
            if self.debug:
                print(f"设置当前模块: {self.current_module}")
            # 重置父级信息，但保留当前模块路径
            parent_path = [title]  # 保留模块路径
            parent_note = ""  
            parent_labels = []  
            
        # 处理节点的备注信息
        current_note = node.get('note', '').strip()
        if not current_note:  # 如果当前节点没有备注，使用父节点的备注
            current_note = parent_note

        # 处理节点的标签信息
        current_labels = node.get('labels', [])
        if not current_labels:  # 如果当前节点没有标签，使用父节点的标签
            current_labels = parent_labels.copy()

        # 检查是否是用例节点
        makers = node.get('makers', [])  # 获取节点的标记（优先级标记）
        
        # 判断是否为用例节点：只需要有优先级标记
        if makers:
            priority = self._get_priority_from_maker(makers[0])
            if priority:
                # 生成用例标题（使用完整路径）
                case_title = '-'.join(current_path)
                # 生成用例唯一标识（使用模块和完整路径）
                case_id = f"{self.current_module}_{'-'.join(current_path)}"
                
                # 检查是否是以/开头的路径
                if current_path and current_path[0].startswith('/'):
                    if case_id not in self.processed_cases:
                        if self.debug:
                            print(f"发现用例节点: {case_title}, 优先级: {priority}, 路径: {current_path}")
                        # 创建测试用例，去除标题开头的/
                        self._create_test_case(
                            node,
                            case_title.lstrip('/'),  # 去除标题开头的/
                            priority,
                            current_labels[0] if current_labels else '',
                            current_note
                        )
                        self.processed_cases.add(case_id)
                    elif self.debug:
                        print(f"跳过重复用例: {case_title}")
                elif self.debug:
                    print(f"跳过非模块路径下的用例: {case_title}")

        # 递归处理所有子节点
        if 'topics' in node:
            for subtopic in node['topics']:
                self.process_node(subtopic, current_path, current_note, current_labels)

    def _create_test_case(self, node: Dict, title: str, priority: int, case_type: str, precondition: str) -> None:
        """
        创建测试用例对象
        
        Args:
            node: 用例节点数据
            title: 用例标题
            priority: 优先级
            case_type: 用例类型
            precondition: 前置条件
        """
        # 处理测试步骤和预期结果
        steps, expects = self._process_steps(node.get('topics', []))
        
        # 创建测试用例字典
        test_case = {
            'module': f"/{self.current_module.lstrip('/')}",  # 确保模块名带上/开头
            'title': '-'.join(title.split('-')[1:]) if '-' in title else title,  # 去掉模块那一级
            'type': case_type,
            'priority': priority,
            'precondition': precondition,
            'steps': steps,
            'expects': expects
        }

        if self.debug:
            print(f"添加测试用例: {test_case}")

        self.test_cases.append(test_case)

    def _process_steps(self, steps_nodes: List[Dict[str, Any]]) -> tuple[str, str]:
        """
        处理测试步骤和预期结果
        
        Args:
            steps_nodes: 步骤节点列表
            
        Returns:
            tuple: (步骤字符串, 预期结果字符串)
        """
        steps = []
        expects = []
        
        # 处理每个步骤节点
        for i, step_node in enumerate(steps_nodes, 1):
            step = step_node.get('title', '').strip()
            if step:
                # 添加步骤（格式：1. 步骤1）
                steps.append(f"{i}. {step}")
                
                # 处理步骤的预期结果（子节点）
                for j, expect_node in enumerate(step_node.get('topics', []), 1):
                    expect = expect_node.get('title', '').strip()
                    if expect:
                        # 如果是子步骤的预期结果，使用 3.1 格式
                        if '.' in step:
                            step_num = step.split('.')[0]
                            expects.append(f"{step_num}.{j}. {expect}")
                        else:
                            # 普通步骤的预期结果（格式：1. 预期1）
                            expects.append(f"{i}. {expect}")

        # 将步骤和预期结果转换为字符串格式
        return '\n'.join(steps), '\n'.join(expects)

    @staticmethod
    def _get_priority_from_maker(maker: str) -> Optional[int]:
        """
        从标记获取优先级
        
        Args:
            maker: 优先级标记字符串
            
        Returns:
            Optional[int]: 优先级数值，如果无法识别则返回None
        """
        # 优先级标记映射表
        priority_map = {
            'priority-1': 1,
            'priority-2': 2,
            'priority-3': 3,
            'priority-4': 4,
            'p1': 1,
            'p2': 2,
            'p3': 3,
            'p4': 4,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4
        }
        return priority_map.get(maker) 