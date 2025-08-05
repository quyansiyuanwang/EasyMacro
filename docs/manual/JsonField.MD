# EasyMacro JSON 字段说明文档

## 目录

- [EasyMacro JSON 字段说明文档](#easymacro-json-字段说明文档)
  - [目录](#目录)
  - [概述](#概述)
  - [宏注册文件 (register.json)](#宏注册文件-registerjson)
    - [顶层字段](#顶层字段)
    - [Macro 对象字段](#macro-对象字段)
    - [触发热键格式](#触发热键格式)
      - [单个按键](#单个按键)
      - [组合键](#组合键)
      - [特殊键名](#特殊键名)
      - [多个触发器](#多个触发器)
  - [宏工作流文件 (macro.json)](#宏工作流文件-macrojson)
    - [工作流结构](#工作流结构)
  - [完整示例](#完整示例)
    - [宏注册文件示例](#宏注册文件示例)
    - [宏工作流文件示例](#宏工作流文件示例)
      - [1. 简单的键盘输入宏 (`macros/open_settings.json`)](#1-简单的键盘输入宏-macrosopen_settingsjson)
      - [2. 复杂的多步骤宏 (`macros/quick_search.json`)](#2-复杂的多步骤宏-macrosquick_searchjson)
      - [3. 带条件分支的宏 (`macros/screenshot.json`)](#3-带条件分支的宏-macrosscreenshotjson)
  - [最佳实践](#最佳实践)
  - [常见问题](#常见问题)

---

## 概述

EasyMacro 使用两种主要的 JSON 配置文件：

1. **宏注册文件** (`macros/register.json`): 定义宏的元数据和触发条件
2. **宏工作流文件** (`macros/macro.json`): 定义具体的执行步骤，遵循 RecognizerFramework 格式

这两个文件通过 `macro_json` 字段建立关联。

---

## 宏注册文件 (register.json)

宏注册文件定义了系统中所有宏的元信息和触发条件。

### 顶层字段

| 字段名  | 类型   | 是否必需 | 说明                                    |
| ------- | ------ | -------- | --------------------------------------- |
| $schema | string | 可选     | JSON Schema 文件路径，用于验证和智能提示 |
| macros  | object | 必需     | 宏定义字典，键为宏名，值为 Macro 对象   |

### Macro 对象字段

| 字段名      | 类型     | 是否必需 | 说明                                           |
| ----------- | -------- | -------- | ---------------------------------------------- |
| description | string   | 可选     | 宏的描述信息，用于说明宏的用途                 |
| macro_json  | string   | 必需     | 宏工作流文件的相对路径或绝对路径               |
| trigger     | string[] | 必需     | 触发热键列表，支持多种格式的热键组合           |

### 触发热键格式

EasyMacro 支持以下热键格式：

#### 单个按键

```json
"trigger": ["a"]           // 按下 A 键
"trigger": ["space"]       // 按下空格键
"trigger": ["enter"]       // 按下回车键
```

#### 组合键

```json
"trigger": ["ctrl+c"]      // Ctrl + C
"trigger": ["alt+tab"]     // Alt + Tab
"trigger": ["ctrl+shift+n"] // Ctrl + Shift + N
```

#### 特殊键名

常用的特殊键名包括：

- **修饰键**: `ctrl`, `alt`, `shift`, `win`
- **功能键**: `f1`, `f2`, ..., `f12`
- **方向键**: `up`, `down`, `left`, `right`
- **其他**: `space`, `enter`, `tab`, `esc`, `backspace`, `delete`
- **符号键**: `grave` (反引号), `minus` (-), `equal` (=) 等

#### 多个触发器

```json
"trigger": ["ctrl+shift+a", "f12"]  // 可以用 Ctrl+Shift+A 或 F12 触发
```

---

## 宏工作流文件 (macro.json)

宏工作流文件定义了宏的具体执行步骤，使用 RecognizerFramework 的 JSON 工作流格式。

### 工作流结构

工作流文件的详细格式请参考 RecognizerFramework 的文档。主要字段包括：

| 字段名  | 类型   | 说明                                   |
| ------- | ------ | -------------------------------------- |
| $schema | string | 工作流 Schema 文件路径                 |
| begin   | string | 起始任务名，必须是 jobs 中的一个任务   |
| globals | object | 全局配置，如调试模式、日志设置等       |
| jobs    | object | 任务定义，键为任务名，值为任务配置     |

**支持的任务类型:**

- **Input**: 输入操作（键盘、鼠标、文本）
- **ROI**: 区域识别和鼠标操作
- **System**: 系统操作（延时、日志、粘贴等）
- **Calculate**: 表达式计算
- **OCR**: 文字识别

详细的工作流字段说明请参考 RecognizerFramework 的文档。

---

## 完整示例

### 宏注册文件示例

```json
{
  "$schema": "./schema/generated.schema.json",
  "macros": {
    "OpenSettings": {
      "description": "打开 Windows 设置",
      "macro_json": "macros/open_settings.json",
      "trigger": ["win+i"]
    },
    "QuickSearch": {
      "description": "快速搜索",
      "macro_json": "macros/quick_search.json", 
      "trigger": ["ctrl+shift+f", "f3"]
    },
    "Screenshot": {
      "description": "截图工具",
      "macro_json": "macros/screenshot.json",
      "trigger": ["grave"]
    },
    "CopyDateTime": {
      "description": "复制当前日期时间",
      "macro_json": "macros/copy_datetime.json",
      "trigger": ["ctrl+alt+d"]
    }
  }
}
```

### 宏工作流文件示例

#### 1. 简单的键盘输入宏 (`macros/open_settings.json`)

```json
{
  "$schema": "../src/ThirdParty/RecognizerFramework/workflow/schema/generated.schema.json",
  "begin": "OpenSettings",
  "globals": {
    "debug": false,
    "colorful": true
  },
  "jobs": {
    "OpenSettings": {
      "type": "Input",
      "description": "打开 Windows 设置",
      "input": {
        "type": "Keyboard",
        "keyboard": {
          "keys": ["win", "i"],
          "duration": 0,
          "sep_time": 100
        }
      }
    }
  }
}
```

#### 2. 复杂的多步骤宏 (`macros/quick_search.json`)

```json
{
  "$schema": "../src/ThirdParty/RecognizerFramework/workflow/schema/generated.schema.json",
  "begin": "OpenRun",
  "globals": {
    "debug": false,
    "logConfig": {
      "level": "INFO",
      "file": "log/quick_search.log"
    }
  },
  "jobs": {
    "OpenRun": {
      "type": "Input",
      "description": "打开运行对话框",
      "input": {
        "type": "Keyboard",
        "keyboard": {
          "keys": ["win", "r"],
          "duration": 0,
          "sep_time": 50
        }
      },
      "next": "TypeBrowser",
      "delay": {
        "post": 500
      }
    },
    "TypeBrowser": {
      "type": "Input", 
      "description": "输入浏览器命令",
      "input": {
        "type": "Text",
        "text": {
          "text": "chrome",
          "duration": 200
        }
      },
      "next": "PressEnter",
      "delay": {
        "post": 300
      }
    },
    "PressEnter": {
      "type": "Input",
      "description": "按回车执行",
      "input": {
        "type": "Keyboard", 
        "keyboard": {
          "keys": ["enter"],
          "duration": 0
        }
      }
    }
  }
}
```

#### 3. 带条件分支的宏 (`macros/screenshot.json`)

```json
{
  "$schema": "../src/ThirdParty/RecognizerFramework/workflow/schema/generated.schema.json",
  "begin": "TakeScreenshot",
  "globals": {
    "debug": true
  },
  "jobs": {
    "TakeScreenshot": {
      "type": "Input",
      "description": "使用系统截图工具",
      "input": {
        "type": "Keyboard",
        "keyboard": {
          "keys": ["win", "shift", "s"],
          "duration": 0,
          "sep_time": 50
        }
      },
      "next": {
        "success": "LogSuccess",
        "failure": "LogFailure"
      }
    },
    "LogSuccess": {
      "type": "System",
      "description": "记录成功日志",
      "system": {
        "type": "Log",
        "log": {
          "message": "截图工具启动成功",
          "levels": ["INFO"]
        }
      }
    },
    "LogFailure": {
      "type": "System", 
      "description": "记录失败日志",
      "system": {
        "type": "Log",
        "log": {
          "message": "截图工具启动失败",
          "levels": ["ERROR"]
        }
      }
    }
  }
}
```

---

## 最佳实践

1. **命名规范**:
   - 宏名使用 PascalCase（如 `OpenSettings`）
   - 任务名使用描述性名称（如 `TypeBrowser`）
   - 文件名使用 snake_case（如 `open_settings.json`）

2. **文件组织**:
   - 将相关的宏文件放在同一目录下
   - 使用有意义的文件名
   - 为复杂宏添加详细的 description

3. **热键选择**:
   - 避免与系统快捷键冲突
   - 选择容易记忆的组合键
   - 考虑使用不常用的键（如反引号 `grave`）

4. **调试建议**:
   - 开发时设置 `"debug": true`
   - 添加适当的延时避免操作过快
   - 使用日志记录关键步骤

5. **错误处理**:
   - 为关键步骤添加错误分支
   - 使用 `limits` 字段控制重试次数
   - 适当使用 `ignore_errors` 选项

---

## 常见问题

**Q: 如何设置全局热键退出？**

A: KeyboardMonitor 默认使用 `ctrl+c` 作为退出热键，可以在代码中修改。

**Q: 热键不生效怎么办？**

A: 检查以下几点：

- 热键格式是否正确
- 是否与其他程序的热键冲突
- 程序是否以管理员权限运行（某些热键可能需要）

**Q: 如何调试宏执行？**

A: 在工作流文件的 `globals` 中设置 `"debug": true`，并查看日志输出。

**Q: 可以在宏中使用变量吗？**

A: 可以，使用 Calculate 任务类型可以进行变量计算和传递。

**Q: 如何实现延时？**

A: 使用 `delay` 字段设置前置/后置延时，或使用 System 任务的 Delay 类型。

---

更多详细信息请参考：

- [项目结构文档](../develop/Structure.MD)
- [RecognizerFramework 文档](../../src/ThirdParty/RecognizerFramework/docs/manual/JsonField.MD)
