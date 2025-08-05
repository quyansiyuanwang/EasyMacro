# EasyMacro

![main language](https://img.shields.io/badge/python-3.13-blue?logo=python)
![platform](https://img.shields.io/badge/platform-windows-blueviolet.svg)
![license](https://img.shields.io/github/license/quyansiyuanwang/EasyMacro.svg)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/quyansiyuanwang/EasyMacro/checks.yml)
![repo size](https://img.shields.io/github/repo-size/quyansiyuanwang/EasyMacro)
![last commit](https://img.shields.io/github/last-commit/quyansiyuanwang/EasyMacro)
![doc last](https://img.shields.io/badge/docs%20last-2025--08--05-blue.svg)

一个基于热键触发的宏管理系统，通过 JSON 配置文件定义自动化宏操作，支持键盘、鼠标、文本输入等多种操作类型。

---

## ✨ 功能特性

- 🎯 **热键触发**: 支持多种热键组合，包括单键、组合键等
- 📝 **JSON 配置**: 通过 JSON 文件灵活定义宏行为，易于编辑和维护
- 🔧 **多任务类型**: 支持键盘输入、鼠标操作、文本输入、系统命令等
- 🎨 **工作流引擎**: 集成 RecognizerFramework，支持复杂的任务流程
- 🔍 **区域识别**: 支持图像识别和屏幕区域操作
- 📊 **日志记录**: 完整的日志系统，便于调试和监控
- 🧩 **模块化设计**: 清晰的架构，易于扩展和定制

---

## 🚀 快速开始

### 环境要求

- Python 3.13+
- Windows 操作系统
- 管理员权限（某些热键功能需要）

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/quyansiyuanwang/EasyMacro.git
cd EasyMacro

# 安装依赖
pip install -r requirements.txt
```

### 基本使用

1. **配置宏**：编辑 `macros/register.json` 文件添加你的宏定义

```json
{
  "$schema": "./schema/generated.schema.json",
  "macros": {
    "OpenSettings": {
      "description": "打开 Windows 设置",
      "macro_json": "macros/open_settings.json",
      "trigger": ["win+i"]
    }
  }
}
```

1. **创建工作流**：在 `macros/` 目录下创建对应的工作流文件

```json
{
  "$schema": "../src/ThirdParty/RecognizerFramework/workflow/schema/generated.schema.json",
  "begin": "OpenSettings",
  "jobs": {
    "OpenSettings": {
      "type": "Input",
      "input": {
        "type": "Keyboard",
        "keyboard": {
          "keys": ["win", "i"]
        }
      }
    }
  }
}
```

1. **运行程序**：

```bash
python main.py macros/register.json
```

1. **使用宏**：按下配置的热键（如 `Win+I`）触发宏执行

---

## 📖 使用指南

### 命令行使用

```bash
# 基本用法
python main.py <宏注册文件路径>

# 示例
python main.py macros/register.json
```

### 配置文件结构

EasyMacro 使用两种主要配置文件：

1. **宏注册文件** (`macros/register.json`)：定义宏的元数据和触发条件
2. **宏工作流文件** (`macros/*.json`)：定义具体的执行步骤

### 热键配置

支持多种热键格式：

```json
// 单个按键
"trigger": ["a"]

// 组合键
"trigger": ["ctrl+c"]
"trigger": ["alt+tab"] 
"trigger": ["ctrl+shift+n"]

// 多个触发器
"trigger": ["ctrl+shift+f", "f3"]

// 特殊键
"trigger": ["grave"]     // 反引号键 `
"trigger": ["space"]     // 空格键
"trigger": ["enter"]     // 回车键
```

### 任务类型

支持以下任务类型：

- **Input**: 键盘输入、鼠标操作、文本输入
- **ROI**: 屏幕区域识别和操作
- **System**: 系统命令、延时、日志等
- **Calculate**: 数学表达式计算
- **OCR**: 文字识别（如果可用）

---

## 📁 项目结构

```text
EasyMacro/
├── main.py                 # 程序入口
├── README.MD              # 项目说明（本文件）
├── docs/                  # 文档目录
│   ├── develop/
│   │   └── Structure.MD   # 项目结构文档
│   └── manual/
│       └── JsonField.MD   # JSON 字段说明
├── macros/                # 宏配置目录
│   ├── register.json      # 宏注册文件
│   ├── macro.json         # 示例宏工作流
│   └── schema/           # JSON Schema 文件
├── src/                   # 源代码
│   ├── CLI.py            # 命令行接口
│   ├── Core/             # 核心模块
│   ├── Models/           # 数据模型
│   ├── ThirdParty/       # 第三方库
│   └── Util/             # 工具函数
└── tools/                 # 开发工具
```

---

## 💡 示例宏

### 1. 快速截图

```json
// macros/register.json
{
  "macros": {
    "Screenshot": {
      "description": "快速截图",
      "macro_json": "macros/screenshot.json",
      "trigger": ["grave"]
    }
  }
}
```

```json
// macros/screenshot.json
{
  "$schema": "../src/ThirdParty/RecognizerFramework/workflow/schema/generated.schema.json",
  "begin": "TakeScreenshot",
  "jobs": {
    "TakeScreenshot": {
      "type": "Input",
      "input": {
        "type": "Keyboard",
        "keyboard": {
          "keys": ["win", "shift", "s"]
        }
      }
    }
  }
}
```

### 2. 快速搜索

```json
// 按 Ctrl+Shift+F 打开浏览器并搜索
{
  "macros": {
    "QuickSearch": {
      "description": "快速搜索",
      "macro_json": "macros/quick_search.json",
      "trigger": ["ctrl+shift+f"]
    }
  }
}
```

### 3. 文本模板

```json
// 快速输入常用文本
{
  "jobs": {
    "InsertEmail": {
      "type": "Input",
      "input": {
        "type": "Text",
        "text": {
          "text": "your.email@example.com"
        }
      }
    }
  }
}
```

---

## 🔧 高级功能

### 工作流控制

支持复杂的工作流控制：

- **条件分支**: 根据执行结果跳转到不同任务
- **循环控制**: 设置执行次数限制
- **错误处理**: 自定义错误处理逻辑
- **延时控制**: 任务前后添加延时

### 变量和计算

支持表达式计算和变量传递：

```json
{
  "type": "Calculate",
  "calculate": {
    "expressions": {
      "result": "x * 2 + y"
    },
    "variables": {
      "x": 10,
      "y": 5
    }
  }
}
```

### 区域识别

支持基于图像的屏幕区域识别：

```json
{
  "type": "ROI",
  "roi": {
    "type": "MoveMouse",
    "image": {
      "path": "images/button.png",
      "confidence": 0.8
    }
  }
}
```

---

## 🛠️ 开发指南

### 添加新宏

1. 在 `macros/register.json` 中添加宏定义
2. 创建对应的工作流文件
3. 重启程序加载新配置

### 扩展功能

EasyMacro 具有良好的扩展性：

- **自定义任务类型**: 在 RecognizerFramework 中添加新的执行器
- **自定义热键处理**: 修改 `KeyboardMonitor` 类
- **自定义数据模型**: 扩展 `Macro` 和 `MacroSet` 类

### 调试技巧

1. 启用调试模式：在工作流文件中设置 `"debug": true`
2. 查看日志：检查 `log/` 目录下的日志文件
3. 测试热键：使用简单的测试宏验证热键配置

---

## 📋 常见问题

### Q: 热键不生效怎么办？

A: 检查以下几点：

- 确保热键格式正确
- 检查是否与其他程序冲突
- 以管理员权限运行程序
- 确认宏配置文件路径正确

### Q: 如何退出程序？

A: 默认使用 `Ctrl+C` 退出程序，或在终端中按 `Ctrl+C`。

### Q: 支持哪些文件格式？

A: 目前支持 JSON 格式的配置文件，未来可能支持 YAML 等格式。

### Q: 如何备份配置？

A: 直接备份 `macros/` 目录即可，包含所有宏配置文件。

---

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范

- 使用 Python PEP 8 代码风格
- 添加适当的类型提示
- 编写清晰的文档字符串
- 添加必要的单元测试

---

## 📄 许可证

本项目采用 MIT 许可证。详细信息请查看 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- [RecognizerFramework](https://github.com/quyansiyuanwang/RecognizerFramework) - 强大的工作流引擎
- [keyboard](https://github.com/boppreh/keyboard) - Python 键盘事件处理
- [pydantic](https://github.com/pydantic/pydantic) - 数据验证和序列化

---

## 📞 联系方式

- 项目主页: [https://github.com/quyansiyuanwang/EasyMacro](https://github.com/quyansiyuanwang/EasyMacro)
- Issues: [https://github.com/quyansiyuanwang/EasyMacro/issues](https://github.com/quyansiyuanwang/EasyMacro/issues)

---

享受自动化的乐趣！🎉
