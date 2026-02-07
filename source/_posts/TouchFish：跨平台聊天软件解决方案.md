---
title: TouchFish：跨平台聊天软件解决方案
date: 2026-02-07 21:08:21
tags: TouchFish
category: 工程
---

:::warning[叠甲]{open}
本软件只用于娱乐与学术交流目的，请各位合理使用。
:::

[TouchFish GitHub 仓库](https://github.com/2044-space-elevator/touchfish)

[TouchFish.xin 官网](http://touchfish.xin)

[TouchFish 文档站 by ILS](http://touchfish.ilovescratch.us.ci)

[TF v3 旧版官网](http://bopid.cn/chat)

[官方团队](https://www.luogu.com.cn/team/116912)

## 介绍

TouchFish 是 [@细数繁星](https://www.luogu.com.cn/user/824363) 和开发组成员制作的聊天软件解决方案，有如下特性：

**社区支持**：多种发行版，满足各种需求

**单文件程序**：便携程序，无需安装

**一键部署**：部署简单，适合内网聊天

**跨平台**：桌面端（Windows，macOS，Linux）和移动端[1]（仅 Android）都有

:::warning[LTS Mobile 已停止支持]{open}
TouchFish LTS（长支持版）的 Android 版本已停止支持，请转到 [TouchFish-Astra](https://bgithub.xyz/ILoveScratch2/TouchFish-Astra)
:::

## 下载

[GitHub Release](https://github.com/2044-space-elevator/touchfish/releases)：最新，但可能有网络问题

[镜像站 by ILoveScratch](https://mirror.ilovescratch.us.ci/)：速度快，但仅提供稳定通道

## 快速开始

**以下内容以 LTS CLI 版为准**

### 服务端（作为聊天室主机）

1. 运行程序后，会显示启动界面
2. 按 `Ctrl+C` 直接使用默认配置启动，或按 `Enter` 手动配置
3. 手动配置步骤：
   - 启动类型：输入 `Server` （大小写严格）
   - 服务端地址：输入要绑定的 IP 地址（如 `127.0.0.1`）
   - 端口：输入要监听的端口（如 `8080`）
   - 服务端管理员的用户名：输入房主用户名
   - 最大在线连接数：输入允许的最大用户数（1-128）

### 客户端（作为聊天室用户）

1. 运行程序
2. 按 `Ctrl+C` 直接使用默认配置启动，或按 `Enter` 手动配置
3. 手动配置步骤：
   - 启动类型：输入 `Client` （大小写严格）
   - 服务端地址：输入服务端的 IP 地址或域名
   - 端口：输入服务端的端口
   - 用户名：输入您希望在聊天室中使用的名称

### 界面模式

我们采用类似 Vim 的模式切换来管理 IO 进程

- **输出模式**：显示聊天消息，行首没有符号
- **输入模式**：输入指令，行首有 `>` 符号
- 切换方式：在输出模式下按 `Enter` 进入输入模式，在输入模式下按 `Enter` 或执行指令后返回输出模式

### 发送消息

1. 进入输入模式
2. 输入以下指令之一：
   - `send` + 消息内容：发送公开消息
   - `whisper <用户> <消息>`：发送私聊消息
   - `broadcast <消息>`：发送公告（需要管理员权限）

### 发送文件

1. 进入输入模式
2. 输入以下指令之一：
   - `distribute <文件名>`：发送公开文件
   - `transfer <用户> <文件名>`：发送私有文件

### 常用指令

- `help`：查看帮助文档
- `dashboard`：查看聊天室状态
- `exit`：退出程序
- `flood`：进入简易命令行模式（可直接输入消息发送）

### 管理员功能

如果您的用户状态是 `Admin` 或 `Root`，可以使用以下高级指令：

- `kick <用户>`：踢出用户
- `ban ip add/remove <IP>`：封禁/解封 IP
- `ban words add/remove <词语>`：添加/移除屏蔽词
- `config <参数> <值>`：修改聊天室配置
- `doorman accept/reject <用户>`：审核用户加入请求

## 配置文件

TouchFish 会在当前目录生成以下文件：

- `config.json`：存储程序配置
- `log.ndjson`：存储聊天日志（NDJSON 格式）
- `TouchFishFiles/`：存储接收到的文件

## 获取帮助

在程序内输入 `help` 查看详细帮助

## 联系我们

[TouchFish 团队](https://www.luogu.com.cn/team/116912)

## 附：发行版列表

**这里的大部分发行版都暂不支持 v4 版本，如需使用请前往 [Release](https://github.com/2044-space-elevator/TouchFish/releases) 页面下载旧版本（v3及以前）**

| 版本名称 | 简称 | 主要作者 | 链接 | 对 v1-3 支持 | 语言 | 平台支持 | 特色 | 对 v4 支持
|---------|------|----------|----|-----|------|----------|------|--|
| LTS | TF | @2044-space-elevator, @035966-L3 和其他 LTS 贡献者 | [github](#发行版本生态), [mirror](https://mirror.ilovescratch.us.ci/TouchFish/LTS/) | ✅ | Python | Win, macOS, Linux | 根版本，长期支持 | ✅ |
| Astra | TFA | @ILoveScratch2 | [github](https://github.com/ILoveScratch2/TouchFish-Astra), [mirror](https://mirror.ilovescratch.us.ci/TouchFish/Astra/) | ✅ | Dart | 全平台 (UI) | 最佳发行版之一，现代化 UI | ✅ |
| UI Remake | TFUR | @pztsdy | [github](https://github.com/pztsdy/touchfish_ui_remake), [main-mirror](https://mirror.ilovescratch.us.ci/TouchFish/UI%20Remake/), [update-branch](https://github.com/pztsdy/touchfish_ui_remake/tree/update) | ✅ | Node.JS | Win, macOS*, Linux* | 现代化 UI，Markdown，代码高亮（生命周期已终止~~即停更~~） | ❌ |
| Plus | Plus | @ayf2192538031 | [github](https://github.com/2044-space-elevator/TouchFishPlus), [mirror](https://mirror.ilovescratch.us.ci/TouchFish/Plus%20(%E6%BA%90%E4%BB%A3%E7%A0%81)/) | ❌ | Python | Win*, macOS*, Linux* | 增强功能集 | ❌ |
| Pro | Pro | @BoXueDuoCai | [github](https://github.com/PigeonTechGroup/TouchFishPro), [mirror](https://mirror.ilovescratch.us.ci/TouchFish/Pro%20(%E6%BA%90%E4%BB%A3%E7%A0%81)/) | ✅ | Python | Win*, macOS*, Linux* | Markdown，LaTeX，用户高亮 | ❌ |
| Android | (已废除) | @pztsdy | [github](https://github.com/pztsdy/TouchFish-for-mobile), [mirror](https://mirror.ilovescratch.us.ci/TouchFish/Mobile%20%EF%BC%88%E4%B8%8D%E6%8E%A8%E8%8D%90%EF%BC%89/) | ✅ | Kotlin | Android | 移动端（有使用限制）（已停更） | ❌ |
| More | More | @xx2860 | [gitee](https://gitee.com/xx2870/touchfish_more), [mirror](https://mirror.ilovescratch.us.ci/TouchFish/More(Lite)/) | ✅ | Python | Win*, macOS*, Linux (UI) | 性能优化，镜像站 | ❓^ |

> *注：*  
> 标 \* 的版本可能需要自行编译、直接运行代码或缺少预编译包  
> 标 \^ 的内容因为不在 Github 内，所以数据可能会有差异现象