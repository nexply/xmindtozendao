# XMind to ZenTao Converter (XMind 转 禅道测试用例转换工具)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

[English](#english) | [中文](#中文)

# English

A simple and efficient tool for converting XMind mind maps to ZenTao test cases.

## ✨ Features

- Support XMind >= 23.0 format files
- Automatically generate ZenTao-compatible CSV format test cases
- Maintain mind map hierarchical structure
- Support test case priority, type, and other attributes
- Support batch processing mode
- Support custom output path
- Simple command-line interface

## 🚀 Quick Start

### Installation

1. Download the latest release
2. Extract to any directory
3. Run the executable directly, no additional dependencies required

### Usage

```bash
xmindtozendao.exe <XMind_file_path> [output_CSV_file_path]
```

Example:
```bash
xmindtozendao.exe "D:\TestProject\testcase.xmind"
```

If no output file path is specified, a CSV file with the same name will be generated in the same directory as the input file.

## 📝 Conversion Rules

### Node Processing Rules
1. Root node will be ignored
2. Nodes starting with "#" and their children will be ignored (for comments)
3. Nodes starting with "/" will be identified as the module to which the test case belongs

### Test Case Title Generation Rules
- The path from parent node to marked node will form the test case title
- Nodes are concatenated using "-"

### Test Case Attribute Rules
- Node notes: Will be used as preconditions for all test cases under that node
- Node tags: Will be used as test case type
- Node markers (1/2/3/4): Correspond to test case priority

### Steps and Expected Results
- Child nodes of marked nodes: Used as test steps
- Child nodes of test steps: Used as expected results

---

# 中文

一个简单高效的工具，用于将 XMind 思维导图转换为禅道(ZenTao)测试用例。

## ✨ 特性

- 支持 XMind >= 23.0 格式文件转换
- 自动生成禅道兼容的 CSV 格式测试用例
- 保持思维导图的层级结构
- 支持测试用例优先级、类型等属性
- 支持批处理模式
- 支持自定义输出路径
- 简单的命令行界面

## 🚀 快速开始

### 安装

1. 下载最新的发布版本
2. 解压到任意目录
3. 直接运行可执行文件，无需安装其他依赖

### 使用方法

```bash
xmindtozendao.exe <XMind文件路径> [输出CSV文件路径]
```

示例：
```bash
xmindtozendao.exe "D:\测试项目\测试用例.xmind"
```

如果不指定输出文件路径，将在输入文件的同目录下生成同名的 CSV 文件。

## 📝 转换规则

### 节点处理规则
1. 根节点将被忽略
2. 以 "#" 开头的节点及其子节点将被忽略（用于注释）
3. 以 "/" 开头的节点名称将被识别为用例所属模块

### 用例标题生成规则
- 从父节点到存在标记的节点的路径将组成用例标题
- 节点间使用 "-" 拼接

### 用例属性规则
- 节点笔记：将作为该节点下所有用例的前置条件
- 节点标签：将作为用例类型
- 节点标记(1/2/3/4)：对应用例优先级

### 步骤和预期
- 带标记的节点的子节点：作为测试步骤
- 测试步骤的子节点：作为预期结果

## 📂 项目结构

```
xmindtozendao/
├── src/                    # 源代码目录
│   ├── core/              # 核心功能模块
│   │   ├── xmind_parser.py    # XMind 解析器
│   │   └── node_processor.py  # 节点处理器
│   ├── utils/             # 工具函数
│   │   └── csv_generator.py   # CSV 生成器
│   └── main.py           # 主程序入口
├── dist/                  # 构建输出目录
├── build/                 # 构建过程目录
└── README.md             # 项目文档
```

## 🛠️ 开发环境设置 | Development Environment Setup

如果你想参与开发，需要以下环境：
If you want to participate in development, you need:

1. Python 3.6 或更高版本 | Python 3.6 or higher
2. 安装依赖 | Install dependencies:
```bash
pip install -r requirements.txt
```

## 📄 许可证 | License

本项目采用  Apache License Version 2.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🤝 贡献 | Contributing

欢迎贡献代码、报告问题或提出新功能建议！
Welcome to contribute code, report issues, or suggest new features!

1. Fork 本仓库 | Fork this repository
2. 创建特性分支 | Create feature branch: `git checkout -b feature/AmazingFeature`
3. 提交更改 | Commit changes: `git commit -m 'Add some AmazingFeature'`
4. 推送分支 | Push to branch: `git push origin feature/AmazingFeature`
5. 提交 Pull Request | Open a Pull Request

## 📮 联系方式 | Contact

如果你有任何问题或建议，欢迎提出 Issue 或 Pull Request。
If you have any questions or suggestions, please feel free to open an Issue or Pull Request.

## 🙏 致谢 | Acknowledgments

- 感谢所有贡献者的支持 | Thanks to all contributors
- 感谢 XMind 和禅道(ZenTao)提供优秀的工具 | Thanks to XMind and ZenTao for providing excellent tools
