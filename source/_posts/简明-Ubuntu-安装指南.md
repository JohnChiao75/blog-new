---
title: 简明 Ubuntu 安装指南
date: 2026-02-09 17:00:37
tags: 系统
category: 教程
---

:::info[写在最前]{open}
此文章是基于 https://www.luogu.com.cn/article/ruiiz6b4 的修改和补充，如有错误请指正。
:::

:::info[Changelog（审核看这里）]
2025.12.24: 
  - 修复：修改“安装”一节的结构，符合 Markdown 语法。
  - **修复**：~~ExFAT~~ -> exFAT。
  - **内容**：对于烧录过程，增加了对虚拟机的说明。
  - **排版**：在引导部分使用突出显示而不是方括号。
  - **修复**：修复引导一节的 Markdown 语法错误：在 F12 按键处多打了反引号（~~``F12`~~）。
  - **内容**：对于“姓名”“主机名”“用户名”的区别进行了解释。
  - **内容**：添加关于 Zorin OS 的提示。
  - **内容**：对于安装编译器的命令进行解释。
    
2026.1.3：
  - **排版**：对于全文添加句号和其他标点。

2026.1.8：
  - **内容**：对于 Windows，添加软件启动到引导的方式

**2026.2.3（最近一次更新）**：
  - **内容**：添加关于 macOS 的内容
:::

## 一、准备

### 1. 硬件

你需要如下的硬件：

- 目标机器（实体机或虚拟机）
- U 盘（至少 32 GB，虚拟机不用）

### 2. Ubuntu 镜像

点击 [下载 Ubuntu](https://cn.ubuntu.com/download/desktop) 来下载。

建议下载 LTS 版本（本文以版本 26 为例），比较稳定。

:::info[关于 Zorin OS]
Zorin OS 是一个 Ubuntu 改版，更加接近 Windows 体验，与本文所述安装方式基本相同。
:::

### 3. 磁盘空间

如果你需要使用双系统，请留足至少 25 GB 的**空闲**空间（不要分区！！！）。

**对于 Windows**，进入“磁盘管理”，选中需要安装的分区，点击“压缩卷”，压缩空间

**对于 macOS**：进入“磁盘工具”，选中你的硬盘，点击分区，选择“仍然分区”，分出空间，格式选 `MS-DOS (FAT32)`，弹出的窗口选“继续”

:::warning{open}
macOS 下分区会使整个系统卡死，请确保关闭所有会一直存取硬盘的应用
:::

另外，你可以将你的一些数据分区格式化为 exFAT 来共享文件。

### 4A. 烧录 ISO（对于实体目标机）

用 Rufus 举例（也可以使用 BelenaEtcher）：

1. 下载 Rufus
2. 选择镜像文件
3. 选择你的 U 盘
4. **备份文件**，烧录镜像会格掉整个 U 盘，这是备份 U 盘文件的最后机会
5. 烧录

### 4B. 挂载安装镜像（对于虚拟目标机）

1. 打开虚拟机软件
2. 点击你的目标机
3. 点击设置（对于 VMWare，点击“调整客户机的选项”，对于 VirtualBox，点击“设置”）
4. 找到“光盘”
5. 添加镜像

:::success[下一步]{open}
插入 U 盘到目标机，准备安装。
:::

## 二、安装 Ubuntu

### 启动到引导


#### 软件启动（推荐，Windows）

打开 Windows 设置，打开 `更新和安全 -> 恢复 -> 高级启动 `，点击 `立即重新启动`。

重启后，选择 `选择启动设备`，选择 U 盘，然后进行“选择引导”步骤。

#### 引导菜单（macOS）

如果你使用 macOS，你需要使用诸如 OpenCore（OC）或 rEFInd 的第三方引导，先长按 `Command-R` 重启进入恢复模式，然后在终端运行：

```bash
$ csrutil disable
```

来关闭 SIP，之后安装所需的引导加载器，按住 `Option` 重启，选择 `EFI Boot`，再选择 U 盘

#### 硬件启动（对于通用 PC 设备）

按住 `F12`，按下电源键，这时一般会弹出启动菜单：

```cpp lines=4
Please select boot device

   Windows Boot Manager... // Windows
   你的 U 盘名字 // Ubuntu
   EFI ...
