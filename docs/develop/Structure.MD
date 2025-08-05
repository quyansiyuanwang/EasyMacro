# EasyMacro 项目结构文档

## 项目概述

EasyMacro 是一个基于热键触发的宏管理系统，允许用户通过 JSON 配置文件定义自动化宏操作，并通过键盘热键触发执行。该项目集成了 RecognizerFramework 工作流引擎，提供强大的任务执行能力。

## 目录结构

```text
EasyMacro/
├── main.py                     # 项目入口文件
├── README.MD                   # 项目说明文档
├── docs/                       # 文档目录
│   ├── develop/               
│   │   └── Structure.MD        # 项目结构文档（本文件）
│   └── manual/
│       └── JsonField.MD        # JSON 字段使用说明
├── log/                        # 日志目录
│   └── example.log            # 示例日志文件
├── macros/                     # 宏配置目录
│   ├── macro.json             # 具体宏定义文件
│   ├── register.json          # 宏注册配置文件
│   └── schema/
│       └── generated.schema.json  # 宏配置 JSON Schema
├── script/                     # 脚本工具目录
│   ├── __init__.py
│   ├── __main__.py
│   ├── schema.py              # Schema 生成脚本
│   ├── workflows.json
│   └── util/
│       ├── __init__.py
│       └── util.py
├── src/                        # 源代码目录
│   ├── __init__.py
│   ├── CLI.py                 # 命令行接口
│   ├── Core/                  # 核心模块
│   │   ├── manager.py         # 宏管理器
│   │   ├── monitor.py         # 键盘监控器
│   │   └── trigger.py         # 触发器
│   ├── Models/                # 数据模型
│   │   ├── __init__.py
│   │   └── macro_json.py      # 宏 JSON 数据模型
│   ├── ThirdParty/            # 第三方库
│   │   └── RecognizerFramework/  # 工作流引擎框架
│   ├── Typehints/             # 类型提示
│   │   ├── __init__.py
│   │   └── basic.py
│   └── Util/                  # 工具模块
│       ├── __init__.py
│       └── utils.py           # 工具函数
└── tools/                      # 开发工具
    ├── __init__.py
    ├── __main__.py
    ├── GitCheckDiff/
    │   └── diff_only_docs.py
    ├── SingleScripts/
    │   ├── all_commit.py
    │   ├── check_type.py
    │   ├── clean.py
    │   ├── export_env.py
    │   ├── format.py
    │   ├── import_sort.py
    │   └── workflows.json
    └── util/
        ├── __init__.py
        └── util.py
```

## 核心模块架构

### 1. 程序入口 (`main.py`)

程序的主入口点，负责启动 CLI 接口：

```python
from src import cli

if __name__ == "__main__":
    cli()
```

### 2. CLI 模块 (`src/CLI.py`)

命令行接口模块，负责：

- 解析命令行参数
- 加载宏配置文件
- 启动宏管理系统

主要功能：

- `args_parse()`: 解析命令行参数
- `load_macros(path)`: 加载并启动宏系统
- `cli()`: CLI 主入口函数

### 3. 核心模块 (`src/Core/`)

#### 3.1 管理器 (`manager.py`)

`Manager` 类负责宏的管理：

- **宏加载**: 从 JSON 文件加载宏配置
- **宏存储**: 将宏配置保存到文件
- **宏管理**: 添加、获取宏定义

主要方法：

- `load_file(file_path)`: 从文件加载宏配置
- `save_file(file_path)`: 保存宏配置到文件
- `add_macro(name, macro)`: 添加新宏
- `macros`: 获取所有宏的属性

#### 3.2 触发器 (`trigger.py`)

`Trigger` 类负责宏的触发管理：

- **加载触发器**: 将宏的热键绑定到对应的工作流
- **启动监听**: 开始监听键盘事件
- **停止监听**: 停止键盘监听

主要方法：

- `load()`: 加载所有宏的触发器
- `run()`: 启动键盘监听
- `stop()`: 停止键盘监听

#### 3.3 监控器 (`monitor.py`)

`KeyboardMonitor` 类负责键盘事件监控：

- **热键注册**: 注册热键组合与回调函数的绑定
- **事件监听**: 监听键盘事件并触发回调
- **线程管理**: 支持多线程处理回调函数

主要功能：

- 支持多种热键格式（字符串、列表）
- 支持多个监控器实例
- 提供线程安全的回调执行
- 支持热键的动态注册和注销

### 4. 数据模型 (`src/Models/`)

#### 4.1 宏数据模型 (`macro_json.py`)

基于 Pydantic 的数据模型：

- **`Macro`**: 单个宏的定义
  - `description`: 宏的描述
  - `macro_json`: 宏工作流文件路径
  - `trigger`: 触发热键列表

- **`MacroSet`**: 宏集合
  - `macros`: 宏字典，键为宏名，值为 Macro 对象

### 5. 第三方集成 (`src/ThirdParty/`)

#### 5.1 RecognizerFramework

集成的工作流引擎框架，提供：

- 复杂的任务执行能力
- JSON 配置驱动的工作流
- 多种任务类型支持（输入、系统操作、计算等）

### 6. 工具模块 (`src/Util/`)

#### 6.1 工具函数 (`utils.py`)

提供通用工具函数：

- `to_indent_str()`: 格式化对象为缩进字符串，用于调试输出

## 数据流程

1. **启动阶段**:

   ```text
   main.py → CLI.py → args_parse() → load_macros()
   ```

2. **宏加载阶段**:

   ```text
   Manager.load_file() → MacroSet.from_json() → Macro 对象创建
   ```

3. **触发器注册阶段**:

   ```text
   Trigger.load() → KeyboardMonitor.add() → 热键与工作流绑定
   ```

4. **运行阶段**:

   ```text
   Trigger.run() → KeyboardMonitor.run() → 监听键盘事件
   ```

5. **宏执行阶段**:

   ```text
   热键触发 → RecognizerFramework.run() → 执行工作流
   ```

## 配置文件结构

### 宏注册文件 (`macros/register.json`)

```json
{
  "$schema": "./schema/generated.schema.json",
  "macros": {
    "宏名称": {
      "description": "宏描述",
      "macro_json": "宏工作流文件路径",
      "trigger": ["热键组合"]
    }
  }
}
```

### 宏工作流文件 (`macros/macro.json`)

遵循 RecognizerFramework 的 JSON 工作流格式，定义具体的执行步骤。

## 扩展性设计

1. **模块化**: 各功能模块独立，便于单独测试和维护
2. **插件化**: 通过 RecognizerFramework 支持多种任务类型
3. **配置化**: 通过 JSON 配置文件灵活定义宏行为
4. **类型安全**: 使用 Pydantic 确保数据类型安全

## 开发指南

1. **添加新宏**: 在 `macros/register.json` 中添加配置，并创建对应的工作流文件
2. **扩展功能**: 可通过继承或修改核心类来扩展功能
3. **自定义任务**: 在 RecognizerFramework 中添加自定义执行器
4. **调试**: 使用 `Manager.__repr__()` 方法查看加载的宏配置

## 依赖关系

- **keyboard**: 键盘事件监听
- **pydantic**: 数据验证和序列化
- **RecognizerFramework**: 工作流执行引擎
- **threading**: 多线程支持

这个架构设计确保了系统的模块化、可扩展性和易维护性，同时提供了强大的宏自动化能力。
