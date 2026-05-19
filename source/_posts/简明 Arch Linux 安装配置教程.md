---
title: 简明 Arch Linux 安装配置教程
date: 2026-02-09 17:00:37
tags: 系统
category: 教程

---

:::info[Changelog（审核看这里）]
最近一次更新：增加大量的空行，改善格式。~~之前快写成史山了~~
:::

**上标说明**：本文在提及安装软件时，会在软件名称后添加上标，以指示该软件包所在的仓库或需要的操作。具体含义如下：

- $^{\texttt{CORE}}$：来自官方核心仓库
- $^{\texttt{EXTRA}}$：来自官方额外仓库
- $^{\texttt{MULTILIB}}$：来自官方 multilib 仓库（32 位支持）
- $^{\texttt{AUR}}$：来自 Arch 用户仓库（需通过 AUR 助手安装）
- $^{\texttt{CN}}$：来自 Arch Linux CN 非官方仓库
- $^{\texttt{REBOOT}}$：需要重启系统
- $^{\texttt{LOGOUT}}$：需要注销当前会话并重新登录

---

## 0. Arch 适合我吗？

Arch Linux 是一个面向有经验的 Linux 用户的滚动发行版。它的特点包括：

- **KISS**（Keep It Simple, Stupid）—— 设计简洁，不添加过多自动化工具，让用户自己掌控系统。
- **滚动更新** —— 一次安装，永久更新，无需重装。
- **极致的定制性** —— 你可以从最基础的系统开始，只安装自己需要的软件。
- **丰富的文档** ——[Arch Wiki](https://wiki.archlinux.org/) 是 Linux 世界最全面的知识库之一。

**Arch 可能适合你，如果：**

- 你有一定的 Linux 基础，或者愿意花时间学习。
- 你喜欢动手配置和优化系统。
- 你需要一个干净、轻量的基础系统来搭建开发环境或服务器。
- 你想深入了解 Linux 的工作原理。

**Arch 可能不适合你，如果：**

- 你是计算机完全新手，期望“开箱即用”的体验。
- 你没有耐心阅读文档或解决问题。
- 你希望系统极其稳定，害怕滚挂（虽然 Arch 滚挂概率不大，但仍需注意更新前查看公告）。

如果你决定尝试，请准备好投入一些时间阅读 Wiki 并动手实践。

---

## 1. 给 Arch 腾出空间

如果你需要安装双系统，请给 Arch 腾出空间，分一个分区（格式随便），大小是你的 Arch 目标大小加上内存（RAM）的大小。

:::warning[如果你使用 macOS]
macOS 在分区时会卡死一段时间，最长可能到达 30 分钟，请关闭所有可能读写硬盘的应用。
:::

## 2. 制作安装介质

1. **下载 ISO** 访问 [Arch Linux 下载页](https://archlinux.org/download/)，选择离你最近的镜像，下载最新的 ISO 文件和相应的签名文件（用于验证，可选）。

2. **验证 ISO（可选）**&#x5BFC;入维护者 PGP 密钥并验证 ISO 的完整性。具体步骤见 [Wiki](https://wiki.archlinux.org/title/Installation_guide#Verify_signature)。

3. **写入 U 盘**

    

   - **Linux/macOS**：使用 `dd` 命令&#x20;
     ```bash
     sudo dd if=/path/to/archlinux-xxxx.xx.xx-x86_64.iso of=/dev/sdX bs=4M status=progress oflag=sync
     ```
     &#x20;其中 `/dev/sdX` 是你的 U 盘设备（注意不是分区，例如 `/dev/sdb`）。
   - **Windows**：推荐使用 [Rufus](https://rufus.ie/)（选择 DD 模式写入）或 [balenaEtcher](https://www.balena.io/etcher/)。

---

## 3. 引导到 USB

将 U 盘插入电脑，重启并从 U 盘启动。不同设备的启动方法：

### PC（传统 BIOS 或 UEFI）

- 开机时按特定键（如 F12、F2、Esc、Del）进入启动菜单，选择 U 盘。
- 如果找不到，可能需要进入 BIOS 设置，禁用 Secure Boot，并将 U 盘设为第一启动项。

### Mac（OpenCore）

如果你使用 OpenCore 引导多系统：

- 将 U 盘插入，重启后在 OpenCore 启动菜单中应该能看到外部 U 盘选项（如“External”或 U 盘名称），选择即可启动。
- 若未出现，可能需要配置 OpenCore 的 `config.plist`，启用 `ScanPolicy` 以允许外部设备启动。

### Mac（rEFInd）

rEFInd 会自动检测可启动介质：

- 插入 U 盘，重启后在 rEFInd 菜单中会出现 Arch Linux 的图标，选择它即可。
- 如果未出现，按 F2 或 Insert 扫描所有驱动器。

### Mac (Native)

如果你不使用任何外置 BootLoader，按照这个步骤配置：

- 如果你使用带有 T2 芯片的 Mac，按住 Command-R 重启，进入恢复环境，选择“启动安全性实用工具”，改为“无安全性”。
- 关闭窗口，打开“终端”，输入：
  ```bash
  csrutil disable
  ```
- 将 U 盘插入，重启后在 OpenCore 启动菜单中应该能看到外部 U 盘选项（如“External”或 U 盘名称），选择即可启动。

### 虚拟机（VM）

- **VirtualBox**：在虚拟机设置中，将 ISO 挂载到光驱，启动时按 F12 选择从光驱启动。
- **VMware**：在虚拟机设置中连接 ISO 文件，启动时按 Esc 选择启动设备。
- **QEMU**：直接使用 `-cdrom /path/to/your/image` 参数启动。

---

## 4. 安装前的准备（禁用服务与连接网络）

进入安装环境后，第一件事是禁用可能干扰后续配置的服务，并确保网络连接。

### 4.1 禁用 `reflector` 服务

ArchISO 中的 `reflector` 服务会自动更新镜像列表，但可能删除有用的源。建议先禁用它：

```bash
systemctl stop reflector
# 可选：查看服务状态确认已禁用
# systemctl status reflector
```

### 4.2 确认 UEFI 模式

```bash
ls /sys/firmware/efi/efivars
```

如果输出了一堆文件名（UEFI 变量），说明已以 UEFI 模式启动。否则，请检查 BIOS 设置。

### 4.3 连接网络

- **有线网络**：通常插上网线后 DHCP 会自动分配 IP。
- **无线网络**：使用 `iwctl` 工具。
  ```bash
  iwctl               # 进入交互式提示符
  device list         # 列出无线网卡，假设为 wlan0
  station wlan0 scan  # 扫描网络
  station wlan0 get-networks  # 查看结果
  station wlan0 connect "SSID"  # 连接，输入密码
  exit
  ```
  &#x20;如果网卡被 `rfkill` 禁用，使用 `rfkill unblock wifi` 解锁。

### 4.4 测试网络连通性

```bash
ping www.bilibili.com
```

Linux 中的 Ping 不会自动停止，按 `^C`（Ctrl+C） 停止。

### 4.5 更新系统时钟

```bash
timedatectl set-ntp true   # 打开网络时间同步
timedatectl status   # 检查状态
```

### 4.6 更换国内镜像源

编辑 `/etc/pacman.d/mirrorlist`，将中国境内的镜像源（如中科大、清华、华为云）放在文件最前面。

```bash
vim /etc/pacman.d/mirrorlist
```

推荐的镜像源：

```
Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch
Server = https://repo.huaweicloud.com/archlinux/$repo/os/$arch
```

---

## 5. 分区

假设你的硬盘是 `/dev/sda`（NVMe 设备可能是 `/dev/nvme0n1`），我们采用 **UEFI + GPT** 分区方案。如果你双系统，注意保留原有 EFI 分区。

使用对新手友好的 `cfdisk` 进行分区：

```bash
cfdisk /dev/sda   # 或 /dev/nvme0n1
```

如果提示选择分区表类型，选择 `gpt`。

你会看到一个交互界面。使用方向键移动，Enter 确认。

如果你使用双系统，你需要删除之前预留的分区。

:::error[三思而后行]{open}
数据无价，请确保你的分区的大小互不相同，以防止删除已有的分区，如果需要更改大小可以重启回其他系统修改。
:::

选中你的预留分区 → `[ Delete ]`，输入 `y` 确定。

按以下顺序创建分区：

1. **创建 EFI 系统分区**（如果已有则跳过）：
   - 选择 `Free space` → `[ New ]`，输入大小（建议 512 MiB \~ 1 GiB），例如 `+1G`。
   - 选择 `[ Type ]`，找到 `EFI System` 并选中。
2. **创建交换分区**：
   - 选择 `Free space` → `[ New ]`，输入大小（通常与内存相当或根据需要，例如 `+4G`）。
   - 选择 `[ Type ]`，找到 `Linux swap` 并选中。
3. **创建 Btrfs 根分区**：
   - 选择剩余空闲空间 → `[ New ]`，使用默认大小（直接回车，占用所有剩余空间）。
   - 类型保持 `Linux filesystem`（默认）。

最终分区布局类似：

```
/dev/sda1   1G   EFI System
/dev/sda2   4G   Linux swap
/dev/sda3   xxxG Linux filesystem
```

选择 `[ Write ]` 写入分区表，输入 `yes` 确认，然后 `[ Quit ]` 退出。

---

## 6. 格式化与挂载（Btrfs + 交换分区）

### 6.1 格式化分区

```bash
# 格式化 EFI 分区（如果双系统请勿执行！！！）
mkfs.fat -F32 /dev/sda1

# 格式化交换分区并启用
mkswap /dev/sda2
swapon /dev/sda2

# 格式化 Btrfs 分区
mkfs.btrfs -f /dev/sda3
```

### 6.2 创建 Btrfs 子卷

挂载 Btrfs 分区，创建子卷（名称保持 `@` 和 `@home` 以便与快照工具兼容）：

```bash
mount /dev/sda3 /mnt
cd /mnt
btrfs subvolume create @
btrfs subvolume create @home
# 可选：创建用于快照的子卷
# btrfs subvolume create @snapshots
cd /
umount /mnt
```

### 6.3 挂载子卷

```bash
# 挂载根子卷
mount -o compress=zstd,subvol=@ /dev/sda3 /mnt

# 创建必要目录
mkdir -p /mnt/{boot,home}

# 挂载 EFI 分区
mount /dev/sda1 /mnt/boot

# 挂载 home 子卷
mount -o compress=zstd,subvol=@home /dev/sda3 /mnt/home
```

> `compress=zstd` 启用透明压缩，可节省空间并提升某些场景下的读写速度。

---

## 7. 安装基础系统

使用 `pacstrap` 安装基础包、内核、固件和开发工具：

```bash
pacstrap /mnt base base-devel linux linux-firmware
```

- `base`$^{\texttt{CORE}}$：基础软件包。
- `base-devel`$^{\texttt{CORE}}$：开发工具包（编译 AUR 软件包必备）。
- `linux`$^{\texttt{CORE}}$：当前最新内核，也可用 `linux-lts` 长期支持版。
- `linux-firmware`$^{\texttt{CORE}}$：各类硬件固件。

---

## 8. 配置基础系统

### 8.1 生成 fstab

```bash
genfstab -U /mnt >> /mnt/etc/fstab
```

### 8.2 Chroot 到新系统

```bash
arch-chroot /mnt
```

### 8.3 安装基础工具

你可以根据自己的喜好选择文本编辑器。本教程以 Vim 为例。

```bash
pacman -S vim nano sudo networkmanager man-db man-pages bash-completion
```

- `vim`$^{\texttt{EXTRA}}$ / `nano`$^{\texttt{CORE}}$：文本编辑器。
- `sudo`$^{\texttt{CORE}}$：权限提升工具。
- `networkmanager`$^{\texttt{EXTRA}}$：网络管理服务。
- `man-db`$^{\texttt{CORE}}$ / `man-pages`$^{\texttt{CORE}}$：帮助文档。
- `bash-completion`$^{\texttt{EXTRA}}$：命令行补全增强。

:::success{open}
恭喜！你首次在新系统中使用 Pacman 安装软件，Linux 的软件基本可以通过包管理安装（~~不用翻网页~~）。
:::

### 8.4 设置时区

```bash
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
hwclock --systohc
```

**提示：有一些时区地点是等价的（UTC+8），但不同的国家 / 地区配置会影响时间格式等。**

### 8.5 本地化

编辑 `/etc/locale.gen`，取消 `en_US.UTF-8 UTF-8` 和其他所需本地化选项（如 `zh_CN.UTF-8 UTF-8`）的注释。

```bash
vim /etc/locale.gen
locale-gen
```

创建 `/etc/locale.conf` 文件，由于我们没有安装中文字体，所以先使用英文：

```bash
echo "LANG=en_US.UTF-8" > /etc/locale.conf
```

### 8.6 配置主机名

创建 `/etc/hostname` 文件，写入你的主机名（例如 `myarch`）：

```bash
echo "myarch" > /etc/hostname
```

同时编辑 `/etc/hosts`：

```bash
vim /etc/hosts
```

添加以下内容：

```cpp lines=3
127.0.0.1   localhost
::1         localhost
127.0.1.1   myarch.localdomain myarch
```

注意把 myarch 换成实际的主机名。

### 8.7 设置 root 密码

```bash
passwd
```

密码可能不会显示，这是正常的。

### 8.8 创建普通用户并配置 sudo

创建用户（例如 `yourusername`）并加入 `wheel` 组：

```bash
useradd -m -G wheel -s /bin/bash yourusername
passwd yourusername
```

配置 `sudo`。使用 `visudo` 命令安全地编辑 sudoers 文件，因为编辑器配置没有生效，所以需要指定为 Vim（或 nano 等）：

```bash
EDITOR=vim visudo
```

找到并取消注释以下行，以允许 `wheel` 组用户执行任何命令：

```
%wheel ALL=(ALL:ALL) ALL
```

**安全加强**：为防止用户通过 `sudo` 滥用 `passwd` 命令修改 root 或其他用户的密码，可以在该行后面添加排除规则：

```
%wheel ALL=(ALL:ALL) ALL, !/usr/bin/passwd, !/usr/bin/passwd *
```

这样 `wheel` 组成员将无法通过 `sudo` 执行 `passwd` 命令（但仍可使用普通 `passwd` 修改自己的密码）。

---

## 9. 安装引导程序

### 9.1 安装 GRUB

```bash
pacman -S grub efibootmgr os-prober
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
```

- `--efi-directory=/boot` 指向 EFI 分区挂载点。

生成 GRUB 配置文件：

```bash
grub-mkconfig -o /boot/grub/grub.cfg
```

### 9.2 安装微码（可选但推荐）

根据你的 CPU 厂商安装：

- Intel：
  ```bash
  pacman -S intel-ucode
  ```
- AMD：
  ```bash
  pacman -S amd-ucode
  ```

微码会在生成 GRUB 配置时自动加入引导项。

---

## 10. 进入新系统

退出 chroot 环境，卸载所有分区，然后重启：

```bash
exit                    # 退出 chroot
umount -R /mnt          # 递归卸载
reboot                  # 重启
```

重启时记得拔掉 U 盘，进入新系统后使用你创建的普通用户登录。

---

## 11. 安装桌面环境（KDE Plasma on Wayland）

登录后，首先启动网络服务并连接网络：

```bash
sudo systemctl enable --now NetworkManager
```

连接 Wi-Fi 可使用 `nmtui` 或系统托盘的网络图标。

### 11.1 安装 Plasma 和 Wayland 会话

```bash
sudo pacman -S plasma plasma-wayland-session
```

- `plasma`$^{\texttt{EXTRA}}$：KDE Plasma 桌面元包，包含基本组件和应用程序。
- `plasma-wayland-session`$^{\texttt{EXTRA}}$：提供 Wayland 会话的支持。

### 11.2 安装显示管理器（SDDM）

SDDM$^{\texttt{EXTRA}}$ 是 Plasma 推荐的登录管理器：

```bash
sudo pacman -S sddm
sudo systemctl enable sddm
```

### 11.3 安装必要的 Wayland 组件

为了更好的 Wayland 兼容性（特别是屏幕共享、截图等），安装 `xdg-desktop-portal-kde`$^{\texttt{EXTRA}}$：

```bash
sudo pacman -S xdg-desktop-portal-kde
```

### 11.4 配置环境变量（针对 Wayland）

创建 `/etc/environment` 文件（如果不存在），添加以下内容以支持输入法等：

```bash
sudo vim /etc/environment
```

添加：

```
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
SDL_IM_MODULE=fcitx
```

> 对于 Wayland，`~/.xprofile` 不会被读取，因此需要将环境变量放在 `/etc/environment` 或 `~/.config/environment.d/*.conf` 中。这里使用全局配置以确保所有程序都能继承。

### 11.5 重启进入桌面

```bash
reboot   # $^{\texttt{REBOOT}}$
```

重启后 SDDM 会启动。在登录界面的会话选择器中，选择 **"Plasma (Wayland)"**，然后输入密码即可进入 Wayland 会话。

---

## 12. 安装常用软件和编程环境

进入桌面后，打开终端（Konsole），开始安装日常软件、编辑器和编程语言支持，并配置更多软件源。

### 12.1 基础功能包

```bash
# 声音固件
sudo pacman -S sof-firmware alsa-firmware alsa-ucm-conf

# NTFS 支持
sudo pacman -S ntfs-3g

# 常用网络和多媒体软件
sudo pacman -S firefox gwenview ark
```

- `firefox`$^{\texttt{EXTRA}}$：网页浏览器。
- `dolphin`$^{\texttt{EXTRA}}$：文件管理器。
- `konsole`$^{\texttt{EXTRA}}$：终端模拟器。
- `gwenview`$^{\texttt{EXTRA}}$：图片查看器。
- `ark`$^{\texttt{EXTRA}}$：压缩文件管理。

### 12.2 编辑器和编程语言支持

#### 编辑器

- **Kate**（已随 `plasma` 安装，亦可单独安装）$^{\texttt{EXTRA}}$
  ```bash
  sudo pacman -S kate   # 若未安装
  ```
- **Visual Studio Code**（官方开源版本）$^{\texttt{EXTRA}}$
  ```bash
  sudo pacman -S code
  ```
- **VSCodium**（社区驱动、不含遥测的 VS Code 分支）$^{\texttt{AUR}}$
  ```bash
  yay -S vscodium-bin   # 需先配置 AUR 助手（见 12.3）
  ```
- **Sublime Text**（商业软件，有试用版）$^{\texttt{AUR}}$
  ```bash
  yay -S sublime-text-4
  ```

#### 编程语言支持

- **GCC**（GNU 编译器套件，通常已随 `base-devel` 安装）$^{\texttt{CORE}}$
  ```bash
  # 若未安装：
  sudo pacman -S gcc
  ```
- **Python**（解释器）$^{\texttt{EXTRA}}$
  ```bash
  sudo pacman -S python python-pip   # pip 为包管理器
  ```
- **JDK**（Java 开发工具包，选择所需版本）$^{\texttt{EXTRA}}$
  ```bash
  # 最新版本
  sudo pacman -S jdk-openjdk
  # 或指定版本，如 JDK 17
  sudo pacman -S jdk17-openjdk
  ```

### 12.3 配置软件源与 AUR 助手

#### 开启 32 位支持库（multilib）

编辑 `/etc/pacman.conf`，找到 `[multilib]` 部分，去掉其前后两行的注释。

```bash
sudo vim /etc/pacman.conf
```

#### 添加 Arch Linux CN 仓库

在 `/etc/pacman.conf` 文件末尾添加以下内容（选择一个镜像）：

```
[archlinuxcn]
Server = https://mirrors.ustc.edu.cn/archlinuxcn/$arch
# Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch
```

#### 安装密钥环和 AUR 助手

更新系统并安装必要软件包：

```bash
sudo pacman -Syyu   # 刷新数据库并更新
sudo pacman -S archlinuxcn-keyring yay
```

如果安装 `archlinuxcn-keyring` 时报密钥信任错误，执行以下命令后重试：

```bash
sudo pacman-key --lsign-key "farseerfc@archlinux.org"
```

#### 检查家目录

确保用户家目录下的常见目录（如 `Downloads`、`Documents` 等）已创建，若没有则运行：

```bash
xdg-user-dirs-update
```

---

## 13. 配置中文字体与输入法（fcitx5）

本节提供两种输入方案，你可以根据自己的喜好选择：

- **方案一：fcitx5 自带拼音**（简单易用，适合大多数用户）
- **方案二：Rime + 雾凇拼音词库**（高度可定制，词库丰富，适合进阶用户）

### 13.1 安装中文字体（通用）

无论选择哪种输入法，都需要先安装中文字体：

```bash
sudo pacman -S noto-fonts-cjk wqy-microhei wqy-zenhei
```

- `noto-fonts-cjk`$^{\texttt{EXTRA}}$：Google 的 CJK 字体，覆盖较全。
- `wqy-microhei`$^{\texttt{EXTRA}}$ / `wqy-zenhei`$^{\texttt{EXTRA}}$：文泉驿中文字体。

### 13.2 安装输入法框架

两种方案都基于 fcitx5，首先安装核心框架：

```bash
sudo pacman -S fcitx5-im fcitx5-configtool
```

- `fcitx5-im`$^{\texttt{EXTRA}}$：输入法基础包组。
- `fcitx5-configtool`$^{\texttt{EXTRA}}$：图形配置工具。

### 13.3 配置输入法环境变量

由于我们使用 Wayland，需要确保环境变量正确设置。我们在前面第 11.4 节已经将配置写入了 `/etc/environment`，此处可以验证一下：

```bash
cat /etc/environment
```

应该包含以下内容：

```
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
SDL_IM_MODULE=fcitx
```

### 13.4 选择并配置输入法

#### 方案一：使用 fcitx5 自带拼音

如果你希望快速上手，可以直接使用 fcitx5 自带的拼音输入法。

1. **安装拼音引擎 $^{\texttt{LOGOUT}}$**：
   ```bash
   sudo pacman -S fcitx5-chinese-addons
   ```

2. **图形化配置**：
   - 打开“系统设置” > “区域设置” > “输入法”。
   - 如果提示“没有输入法正在运行”，点击“运行 Fcitx”。
   - 点击“添加输入法”，找到“简体中文”下的“Pinyin”并添加。

#### 方案二：使用 Rime + 雾凇拼音词库（推荐进阶用户）

Rime（中州韵）是一款强大的输入法引擎，配合雾凇拼音词库可以获得更丰富的词库和更好的输入体验。

1. **安装 Rime 输入法引擎**：
   ```bash
   sudo pacman -S fcitx5-rime
   ```

2. **安装雾凇拼音词库**：
   ```bash
   yay -S rime-ice
   ```
   > &#x20;雾凇拼音是目前非常活跃的 Rime 词库项目，拥有庞大的词库和良好的维护。

3. **创建 Rime 用户配置目录**：
   ```bash
   mkdir -p ~/.local/share/fcitx5/rime
   ```

4. **配置雾凇拼音为默认方案**：
   创建并编辑 `~/.local/share/fcitx5/rime/default.custom.yaml`：
   ```bash
   vim ~/.local/share/fcitx5/rime/default.custom.yaml
   ```
   &#x20;输入以下内容：
   ```yaml
   patch:
     # 仅使用「雾凇拼音」的默认配置，配置此行即可
     __include: rime_ice_suggestion:/
     # 以下根据自己所需自行定义
     __patch:
       menu/page_size: 5   # 每页候选词个数，可自定义
   ```
   &#x20;保存并退出。

5. **添加 Rime 输入法到系统**：
   - 打开“系统设置” > “区域设置” > “输入法”。
   - 点击“运行 Fcitx”（如果尚未运行）。
   - 点击“添加输入法”，找到“汉语”下的“中州韵 (Rime)”并添加。
   - 如果你不需要其他输入法，可以移除之前的 Pinyin。

6. **重新部署 Rime**：
   配置完成后，需要重新部署 Rime 才能生效。
   - **方法一**：右键点击系统托盘中的输入法图标，选择“重新部署”。
   - **方法二**：在终端中执行：
     ```bash
     fcitx5-remote -r
     ```

> **提示**：Rime 的配置非常灵活，你可以通过修改 `~/.local/share/fcitx5/rime/` 下的各种 `.yaml` 文件来自定义输入行为。更多配置请参考 [Rime 官方文档](https://rime.im/docs/)。

> **Wayland 下的输入法提示**：在某些基于 Chromium 的应用程序（如 VS Code、Electron 应用）中，可能需要添加启动参数 `--enable-features=UseOzonePlatform --ozone-platform=wayland --enable-wayland-ime` 来启用输入法支持。

---

## 14. 显卡驱动

**注意**：虚拟机通常不需要安装显卡驱动。**进行此部分操作前，强烈建议先创建系统快照（如使用 Timeshift），以便在出现问题时回滚。**

### 14.1 集成显卡

#### Intel 核芯显卡

```bash
sudo pacman -S mesa lib32-mesa vulkan-intel lib32-vulkan-intel
```

> 不建议安装 `xf86-video-intel`，使用 Xorg 内置的 `modesetting` 驱动即可。对于 Wayland，mesa 和 vulkan 驱动已足够。

#### AMD 集成显卡

需要先确定你的显卡架构（GCN 版本），再选择驱动。

- **GCN 3 架构及更新**（多数 Ryzen 处理器集显）：安装开源 `AMDGPU` 驱动。
  ```bash
  sudo pacman -S mesa lib32-mesa xf86-video-amdgpu vulkan-radeon lib32-vulkan-radeon
  ```
- **GCN 2 架构及更老**：安装开源 `ATI` 驱动。
  ```bash
  sudo pacman -S mesa lib32-mesa xf86-video-ati 
  ```

### 14.2 独立显卡

#### NVIDIA 独立显卡

- **Turing 架构及更新（GTX 1600 系列 / RTX 系列）**：安装 `nvidia-open` 开源内核模块。
  ```bash
  sudo pacman -S nvidia-open nvidia-settings lib32-nvidia-utils
  ```
- **较新型号（Maxwell 至 Ampere 架构）**：安装闭源驱动 `nvidia`。
  ```bash
  sudo pacman -S nvidia nvidia-settings lib32-nvidia-utils 
  ```
- **GeForce 400 \~ 900 系列（Fermi 至 Maxwell）**：安装 `nvidia-390xx-dkms`$^{\texttt{AUR}}$。
- **更老的显卡**：安装开源驱动 `nouveau`。
  ```bash
  sudo pacman -S mesa lib32-mesa xf86-video-nouveau
  ```

安装 NVIDIA 闭源驱动后，需编辑 `/etc/mkinitcpio.conf`，在 `HOOKS` 行中删除 `kms`，然后重新生成镜像：

```bash
sudo vim /etc/mkinitcpio.conf   # 删除 kms
sudo mkinitcpio -P
```

#### AMD 独立显卡

参考上文“AMD 集成显卡”部分，根据架构选择 `AMDGPU` 或 `ATI` 驱动。

### 14.3 双显卡（集显 + 独显）

#### NVIDIA Optimus 技术（NVIDIA 独显 + Intel/AMD 集显）

推荐使用 `optimus-manager` 进行切换。

1. 安装驱动：同时安装集显驱动（见 14.1）和对应的 NVIDIA 驱动（见 14.2，建议使用 `nvidia` 或 `nvidia-open`）。
2. 安装 `optimus-manager` 及其图形前端：
   ```bash
   yay -S optimus-manager optimus-manager-qt
   ```
3. 启用服务并重启：
   ```bash
   sudo systemctl enable optimus-manager.service
   reboot
   ```
4. 重启后，在系统托盘的 `optimus-manager-qt` 图标中可以选择“仅集显”、“仅独显”或“动态切换”模式。

**动态切换模式使用说明**：
在“动态切换”模式下，默认使用集显。若需为特定程序启用独显，有两种方法：

- 使用 `prime-run` 命令（需安装 `nvidia-prime`$^{\texttt{EXTRA}}$）：
  ```bash
  prime-run steam   # 以独显运行 Steam
  ```
- 手动添加环境变量：
  ```bash
  __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia __VK_LAYER_NV_optimus=NVIDIA_only 程序名
  ```

#### AMD 双显卡（AMD 独显 + AMD 集显）

使用 PRIME 技术的 `DRI_PRIME` 环境变量进行切换。

- 测试集显性能：`glmark2`
- 测试独显性能：`DRI_PRIME=1 glmark2`
- 以独显运行程序：`DRI_PRIME=1 程序名` 例如：`DRI_PRIME=1 steam`

---

## 15 配置与美化

参见我的[另一篇文章](https://www.luogu.com.cn/article/6x15menx)

## 16. 版权声明与致谢

### 16.1 版权声明

本作品（《Arch Linux 安装与配置教程》）采用 **知识共享署名 - 相同方式共享 4.0 国际许可协议（CC BY-SA 4.0）**&#x8FDB;行许可。

您可以自由地：

- **共享** — 在任何媒介以任何形式复制、发行本作品
- **演绎** — 修改、转换或以本作品为基础进行创作

惟须遵守下列条件：

- **署名** — 您必须给出适当的署名，提供指向本许可协议的链接，同时标明是否对原始作品作了修改。您可以用任何合理的方式来署名，但是不得以任何方式暗示许可人为您或您的使用背书。
- **相同方式共享** — 如果您再混合、转换或者基于本作品进行创作，您必须基于与原先许可相同的许可协议来分发您的贡献。

完整的许可协议文本请见：<https://creativecommons.org/licenses/by-sa/4.0/legalcode.zh-Hans>

### 16.2 致谢

本教程在编写过程中，参考并整合了大量来&#x81EA;**[《archlinux 简明指南》](https://arch.icekylin.online/)**&#x7684;内容。该指南由 icekylin 等贡献者维护，是一份优秀的中文 Arch Linux 安装指南，对本教程的完善起到了重要的参考作用。特此感谢原作团队的卓越工作！

原作采用 **CC BY-SA 4.0** 许可，本教程遵循相同的许可协议。

---

**Happy Arching!**