```

:::warning[如果你的电脑没有启动菜单配置]
启动时按住 `F2` 或 `Del`（各品牌主板不同），进入 BIOS，找到 `Boot`，将 U 盘放到最上方，重启（无需按任何按键）即可进入下文的步骤。
:::

选择 U 盘，按下 `Enter`。

#### 选择引导

```boot lines=1-2
   Try or install Ubuntu // 试用或安装 Ubuntu
   Ubuntu (safe graphics) // 如果出现显卡故障，选择此项
   Boot from next volume
   UEFI Firmware Settings
```

选第一个（或第二个），按下 `Enter`。


### 安装过程

1. 选择你的语言：
   
   选择 `中文（简体）` 或你想使用的语言。


2. 你想对 Ubuntu 做什么：

   如果想要试用，选择 `试用 Ubuntu` 否则 `安装 Ubuntu`。

3. 您想如何安装 Ubuntu？

   
   选择 `交互式安装`。

   :::warning[不要使用自动 Windows Boot Manager 安装]
   Ubuntu 自带的分区是灾难性的，后期很难配置，而且有概率因安全启动和 Windows 更新而卡掉引导。
   :::

   如果你需要抹掉之前的系统，选择“擦除硬盘并安装 Ubuntu”，否则选“手动分区”。
   
   如果选择“手动分区”，选择之前配好的空闲空间，点击“更改”，格式化为 ext4，挂载到 `/`，这是 Ubuntu 的系统分区。


   :::info[关于磁盘大小]
   在此页面中，磁盘的大小可能略高于 Windows 中的大小，因为此处的单位是 kB (1000 B)，而 Windows 使用的是 KB 或 KiB (1024 B)。
   :::


5. 选择软件集合


   如果你希望自己安装软件，选择“基本集合”（包含基础工具），否则选择“扩展集合”（包含较多的应用软件，**需要网络连接**）。


6. 设置账户


   - 注意：“姓名”是登录界面上的名字，可以使用空格，安装后可以修改，如 `Farmer John`
   - “主机名”是这台电脑的名字，如 `UbuntuPC`
   - “用户名”是用户目录（`~`）的名字，类似变量名的命名，安装后不能更改，也不能使用空格，如 `User123`

7. 点击“安装”

:::success[下一步]{open}
安装好后拔出 U 盘，重启即可进系统。

对于虚拟机，按照“安装”一节的第 4B 步逆操作即可。
:::

## 三、安装软件的示例：安装和配置 VS Code

### 安装编译器

**此节演示使用包管理器安装软件的步骤**

:::info[Tip: Linux 终端快捷键]{open}
全局快捷键：按 `Ctrl-Alt-T` 打开终端。
:::

在终端输入：

```bash
sudo apt-get update
```

解释：`sudo` 代表提权执行（需要密码），`apt-get` 表示使用 APT 安装软件，`update` 更新软件列表。

```bash
sudo apt-get install build-essential gdb
```

同上，使用 APT 安装 `build-essential` 和 `GDB` 包。

### 安装 VS Code

**此节演示使用安装包安装软件的步骤。**

参见：https://www.luogu.com.cn/article/a594wn3y

可以发现下载的是 deb 安装器，点击“安装”，输入密码即可。

在 Linux 下，你无需配置编译器，请跳过文中的“安装 `GCC`”一节。

## 四、迁移到 Ubuntu：以浏览器为例

**这里以浏览器举例介绍如何跨系统交换文件。**

首先，启动你的除 Ubuntu 之外的系统（如 Windows）。

然后，找到你的浏览器，导出配置到 HTML。

进入“磁盘管理”，挂载 exFAT 分区。

将 HTML 移动到新的 exFAT 硬盘。

最后，重启到 Ubuntu，导入配置，完成！

对于反向操作同理，**注意：Ubuntu 可以访问 NTFS 格式的 Windows 系统分区（如 `C:`），但 Windows 不可以访问 ext4 格式的 Ubuntu 分区（如 `/`），对于 macOS 反之，macOS 使用 APFS，Linux 无法访问**

:::success[成功！]{open}
至此，你已完成 Ubuntu 的安装配置，享受新系统吧！
:::

:::info[提交新内容]{open}
如果你有新的内容，欢迎在评论区补充。
:::