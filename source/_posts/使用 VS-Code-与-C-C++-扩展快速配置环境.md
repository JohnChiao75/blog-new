---
title: 使用 VS Code 与 C/C++ 扩展快速配置环境
date: 2026-02-07 21:07:08
tags:
  - VS Code
category: 教程
author: John Chiao
---

本文是 VS Code 和 C/C++ 扩展的安装与配置教程，如有不足，请在评论区指正

::::info

**本文有部分内容引用了 [`OI Wiki`](https://oi-wiki.org)，遵照原作者的要求，本文使用 `CC-SA-BY-NC 2.0` 协议共享**[^1]

::::

## 推荐：交互式安装

[CodeStart 安装器](https://icc.gt.tc/vscode)

可以使用安装器来安装 VS Code，请在编程语言选择处选择“C/C++”，安装好后从“安装 `GCC`”一节开始自行配置编译器

## 安装 Visual Studio Code

### Windows 10 及以上/macOS 11+

[**`下载`**](https://code.visualstudio.com)

### 如果你使用 Windows 7/8/8.1

点击上面的链接后点击 `Releases`，找到 1.70.2，这是最后支持 Windows 7/8/8.1 的版本，前往发布页面下载

---

### 配置中文

安装好后，点击左侧活动栏的“扩展”，搜索`Chinese(Simplified)`，点击`安装`。安装好后按`Ctrl+Shift+P`，搜索`Display`，选择`Configure Display Language`，切换为中文

## 安装 `C/C++` 扩展

安装好 VS Code 后，重复上一步，安装`C/C++`。

## 安装 `GCC`

[安装引导 - OI Wiki](https://oi-wiki.org/tools/compiler/#gcc)

注：Windows 最好使用 TDM-GCC 的离线安装版，MinGW 可能会出现问题

## 配置环境

新建一个目录，这将是代码的存放位置。

在 VS Code 中选择`文件 -> 打开文件夹`，打开刚才新建的文件夹。

### 自动配置（推荐）

1. 在 VS Code 中新建一份 C++ 代码文件，按照 C++ 语法写入一些内容，保存并按下 `F5`，进入调试模式。
2. 如果出现了`选择调试器`的提示，选择 `C++ (GDB/LLDB)`
3. 在`选择配置`中，`G++` 选择 `g++.exe - 生成和调试活动文件`。

### 手动配置

在此目录中新建一个文件夹，名为 `.vscode`。

#### 调试器（运行代码）

在 VS Code 中新建 `.vscode/launch.json`，代码如下：

```javascript
{
    "version": "0.2.0",
    "configurations": [
      {
        "name": "C/C++ 调试", // 配置名称
        "type": "cppdbg", // 类型，仅限 cppdbg 即 CPP DEBUG
        "request": "launch",
        "program": "${fileDirname}\\${fileBasenameNoExtension}.exe", // 目标程序，即编译后的二进制程序
        "args": [],
        "stopAtEntry": false, // 是否在开始前打断点
        "cwd": "你的 MinGW 路径\\bin",
        "environment": [],
        "externalConsole": false, // 是否产生控制台窗口，如果设为 False 则在编辑器下方调试
        "MIMode": "gdb",
        "miDebuggerPath": "gdb",
        "setupCommands": [
          {
            "description": "为 gdb 启用整齐打印",
            "text": "-enable-pretty-printing",
            "ignoreFailures": true
          },
          {
            "description": "将反汇编风格设置为 Intel",
            "text": "-gdb-set disassembly-flavor intel",
            "ignoreFailures": true
            // VS Code 中的“反汇编”是一个类似 Dev_C++ 中 CPU 窗口的功能，用于查看汇编代码
          }
        ],
        "preLaunchTask": "C/C++: gcc.exe 生成活动文件"
      }
    ]
}
```

至此，调试器的部分已经写好，现在链接 `GCC`,也就是 `C/C++: gcc.exe 生成活动文件` 的任务

#### 编译器

同上，新建 `.vscode/tasks.json`

```javascript
{
    "tasks": [
        {
            "type": "cppbuild",
            "label": "C/C++: gcc.exe 生成活动文件",
            "command": "你的 MinGW 路径\\bin/gcc.exe",
            "args": [
                "-fdiagnostics-color=always",
                // 添加你需要的参数，如 "-O2"，结尾加逗号
                "-g", // 允许调试
                "${file}",
                "-o",
                "${fileDirname}\\${fileBasenameNoExtension}.exe" // 这条命令会处理文件名，如：a.cpp -> a.exe
            ],
            "options": {
                "cwd": "你的 MinGW 路径\\bin"
            },
            "problemMatcher": [
                "$gcc" // 按照 GCC 标准识别异常
            ],
            "group": {
                "kind": "build", // 生成
                "isDefault": true // 默认
            },
            "detail": "调试器生成的任务。"
        }
    ],
    "version": "2.0.0"
}
```

#### 自动显示异常（InteliSense）

新建 `.vscode/c_cpp_properties.json`：

```javascript
{
    "configurations": [
        {
            "name": "Win32",
            "includePath": [
                "${workspaceFolder}/**"
            ],
            "defines": [
                "_DEBUG",
                "UNICODE",
                "_UNICODE"
            ],
            "compilerPath": "你的 MinGW 路径\\bin/gcc.exe",
            "cppStandard": "c++11", // 你使用的 C++ 标准
            "intelliSenseMode": "windows-gcc-x64", // 或者你的平台
        }
    ],
    "version": 4
}
```

---

### 检查

当你看到这里，恭喜你！完成了 `C/C++` 的配置，现在你的目录应该是这样

- 工作区目录
  - `.vscode`
    - `c_cpp_properties.json`
    - `launch.json`
    - `tasks.json`
    - `settings.json` (有可能没有)
  - `其他文件`

## 书写程序

按 `Ctrl + N`，点击 `选择语言`，点击 `C `或 `C++`，编写程序。

此时状态栏右侧应该是此状态

:::align{right}

| 行/列 | 空格/制表符长度 | UTF-8 | CRLF | { }C++ | Win32 |
| ----: | --------------: | ----: | ---: | -----: | ----: |

::::

按 `Ctrl + Shift + B` 开始编译，编译完成会显示

```
生成已成功完成。
 *  终端将被任务重用，按任意键关闭。
```

按 `F5` 编译并运行，在 VS Code 中，运行与调试的方法相同

开始编程之旅吧！

## 调试你的代码

与 Dev-C++ 不同，在 VS Code 中，通过点击行号左侧的区间来设置/取消断点，类似这样：

```cpp lines=7-7
#include <bits/stdc++.h>
using namespace std;

int main()
{
  	// Some Code...
●	for (int i = 1; i <= n; i++) // 这是断点
  	{
  		// Some Code...
    }
    // Some Code...
    return 0;
}
```

添加好断点后，按下`F5`开始调试，此时代码上方会出现浮动工具栏：

::::align{center}

![](https://cdn.luogu.com.cn/upload/image_hosting/v389awm9.png)

这是浮动工具栏按钮的解释：

| (移动工具栏) | 跳过(continue) | 下一步(next) | 单步进入 | 单步跳出 | 重新开始 | 暂停/停止 |
| :----------: | :------------: | :----------: | :------: | :------: | :------: | :-------: |

::::

此时，`调试`主菜单会自动展开，如果没有，就点击左侧的调试按钮（开始调试后会显示蓝色角标）

在“调试”主菜单中，可以进行以下操作：

- 监视：添加查看，修改变量
- 调用堆栈：查看函数调用轨迹，在调试搜索算法或递归时有用
- 断点：设置断点的条件或设置异常处理

在调试模式中，编辑器将以黄色底色显示下一步将要执行的代码。

此时就可以进行单步调试了

## GitHub Copilot（仅练习或开发）

::::error[慎用 AI 工具]{open}

**在目前的官方 OI/XCPC 比赛中禁止使用生成式 AI**，AI 工具仅可以在平常练习时和开发时使用

AI 有可能输出有错误/不自洽的代码，请检查正确性

::::

在新版本的 VS Code 中内置有 GitHub Copilot，可以生成和检查代码

### 登录或注册 GitHub

如果你没有 `GitHub`，你可以点击 [`GitHub`](https://github.com) 注册一个

::::warning{open}
关于 2FA 的内容，参见 [`此专栏`](https://www.luogu.com.cn/article/x8af46mn) 中 GitHub 一节
::::

打开 VS Code，点击标题栏右侧的 `Copilot` 按钮，右侧会打开一个侧栏，登录 GitHub 后即可使用

### Copilot Chat/Edit

`Copilot Chat` 是默认模式，用于生成代码

`Copilot Edit` 用于在整个项目中更改，点击侧栏标题栏的第二个按钮来切换

## 使用 CPH 自动评测

CPH (Competitive Programming Helper) 是一个 VS Code 插件，用于自动进行数据拉取和评测，以下是使用教程：

:::warning[注意安装正确的版本]{open}
CPH 有大量的第三方版本，这里建议安装官方版（即最上面的，带蓝勾的版本）
:::

:::info[关于 CPH-NG]{open}
CPH-NG 是一个重写后的 CPH，拥有现代 UI，更多评测特性和对排器，但兼容性略差，如果设备支持可以使用 CPH-NG 来代替 CPH
:::

### 安装 CPH

点击左侧活动栏的“扩展”，搜索`CPH`，点击`安装`

**注意安装官方版本**

### 安装 CC

打开 [`Crxsoso`](https://crxsoso.com)，搜索 `Companion`，安装到浏览器

#### 特殊：如果你使用新版本浏览器

在新版的浏览器中，安装可能无法自动进行，打开扩展页面，打开 `开发者模式`，此时在下载目录下将 `crx` 文件拖入即可

### 配置 CPH

回到 VS Code 打开设置，搜索 `CPH`，找到默认语言，选择 `C` 或 `C++` 即可

### 拉取测例和评测

在 OJ 中找到一道题，点击扩展栏中绿色加号图标，这会跳转至 VS Code，然后创建一个与题目同名的文件

这时左侧会显示测例，点击 `Run All` 评测

### 参加比赛

在进行中的比赛的题目列表中，点击扩展栏中绿色加号图标，这会跳转至 VS Code，然后开始初始化比赛，等待所有文件创建完成后，点开第一道题，开始吧！

**特别鸣谢**

[^1]: [`OI Wiki`](https://oi-wiki.org): 提供 GCC 和 Git 安装引导
