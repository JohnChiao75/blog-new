---
title: Arch Linux 配置教程（续）
date: 2026-04-19 11:49:00
tags: 系统
category: 教程

---



[上一篇文章](https://www.luogu.com.cn/article/4oe52287) 介绍了如何安装 Arch Linux，本篇则聚焦于系统的配置、美化与个性化定制。

:::info{open}
本文所有配置均为可选操作。系统美化与个人审美高度相关，请理性讨论，~~不要在评论区对线~~。
:::

## 前置

### 快捷键的表示方式

Linux 中快捷键使用 **修饰键+字符** 的方式表示。

修饰键是符号，代表按下的 Ctrl, Alt 等，一般 `^` -> `Ctrl`，`!` -> `Alt`。

比如 `^C` 代表 `Ctrl-C`。

有一些软件的快捷键使用 Emacs 表示，即 **修饰键首字母_字符** 表示，如 `C_C` 代表 `Ctrl-C`。

### 软件包的表示方式

在本篇文章中，软件包使用 pkg in repo 的表示方式。

对于 **Core, Extra** 软件包可以用 Pacman、Discover 或 Octopi 安装。

对于 **ArchlinuxCN** 软件包需要安装 archlinuxcn-keyring in ArchlinuxCN 后使用上一行的方式安装（当然，密钥环本身除外，不然就递归了）。

对于 **AUR** 软件包，使用 Yay、Paru 或 Pamac 安装。

对于 **Flathub** 软件包，使用 Flatpak 或者 Discover 安装。

## 系统篇

### 可选内核

Linux 内核提供多个版本可选。`linux` 为官方版本，适用于大多数场景。此外也可选用以下第三方内核：

- `linux-zen`：高性能内核，基于逆向优化，但能耗较高。
- `linux-lts`：功耗较低，但可能与部分软件不兼容。

安装内核后，务必重新执行 `grub-mkconfig` 以刷新启动项。启动时选择“高级选项”即可切换内核。

### TLP 能耗控制

对笔记本用户而言，TLP 可帮助调节能耗设置，较为实用。

安装命令：

```bash
sudo pacman -S tlp tlp-gtk
```

常用配置项举例：

- **CPU → CPU 电压**：超频用的。
  :::warning
  Linux 下没有数值保护机制，请合理调节，~~系统死了别来找我~~。
  :::
- **无线电 → 自动关闭指定网络设备**：休眠时关闭网卡。若合盖时仍需后台任务（如 `sudo pacman -Syu`），建议关闭此功能。

### Timeshift 备份

滚动更新一旦中断可能导致不确定后果（例如内核更新失败可能连带损坏 initramfs 甚至引导项），因此备份在 Arch 中尤为重要。

安装 Timeshift：

```bash
sudo pacman -S timeshift
```

在启动菜单中打开 Timeshift，跟随向导完成设置。一般建议保留 5 个每日备份，其余按需调整。

### 设置休眠

:::warning[注意内存与交换空间大小]
请勿在内存超大的机器上配置休眠。此类机器休眠与唤醒耗时显著，且会带来大量硬盘读写。
:::

打开 Plasma 设置 → 电源 → 使用电池供电时，将“睡眠选项”改为“混合睡眠”。

如需更激进的休眠策略，可启用“睡眠后立即休眠”，但请注意睡眠后将无法运行后台服务。

### Pacman 实用配置

编辑 `/etc/pacman.conf`，取消注释或添加以下行以改善使用体验：

```ini
# 启用并行下载（同时下载 5 个包）
ParallelDownloads = 5
# 启用彩色输出
Color
```
### SSH 远程登录

若需通过局域网或互联网远程管理你的 Arch 机器，SSH 是最常用且安全的方案。

#### 安装与启动

```bash
sudo pacman -S openssh
sudo systemctl enable sshd
sudo systemctl start sshd
```

查看 SSH 服务状态：`sudo systemctl status sshd`

#### 基本连接

在另一台设备（Linux / macOS / Windows WSL 或 PowerShell）上执行：

```bash
ssh 用户名@IP地址
```

例如：`ssh arch@192.168.1.100`

首次连接会提示确认主机指纹，输入 `yes` 后按提示输入密码即可登录。

#### 密钥认证（免密登录）

使用密钥对比密码登录更安全、更方便。

1. **在客户端生成密钥对**（如已有则跳过）：

   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

   一路回车即可，默认保存为 `~/.ssh/id_ed25519`（私钥）和 `~/.ssh/id_ed25519.pub`（公钥）。

2. **将公钥复制到 Arch 机器**：

   ```bash
   ssh-copy-id 用户名@IP地址
   ```

   若 `ssh-copy-id` 不可用，可手动将公钥内容追加到 Arch 上的 `~/.ssh/authorized_keys` 文件中。

3. **测试免密登录**：再次执行 `ssh` 应不再需要密码。

#### 安全配置（可选）

编辑 `/etc/ssh/sshd_config`，建议修改以下内容：

```ini
# 禁止 root 直接登录
PermitRootLogin no

# 仅允许密钥登录（禁用密码登录，前提是已配置好密钥）
PasswordAuthentication no
```

修改后重启服务：`sudo systemctl restart sshd`。若更改了端口，客户端连接时需加上 `-p 端口号`。

#### 常用客户端工具

- Linux / macOS：系统自带 `ssh`
- Windows：PowerShell 或 PuTTY
- 手机：JuiceSSH（Android）、Termius（跨平台）

### 切换会话

在 Arch Linux 中按 ^![F1, F12] （即 Ctrl-Alt-F1 ~ Ctrl-Alt-F12）可以切换会话，默认的会话是 1，SDDM 在会话 2。

比如，在桌面（已登录）可以按 ^!F3 切换到一个纯 tty，原会话会保留，可以用来执行一些耗内存较大的任务，如 npm build 等。

如果你需要在 tty 会话打开桌面环境，运行 `plasmashell`。

### 跨系统传输文件与磁盘空间

如果你使用双系统，那么可能需要跨系统传输文件和空间。

对于 **传输文件**，我们可以开一块 FAT / NTFS 的分区来传输，以 FAT 为例：

首先缩小你的 Btrfs 分区，新增一块 **Linux Filesystem** 分区。

格式化：

```bash
sudo mkfs.fat -F32 /dev/sdXX
```

然后就可以跨系统传输。

对于 **传输磁盘空间**，比较复杂，大致步骤如下：

从其他系统到 Arch：

1. 关闭硬盘加密：如果你开启了如 BitLocker 或 Apple FileVault 等功能，最好先关闭。

2. 打开另一个系统，缩小磁盘，新建一块 **FAT** 空间。

3. 回到 Arch，运行这个命令：

   ```bash
   df -h # 查看刚才开的分区
   sudo btrfs device add /dev/sdXX # 添加到分区
   ```

从 Arch 到其他系统：

1. 首先进入 **Live USB**，打开 `cfdisk`。
2. 选中目标分区，resize 到合适大小。
3. 分出来的分区创建目标系统的文件系统。（Windows：NTFS，macOS：APFS Data，Linux：Linux Filesystem）
4. reboot 到目标系统
   1. 如果你的分区和待扩展分区连续，那么直接进行扩展。（Windows 下“扩展卷”，macOS 下拖动圆点覆盖所有区域）
   2. 如果不连续，可以尝试 resize 中间的分区来移动，但如果中间有 Swap 分区则无法扩展，只能再新建一个分区。

## 终端篇

### Linux 常用命令与终端键位

| 命令   | 操作或解释           | 包            |
| ------ | -------------------- | ------------- |
| cd     | 切换目录             | linux in Core |
| md     | 新建目录             | ^             |
| mv     | 移动或重命名         | ^             |
| cp     | 复制                 | ^             |
| rm     | 删除                 | ^             |
| man    | 查看命令的帮助       | man in Core   |
| cat    | 查看文件内容         | linux in Core |
| vim    | 终端编辑器，编辑文件 | vim in Extra  |
| chsh   | 切换默认 Shell       | linux in Core |
| pacman | 包管理器             | base in Core  |
| curl   | 从网络上下载内容     | curl in Core  |
| pkill  | 停止进程             | base in Core  |

| 键位 | 操作                                       |
| ---- | ------------------------------------------ |
| ^C   | 停止当前任务（SIGTERM 15）                 |
| ^D   | 关闭当前进程，可以用于关闭终端             |
| ^Z   | 挂起当前进程（SIGSTOP 18），使用 `fg` 恢复 |

### 

### 安装 Zsh 与 Oh My Zsh

Oh My Zsh 可安装多种主题，美化提示符。

```bash
sudo pacman -S zsh
chsh -s /usr/bin/zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

在 GitHub 上搜索 `oh-my-zsh theme` 查找主题，并按相应配置步骤安装。

### 实用的 Zsh 插件

插件可极大提升效率。以下两个常用插件可通过 Oh My Zsh 内置管理器安装：

编辑 `~/.zshrc`，找到 `plugins=(git)` 一行，修改为：

```bash
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
```

然后分别安装这两个插件：

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

重新打开终端，即可体验输入时的自动建议与语法高亮。

### Bashrc / Zshrc 配置

Shell 配置文件（`~/.bashrc` 或 `~/.zshrc`）可用于修改命令别名、环境变量等。

以下为个人常用的设置：

- **Askpass sudo**：弹出密码框并显示输入密码（需安装 `ksshaskpass`）。

  ```bash
  alias sudo="SUDO_ASKPASS=ksshaskpass sudo -A"
  ```

- **Pacman 自动提权**：免去每次输入 `sudo pacman` 的麻烦。

  ```bash
  alias pacman="sudo pacman"
  ```

- **简化常用命令**：

  ```bash
  alias ls='ls --color=auto'
  alias ll='ls -alF'
  alias la='ls -A'
  alias grep='grep --color=auto'
  alias update='sudo pacman -Syu'
  ```

- **自动添加文件单位**：

  ```bash
  alias df="df -h"
  ```

通过 `export` 设置环境变量，例如指定 Shell 专用语言：

```bash
export LANG="zh-CN"   # 当全局语言未设为中文时可生效
```

更多配置可按需自行添加。

### 终端模拟器的选择与配置

我自己习惯使用 Kitty（kitty in Extra），可以调整的设置比 Konsole 丰富很多。

进入 Kitty 后会发现这个 tty 没有界面组件，按下 ^Shift-F2 打开配置，配置做了折叠，按下右箭头展开，以下是一些常用配置项：

- 背景颜色和字体：`Appearance.color-scheme`
- 标签栏：`Tabs.tab-side`，我这里选择 `top`
- 快捷键：`Hotkeys`

常用键位：

| 按键（K -> Kitty (Ctrl+Shift)） | 操作或命令         |
| ------------------------------- | ------------------ |
| K-F2                            | 打开配置文件编辑器 |
| K-F3                            | 命令面板           |
| K-T                             | 新标签页           |
| K-Q                             | 关闭标签页         |
| K-N                             | 分屏，新建容器     |
| K-W                             | 关闭容器           |

## 桌面篇

以下以 KDE Plasma 为例，部分配置可能不兼容其他桌面环境，会注明兼容性。

### 字体配置

系统界面字体推荐使用 Google 开发的 **Noto Fonts** 字体包。

```bash
sudo pacman -S noto-fonts noto-fonts-emoji noto-fonts-cjk
```

| 字体名称      | 包名          | 兼容性                                                       |
| ------------- | ------------- | ------------------------------------------------------------ |
| Noto Fonts     | noto-fonts     | UTF-8 Basic，UI 兼容                                         |
| Noto Fonts CJK | noto-fonts-cjk | 可以使用繁体字和生僻字                                       |
| 文泉驿正黑    | wqy-zenhei  | 有良好的 UI 兼容，但对次像素渲染几乎不兼容，一些 LCD 屏幕可能表现异常 |

等宽字体选择众多，如 Jetbrains Mono、Consolas 等。此处以 Monaspace 为例：

```bash
sudo pacman -S monaspace
```

| 字体名称       | 包名           | 兼容性                                  | 连字和 OpenType 特性 |
| -------------- | -------------- | --------------------------------------- | -------------------- |
| Monospace      | Plasma 自带    | 良好                                    | 无                   |
| Hack           | Plasma 自带    | ^                                       | 无                   |
| Jetbrains Mono | jetbrains-mono | ^                                       | 支持连字             |
| Fira Code      | fira-code      | ^                                       | ^                    |
| Monaspace      | monaspace      | 中等，在 tty 环境中可能出现少量显示异常 | 支持连字和纹理修复   |
| Consolas       | consolas       | 良好                                    | 无                   |

在 Plasma 设置 -> 字体 处更换字体和字号。

### 美化 Plasma

Plasma 支持非常精细的调整。以下为各选项的含义：

- **全局主题**：以下各选项的并集。
- **应用程序外观样式**：调整 Qt / GTK 应用内的按钮等控件。
- **Plasma 外观样式**：调整任务栏等组件样式。
- **窗口装饰元素**：调整窗口标题栏按钮。
- **图标**：更改文件图标等。
- **光标**：鼠标指针样式。
- **欢迎屏幕**：调整从 SDDM 进入桌面后的动画效果。

### 其他美化建议

- **壁纸轮换**：前往“设置 → 工作区行为 → 桌面壁纸”，添加多张壁纸并设置切换间隔（如每小时）。
- **Konsole 配色方案**：打开 Konsole，进入设置 → 编辑当前方案，选择“Pro”或“Solarized”，或从 [KDE Store](https://store.kde.org/browse?cat=103&ord=latest) 下载更多配色。
- **Latte Dock**（仅 Plasma）：一个优雅的 Dock，可替代默认面板。安装 `latte-dock` 后，在系统设置中启用并美化。
- **全局菜单**：在面板上添加“全局菜单”小部件，将应用程序菜单整合到顶部栏，以节省空间。

### Grub / SDDM 主题

两者的配置方式类似。

**Grub 主题**：  
访问 [grub-theme - GitHub Topic](https://github.com/topics/grub-theme)（网络加速请自行解决），找到合适的主题下载，使用 `sudo` 运行 `install.sh`。  
然后编辑 `/etc/grub.conf`，修改 `theme` 的值。

**SDDM 主题**：  
访问 [sddm-theme - GitHub Topic](https://github.com/topics/sddm-theme)，下载主题，同样使用 `sudo` 运行 `install.sh`。  
编辑 `/etc/sddm.conf`，修改 `theme` 的值。

## 日常管理篇

本章介绍 Arch Linux 日常使用中的重要注意事项及实用维护技巧。

### 系统更新注意事项

Arch 为滚动发行版，**必须进行完整升级**，不支持部分更新。请始终使用：

```bash
sudo pacman -Syu
```

**禁止**使用 `pacman -Sy` 或单独 `pacman -S <包名>` 而不执行完整升级，否则可能导致依赖冲突或系统不稳定。

建议每周至少更新一次，避免因积压过多更新而产生冲突。

:::error[如果你真的滚挂了]{open}
虽然这种情况较少见，但若在更新安装阶段意外中断，**不要重启，也不要关闭当前终端**。先尝试排查问题，若问题较浅，可再次执行 `pacman -Syu`。  
若已无法执行更新，立即打开 Timeshift 选择一个快照进行恢复。  
若更严重——引导直接崩溃无法进入系统，可尝试手动修复，但更推荐使用 Arch Live USB 启动，执行 `arch-chroot`，然后使用命令行的 Timeshift 恢复。
:::

### Sudo 的安全与便捷配置

`sudo` 是日常提权工具，使用中需注意以下要点。

#### 编辑 sudoers 的正确方法

必须使用 `visudo` 命令，该命令会检查语法错误，防止锁死系统。

```bash
sudo visudo
```

#### 常用配置项

在 `/etc/sudoers` 或 `/etc/sudoers.d/` 下添加文件：

- 允许 `wheel` 组用户执行任何命令（需密码）：

  ```
  %wheel ALL=(ALL:ALL) ALL
  ```

- 允许 `wheel` 组无密码执行 `pacman`（谨慎使用）：

  ```
  %wheel ALL=(ALL:ALL) NOPASSWD: /usr/bin/pacman
  ```

- 设置密码重试次数与超时时间：

  ```
  Defaults passwd_tries=3, timestamp_timeout=5
  ```

  上述配置表示：密码最多输错 3 次；单次成功提权后 5 分钟内再次 `sudo` 不再询问密码。

:::warning
`NOPASSWD` 会降低系统安全性，仅建议在单用户个人电脑上针对特定命令（如 `pacman`）使用，**切勿为 `ALL` 命令设置 `NOPASSWD`**。
:::

#### 安全使用习惯

- **警惕破坏性命令**：执行 `sudo rm -rf`、`sudo dd` 等命令前，务必再三确认路径。一条错误的路径（例如少写一个点）可能导致系统崩溃。

- **谨慎对待一行式安装命令**：尤其包含 `curl ... | sudo bash` 的命令。建议先下载脚本并人工审计：

  ```bash
  curl -fsSL https://example.com/install.sh -o install.sh
  less install.sh          # 或使用 cat / vim 检查
  sudo bash install.sh
  ```

  若脚本中包含 `rm -rf`、`/dev`、`/sys` 等可疑操作，**切勿运行**。

- **小心使用 `sudo !!`**：该快捷方式会以上一条命令为参数加上 `sudo` 执行。若上一条命令是 `rm -rf /*`，后果严重。建议先用 `echo !!` 查看内容，再决定是否执行。

### 清理系统垃圾

长期使用会积累大量无用包和缓存。

- **清理 pacman 缓存**：包文件缓存于 `/var/cache/pacman/pkg/`。使用 `paccache` 可保留最近 3 个版本：

  ```bash
  sudo pacman -S pacman-contrib   # 安装 paccache
  sudo paccache -r                # 保留最近 3 个版本，删除其余
  ```

- **彻底清理（不推荐常规使用）**：`sudo pacman -Scc` 会删除所有缓存包，导致无法降级已安装软件，请谨慎使用。

- **删除孤儿包**：移除不再被任何包依赖的软件包：

  ```bash
  sudo pacman -Rns $(pacman -Qtdq)
  ```

  可将此命令添加到别名中（参见终端篇）。

### 回滚与故障恢复

- **单软件降级**：从 `/var/cache/pacman/pkg/` 中找到旧版本包文件，使用 `pacman -U` 安装：

  ```bash
  sudo pacman -U /var/cache/pacman/pkg/包名-旧版本.pkg.tar.zst
  ```

- **系统整体回滚**：使用 Timeshift（系统篇已安装）从备份还原。建议在每次重大更新前手动创建快照。

- **内核问题恢复**：若更新后无法启动，在 GRUB 启动菜单中选择“高级选项”，使用 `linux-lts` 或其他备用内核启动（参见系统篇），然后修复原内核。

### 日志查看与调试（Journalctl）

- **查看系统日志**：

  ```bash
  journalctl -xe               # 显示最近的错误及详细信息
  journalctl -p 3 -b           # 显示本次启动的所有错误级别日志
  journalctl -u NetworkManager # 查看特定服务的日志
  ```

- **分析启动慢的原因**：

  ```bash
  systemd-analyze blame
  ```

### 其他

- **防火墙**：安装并启用 `ufw` 或 `firewalld`，可在 Plasma 设置中管理防火墙规则。

  ```bash
  sudo pacman -S ufw
  sudo ufw enable
  sudo systemctl enable ufw
  ```

- **SELinux / AppArmor**：Arch 对两者均提供支持，但配置较为复杂。普通桌面用户通常无需额外配置。
