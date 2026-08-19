---
title: 简明 Arch Linux 安装配置教程
date: 2026-02-09 17:00:37
tags: 系统
category: 教程
---
**上标说明**：本文在提及安装软件时，会在软件名称后添加上标，以指示该软件包所在的仓库或需要的操作。具体含义如下：

- $^{\texttt{CORE}}$：来自官方核心仓库
- $^{\texttt{EXTRA}}$：来自官方额外仓库
- $^{\texttt{MULTILIB}}$：来自官方 multilib 仓库（32 位支持）
- $^{\texttt{AUR}}$：来自 Arch 用户仓库（需通过 AUR 助手安装）
- $^{\texttt{CN}}$：来自 Arch Linux CN 非官方仓库
- $^{\texttt{REBOOT}}$：需要重启系统
- $^{\texttt{LOGOUT}}$：需要注销当前会话并重新登录

**快捷键的表示方式**：Linux 中快捷键使用 `修饰键+字符` 的方式表示。修饰键是符号，代表按下的 Ctrl、Alt 等，一般 `^` → Ctrl，`!` → Alt。比如 `^C` 代表 `Ctrl-C`。有一些软件的快捷键使用 Emacs 表示，即 `修饰键首字母_字符` 表示，如 `C_C` 代表 `Ctrl-C`。

---

## Arch 适合我吗？

Arch Linux 是一个面向有经验的 Linux 用户的滚动发行版。它的特点包括：

- **KISS**（Keep It Simple, Stupid）—— 设计简洁，不添加过多自动化工具，让用户自己掌控系统。
- **滚动更新** —— 一次安装，永久更新，无需重装。
- **极致的定制性** —— 你可以从最基础的系统开始，只安装自己需要的软件。
- **丰富的文档** ——[ArchWiki](https://wiki.archlinux.org/) 是 Linux 世界最全面的知识库之一。

> 许多 Linux 发行版都试图变得更加“用户友好”，Arch Linux 则一直是，且永远会是“以用户为中心”。本发行版是为了满足贡献者的需求，而不是为了吸引尽可能多的用户。
> 
> Arch Linux 适用于乐于自己动手的用户，因为他们往往更愿意花时间阅读文档，解决自己的问题。
> :::align{right}
> ——ArchWiki
> :::

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


## 给 Arch 腾出空间

> 预计耗时：10 分钟（若已有空闲分区则忽略）

如果你需要安装双系统，请给 Arch 腾出空间，分一个分区（格式随便），大小是你的 Arch 目标大小加上内存（RAM）的大小。

{% callout type=warning title="如果你使用 macOS" %}
macOS 在分区时会卡死一段时间，最长可能到达 30 分钟，请关闭所有可能读写硬盘的应用。
{% endcallout %}

## 制作安装介质

> 预计耗时：5–10 分钟（取决于下载速度）

1. **下载 ISO** 访问 [Arch Linux 下载页](https://archlinux.org/download/)，选择离你最近的镜像，下载最新的 ISO 文件和相应的签名文件（用于验证，可选）。

2. **验证 ISO（可选）** 镜像站中一般会存放 SHA256 校验和与 GPG 签名，对于 sha256 使用 `sha256sum` 等校验，对于 GPG 可以使用 Gpg4win 或 `pacman-key`。

3. **写入 U 盘**

   - **Linux/macOS**：使用 `dd` 命令。
     ```bash
     sudo dd if=/path/to/archlinux-xxxx.xx.xx-x86_64.iso of=/dev/sdX status=progress
     ```
     其中 `/dev/sdX` 是你的 U 盘设备（注意不是分区，例如 `/dev/sdb`）。
   - **Windows**：推荐使用 [Rufus](https://rufus.ie/)（选择 DD 模式写入）或 [balenaEtcher](https://www.balena.io/etcher/）。

## 选择安装方式

> 预计耗时：2 分钟（阅读）

在开始实际操作之前，你需要决定如何安装 Arch Linux。目前主要有两种方式：**手动安装**和**自动化脚本安装**。

**手动安装**

这是本教程所采用的方式，也是官方推荐的方式。你将一步步执行所有命令，理解每个步骤的作用。

优点：
- 充分了解系统的组成和配置，便于日后维护和故障排除。
- 可根据自己的硬件和需求灵活调整分区方案、文件系统、软件包等。
- 掌握 Arch 的基本操作，为后续使用打下坚实基础。

缺点：
- 耗时较长，需要耐心和一定的 Linux 基础。
- 容易因操作失误导致安装失败。

**自动化脚本安装**

社区中存在一些一键安装脚本，如 `arch-install` 或通过 `curl -fsSL https://helloarch.netlify.app/inst.sh | sh` 等方式运行。它们能快速完成安装。

优点：
- 快速、省事，适合重复安装或应急场景。

缺点：
- 脚本是“黑盒”，你无法知道它具体修改了哪些配置，一旦出现故障，难以自行修复。
- 无法适应个人定制需求，例如特定的分区布局、文件系统选择、桌面环境偏好等。
- 滚动更新后若出现问题（俗称“滚挂”），由于你不了解系统底层，恢复难度极高。

**建议**：

如果你是第一次接触 Arch Linux，**强烈建议选择手动安装**。虽然过程稍显繁琐，但这是学习 Arch 的最佳途径。通过手动安装，你会了解分区表、文件系统、引导程序、网络配置等核心概念，这些知识会在今后的使用中为你提供巨大帮助。脚本安装虽然快捷，但会让你错失学习机会，且一旦系统出现问题，你可能束手无策。

如果你已有丰富经验，且仅需快速部署，可以使用脚本，但本教程不提供脚本安装的指导。

## 引导到 USB

> 预计耗时：2 分钟（启动与选择）

将 U 盘插入电脑，重启并从 U 盘启动。不同设备的启动方法：

**PC（传统 BIOS 或 UEFI）**

- 开机时按特定键（如 F12、F2、Esc、Del）进入启动菜单，选择 U 盘。
- 如果找不到，可能需要进入 BIOS 设置，禁用 Secure Boot，并将 U 盘设为第一启动项。

**Mac（OpenCore）**

如果你使用 OpenCore 引导多系统：

- 将 U 盘插入，重启后在 OpenCore 启动菜单中应该能看到外部 U 盘选项（如“External”或 U 盘名称），选择即可启动。
- 若未出现，可能需要配置 OpenCore 的 `config.plist`，启用 `ScanPolicy` 以允许外部设备启动。

**Mac（rEFInd）**

rEFInd 会自动检测可启动介质：

- 插入 U 盘，重启后在 rEFInd 菜单中会出现 Arch Linux 的图标，选择它即可。
- 如果未出现，按 F2 或 Insert 扫描所有驱动器。

**Mac（Native）**

如果你不使用任何外置 BootLoader，按照这个步骤配置：

- 如果你使用带有 T2 芯片的 Mac，按住 Command-R 重启，进入恢复环境，选择“工具 -> 启动安全性实用工具”，改为“无安全性”。
- 关闭窗口，打开“工具 -> 终端”，输入：
  ```bash
  csrutil disable
  ```
- 将 U 盘插入，重启后按住 Alt，在启动菜单中应该能看到外部 U 盘选项（如“External”或 U 盘名称），选择即可启动。

**虚拟机（VM）**

- **VirtualBox**：在虚拟机设置中，将 ISO 挂载到光驱，启动时按 F12 选择从光驱启动。
- **VMware**：在虚拟机设置中连接 ISO 文件，启动时按 Esc 选择启动设备。
- **QEMU**：直接使用 `-cdrom /path/to/your/image` 参数启动。

## 安装前的准备（禁用 reflector 与连接网络）

> 预计耗时：5 分钟（网络连接可能稍久）

进入安装环境后，第一件事是禁用可能干扰后续配置的服务，并确保网络连接。

### 禁用 `reflector` 服务

ArchISO 中的 `reflector` 服务会自动更新镜像列表，但可能删除有用的源。建议先禁用它：

```bash
systemctl stop reflector
```
- `systemctl`：控制 systemd 系统和服务管理器的命令。
- `stop`：立即停止指定的服务单元。
- `reflector`：要停止的服务名称。

```bash
systemctl status reflector
```
- `status`：查看指定服务的当前运行状态（可选，用于确认是否已停止）。

### 确认 UEFI 模式

```bash
ls /sys/firmware/efi/efivars
```
- `ls`：列出目录内容。
- `/sys/firmware/efi/efivars`：该路径存在且非空，则说明当前以 UEFI 模式启动；否则为 BIOS 模式。

### 连接网络

**这不是可选的，Arch Live ISO 仅含可运行在 U 盘的系统，安装 Arch 必须下载软件包。**

**有线网络**：通常插上网线后 DHCP 会自动分配 IP，无需额外命令。

**无线网络**：使用 `iwctl` 工具。

```bash
iwctl
```
- `iwctl`：进入无线网络配置的交互式命令行工具。

在 `iwctl` 交互环境中输入以下命令（每行一条）：

```bash
device list
```
- `device list`：列出所有无线网卡设备，记下设备名（如 `wlan0`）。

```bash
station wlan0 scan
```
- `station`：指定要操作的无线网卡设备。
- `wlan0`：替换为你的实际设备名。
- `scan`：扫描可用的无线网络。

```bash
station wlan0 get-networks
```
- `get-networks`：显示扫描到的无线网络列表。

```bash
station wlan0 connect "SSID"
```
- `connect`：连接指定的无线网络，将 `SSID` 替换为实际网络名称，回车后输入密码。

```bash
exit
```
- `exit`：退出 `iwctl` 交互环境。

如果网卡被 `rfkill` 禁用，使用：

```bash
rfkill unblock wifi
```
- `rfkill`：管理无线设备软锁的工具。
- `unblock`：解除阻塞。
- `wifi`：指定无线设备类型。

### 测试网络连通性

```bash
ping www.archlinux.org
```
- `ping`：发送 ICMP 回显请求以测试网络连通性。  
  Linux 中的 ping 不会自动停止，按 `^C`（Ctrl+C）停止。

### 更新系统时钟

```bash
timedatectl set-ntp true
```
- `timedatectl`：控制系统时间和日期。
- `set-ntp`：启用或禁用网络时间同步。
- `true`：将 NTP 设为真（开启）

```bash
timedatectl status
```
- `status`：显示当前时间、时区及 NTP 同步状态。

### 更换国内镜像源

编辑 `/etc/pacman.d/mirrorlist`，将中国境内的镜像源（如中科大、清华、华为云）放在文件最前面。

```bash
vim /etc/pacman.d/mirrorlist
```
- `vim`：文本编辑器，请自行查找使用方法。  
  你也可以使用 `nano` 等其他编辑器。

推荐的镜像源：

```
Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch
Server = https://repo.huaweicloud.com/archlinux/$repo/os/$arch
```

---

## 分区

> 预计耗时：10 分钟（使用 cfdisk 操作）

{% callout type=error title="三思而后行" %}
数据无价，请确保你的分区和硬盘的大小互不相同，以防止删除已有的分区和硬盘，如果需要更改大小可以重启回其他系统修改。
{% endcallout %}

假设你的硬盘是 `/dev/sdX`（NVMe 设备可能是 `/dev/nvme0nX`），我们采用 **UEFI + GPT** 分区方案。如果你双系统，注意保留原有 EFI 分区。

使用对新手友好的 `cfdisk` 进行分区：

```bash
cfdisk /dev/sdX
```
- `cfdisk`：基于鼠标/键盘的磁盘分区工具。
- `/dev/sdX`：目标磁盘设备（若为 NVMe 则改为 `/dev/nvme0nX`）。

如果提示选择分区表类型，选择 `gpt`。

你会看到一个交互界面。使用方向键移动，Enter 确认。

如果你使用双系统，你需要删除之前预留的分区。

选中你的预留分区 → `[ Delete ]`，输入 `y` 确定。

按以下顺序创建分区：

1. **创建 EFI 系统分区**（如果已有则跳过）：
   - 选择 `Free space` → `[ New ]`，输入大小（建议 512 MiB \~ 1 GiB），例如 `1G`。
   - 选择 `[ Type ]`，找到 `EFI System` （通常在列表顶部）并选中。
2. **创建交换分区**：
   - 选择 `Free space` → `[ New ]`，输入大小（通常与内存相当或根据需要，例如 `4G`）。
   - 选择 `[ Type ]`，找到 `Linux swap` 并选中。
3. **创建 Btrfs 根分区**：
   - 选择剩余空闲空间 → `[ New ]`，使用默认大小（直接回车，占用所有剩余空间）。
   - 类型保持 `Linux`（默认）。

最终分区布局类似：

```
/dev/sdX1   1G   EFI System
/dev/sdX2   4G   Linux swap
/dev/sdX3   xxxG Linux
```

选择 `[ Write ]` 写入分区表，输入 `yes` 确认，然后 `[ Quit ]` 退出。

---

## 格式化与挂载（Btrfs + 交换分区）

> 预计耗时：5 分钟

### 格式化分区

```bash
mkfs.fat -F32 /dev/sdX1
```
- `mkfs.fat`：在设备上创建 FAT 文件系统。
- `-F32`：指定 FAT 版本为 32 位（即 FAT32）。
- `/dev/sdX1`：要格式化的 EFI 分区设备。  
  **注意**：如果双系统且已有 EFI 分区，**请勿执行此命令**，否则会破坏原有引导。

```bash
mkswap /dev/sdX2
```
- `mkswap`：在设备上创建交换分区（swap）。
- `/dev/sdX2`：交换分区设备。

```bash
swapon /dev/sdX2
```
- `swapon`：启用指定的交换分区或交换文件。
- `/dev/sdX2`：要启用的交换设备。

```bash
mkfs.btrfs -f /dev/sdX3
```
- `mkfs.btrfs`：在设备上创建 Btrfs 文件系统。
- `-f`：强制覆盖已有的文件系统。
- `/dev/sdX3`：Btrfs 根分区设备。

### 创建 Btrfs 子卷

挂载 Btrfs 分区，创建子卷（名称保持 `@` 和 `@home` 以便与快照工具兼容）：

```bash
mount /dev/sdX3 /mnt
```
- `mount`：将设备挂载到指定目录。
- `/dev/sdX3`：要挂载的 Btrfs 分区。
- `/mnt`：挂载点（临时根目录）。

```bash
cd /mnt
```
- `cd`：切换当前工作目录到 `/mnt`。

```bash
btrfs subvolume create @
```
- `btrfs subvolume create`：在 Btrfs 文件系统中创建子卷。
- `@`：子卷名称（通常用于根目录）。

```bash
btrfs subvolume create @home
```
- `@home`：子卷名称（通常用于 `/home`）。

```bash
cd /
```
- 返回根目录。

```bash
umount /mnt
```
- `umount`：卸载已挂载的设备。

### 挂载子卷

```bash
mount -o compress=zstd,subvol=@ /dev/sdX3 /mnt
```
- `-o`：挂载选项。
- `compress=zstd`：启用 zstd 透明压缩，节省空间并提升读写速度。
- `subvol=@`：指定要挂载的子卷为 `@`。
- `/dev/sdX3`：Btrfs 分区。
- `/mnt`：挂载点。

```bash
mkdir -p /mnt/{boot,home}
```
- `mkdir -p`：创建目录，`-p` 确保父目录存在。
- `/mnt/{boot,home}`：花括号展开，同时创建 `/mnt/boot` 和 `/mnt/home`。

```bash
mount /dev/sdX1 /mnt/boot
```
- 挂载 EFI 分区到 `/mnt/boot`。

```bash
mount -o compress=zstd,subvol=@home /dev/sdX3 /mnt/home
```
- 挂载 `@home` 子卷到 `/mnt/home`，同样启用压缩。

---

## 安装基础系统

> 预计耗时：20–30 分钟（主要取决于网络速度）

使用 `pacstrap` 安装基础包、内核、固件和开发工具：

```bash
pacstrap /mnt base base-devel linux linux-firmware
```
- `pacstrap`：在指定的挂载点（新系统根目录）安装 Arch Linux 基础包组。
- `/mnt`：目标系统挂载点。
- `base`$^{\texttt{CORE}}$：基础软件包（必须）。
- `base-devel`$^{\texttt{CORE}}$：开发工具包（编译 AUR 软件包必备）。
- `linux`$^{\texttt{CORE}}$：当前最新内核，也可用 `linux-lts` 长期支持版。
- `linux-firmware`$^{\texttt{CORE}}$：各类硬件固件。

---

## 配置基础系统

> 预计耗时：15 分钟（时区、本地化、用户等）

### 生成 fstab

```bash
genfstab -U /mnt >> /mnt/etc/fstab
```
- `genfstab`：根据当前挂载情况生成 fstab 文件。
- `-U`：使用分区的 UUID 作为标识。
- `/mnt`：目标系统的挂载点。
- `>>`：将输出追加到 `/mnt/etc/fstab` 文件中。

### Chroot 到新系统

```bash
arch-chroot /mnt
```
- `arch-chroot`：进入新系统的 chroot 环境，使后续操作在新系统中执行。

### 安装基础工具

你可以根据自己的喜好选择文本编辑器。本教程以 Vim 为例。

```bash
pacman -S vim sudo networkmanager man-db man-pages bash-completion
```
- `pacman -S`：从仓库安装指定软件包。
- `vim`$^{\texttt{EXTRA}}$：文本编辑器（亦可选 `nano`）。
- `sudo`$^{\texttt{CORE}}$：权限提升工具。
- `networkmanager`$^{\texttt{EXTRA}}$：网络管理服务。
- `man-db`$^{\texttt{CORE}}$：手册页索引数据库。
- `man-pages`$^{\texttt{CORE}}$：系统手册页内容。
- `bash-completion`$^{\texttt{EXTRA}}$：命令行补全增强。

{% callout type=info %}
恭喜！你首次在新系统中使用 Pacman 安装软件，到这里，Arch 基础系统已安装完毕。
{% endcallout %}

### 设置时区

```bash
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```
- `ln -sf`：创建符号链接，`-s` 为软链接，`-f` 强制覆盖已存在文件。
- `/usr/share/zoneinfo/Asia/Shanghai`：时区文件（东八区）。
- `/etc/localtime`：系统本地时间链接。

```bash
hwclock --systohc
```
- `hwclock`：访问硬件时钟。
- `--systohc`：将系统时间写入硬件时钟（使硬件时间与系统时间同步）。

### 本地化

编辑 `/etc/locale.gen`，取消 `en_US.UTF-8 UTF-8` 和其他所需本地化选项（如 `zh_CN.UTF-8 UTF-8`）的注释。


```bash
vim /etc/locale.gen
```
- 编辑 locale 生成配置文件。

{% callout type=info title="Protip" %}
在 Vim 命令模式按下 `/` 来查找文本。
{% endcallout %}

```bash
locale-gen
```
- `locale-gen`：根据 `/etc/locale.gen` 生成本地化数据库。

创建 `/etc/locale.conf` 文件，由于我们没有安装中文字体，所以先使用英文：

```bash
echo "LANG=en_US.UTF-8" > /etc/locale.conf
```
- `echo`：输出字符串。
- `>`：重定向到文件（覆盖写入）。
- `LANG=en_US.UTF-8`：设置系统语言为英文 UTF-8。

### 配置主机名

创建 `/etc/hostname` 文件，写入你的主机名（例如 `myarch`）：

```bash
echo "myarch" > /etc/hostname
```

同时编辑 `/etc/hosts`：

```bash
vim /etc/hosts
```
添加以下内容：

```
127.0.0.1   localhost
::1         localhost
127.0.1.1   myarch.localdomain myarch
```
注意把 myarch 换成实际的主机名。

### 设置 root 密码

```bash
passwd
```
- `passwd`：设置当前用户（root）的密码。密码不会显示，这是正常的。

### 创建普通用户并配置 sudo

创建用户（例如 `yourusername`）并加入 `wheel` 组：

```bash
useradd -m -G wheel -s /bin/bash yourusername
```
- `useradd`：创建新用户。
- `-m`：创建用户家目录。
- `-G wheel`：将用户附加到 `wheel` 组（该组通常用于 sudo 授权）。
- `-s /bin/bash`：指定默认 Shell 为 Bash。
- `yourusername`：替换为实际用户名。

```bash
passwd yourusername
```
- 设置该用户的密码。

配置 `sudo`。使用 `visudo` 命令安全地编辑 sudoers 文件：

```bash
EDITOR=vim visudo
```
- `EDITOR=vim`：临时设置环境变量，指定 `visudo` 使用 Vim 作为编辑器。
- `visudo`：安全编辑 `/etc/sudoers` 文件，会进行语法检查。

找到并取消注释以下行，以允许 `wheel` 组用户执行任何命令：

```
%wheel ALL=(ALL:ALL) ALL
```

**安全加强**：为防止用户通过 `sudo` 滥用 `passwd` 命令修改 root 或其他用户的密码，可以在该行后面添加排除规则：

```
%wheel ALL=(ALL:ALL) ALL, !/usr/bin/passwd, !/usr/bin/passwd *
```

## 安装引导程序

> 预计耗时：5 分钟

### 安装 GRUB

```bash
pacman -S grub efibootmgr os-prober
```
- `grub`$^{\texttt{EXTRA}}$：GRUB 引导程序。
- `efibootmgr`$^{\texttt{CORE}}$：管理 UEFI 启动项的工具。
- `os-prober`$^{\texttt{EXTRA}}$：检测其他操作系统的工具（双系统需要）。

```bash
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
```
- `grub-install`：将 GRUB 安装到指定位置。
- `--target=x86_64-efi`：指定目标系统类型为 64 位 UEFI。
- `--efi-directory=/boot`：指定 EFI 分区挂载点。
- `--bootloader-id=GRUB`：在 UEFI 启动项中的名称。

生成 GRUB 配置文件：

```bash
grub-mkconfig -o /boot/grub/grub.cfg
```
- `grub-mkconfig`：生成 GRUB 配置文件。
- `-o /boot/grub/grub.cfg`：输出配置文件到指定路径。

### 安装微码（可选但推荐）

根据你的 CPU 厂商安装：

- Intel：

```bash
pacman -S intel-ucode
```
- `intel-ucode`$^{\texttt{EXTRA}}$：Intel CPU 微码更新包。

- AMD：

```bash
pacman -S amd-ucode
```
- `amd-ucode`$^{\texttt{EXTRA}}$：AMD CPU 微码更新包。

微码会在生成 GRUB 配置时自动加入引导项。


## 进入新系统

> 预计耗时：2 分钟（重启）

退出 chroot 环境，卸载所有分区，然后重启：

```bash
exit
```
- `exit`：退出当前 chroot 环境（回到 Live 环境的 shell）。

```bash
umount -R /mnt
```
- `umount -R`：递归卸载 `/mnt` 下的所有挂载点。

```bash
swapoff /dev/sdX2
```
- `swapoff`：关闭交换分区。

```bash
reboot
```
- `reboot`：重启系统。

重启时记得拔掉 U 盘，进入新系统后使用你创建的普通用户登录。


## 安装桌面环境（KDE Plasma on Wayland）

> 预计耗时：15–30 分钟（下载大量软件包）

登录后，首先启动网络服务并连接网络：

```bash
sudo systemctl enable --now NetworkManager
```
- `sudo`：以 root 权限执行（首次出现，解释：提权执行命令）。
- `systemctl enable --now`：启用服务并立即启动。
- `NetworkManager`：网络管理服务。

连接 Wi-Fi 可使用 `nmtui` 或系统托盘的网络图标。

### 安装 Plasma 和 Wayland 会话

```bash
sudo pacman -S plasma-meta plasma-wayland-session
```
- `plasma-meta`$^{\texttt{EXTRA}}$：KDE Plasma 桌面元包。
- `plasma-wayland-session`$^{\texttt{EXTRA}}$：提供 Wayland 会话支持。

### 安装显示管理器（SDDM）$^{\texttt{REBOOT}}$

SDDM $^{\texttt{EXTRA}}$ 是 Plasma 推荐的登录管理器：

```bash
sudo pacman -S sddm
```
- `sddm`$^{\texttt{EXTRA}}$：Simple Desktop Display Manager，简单桌面显示管理器。

```bash
sudo systemctl enable sddm
```
- `enable`：设置服务开机自启。

### 安装必要的 Wayland 组件

为了更好的 Wayland 兼容性（特别是屏幕共享、截图等），安装 `xdg-desktop-portal-kde`$^{\texttt{EXTRA}}$：

```bash
sudo pacman -S xdg-desktop-portal-kde
```
- `xdg-desktop-portal-kde`$^{\texttt{EXTRA}}$：KDE 的桌面门户后端，提供屏幕录制、文件选择等 API。

### 配置环境变量（针对 Wayland）$^{\texttt{LOGOUT}}$

创建 `/etc/environment` 文件（如果不存在），添加以下内容以支持输入法等：

```bash
sudo vim /etc/environment
```
- 编辑全局环境变量文件。

添加：

```
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
SDL_IM_MODULE=fcitx
```

> 对于 Wayland，`~/.xprofile` 不会被读取，因此需要将环境变量放在 `/etc/environment` 或 `~/.config/environment.d/*.conf` 中。这里使用全局配置以确保所有程序都能继承。

### 重启进入桌面

```bash
reboot 
```

重启后 SDDM 会启动。在登录界面的会话选择器中，选择 **"Plasma (Wayland)"**，然后输入密码即可进入 Wayland 会话。


## 安装常用软件和编程环境

> 预计耗时：10–20 分钟（下载软件包）

进入桌面后，打开终端（Konsole），开始安装日常软件、编辑器和编程语言支持，并配置更多软件源。

### 基础功能包

```bash
sudo pacman -S sof-firmware alsa-firmware alsa-ucm-conf
```
- `sof-firmware`$^{\texttt{EXTRA}}$：Sound Open Firmware（音频 DSP 固件）。
- `alsa-firmware`$^{\texttt{EXTRA}}$：ALSA 声卡固件。
- `alsa-ucm-conf`$^{\texttt{EXTRA}}$：ALSA 用例配置文件（支持现代音频设备）。

```bash
sudo pacman -S ntfs-3g
```
- `ntfs-3g`$^{\texttt{EXTRA}}$：读写 NTFS 文件系统的驱动。

```bash
sudo pacman -S firefox gwenview ark
```
- `firefox`$^{\texttt{EXTRA}}$：网页浏览器，也可以使用 `chromium`$^{\texttt{EXTRA}}$，`falkon`$^{\texttt{EXTRA}}$ 等。
- `gwenview`$^{\texttt{EXTRA}}$：图片查看器。
- `ark`$^{\texttt{EXTRA}}$：压缩文件管理器，也可以使用 `nautilus`$^{\texttt{EXTRA}}$。

### 编辑器和编程语言支持

#### 编辑器

```bash
sudo pacman -S kate   # 若未安装（通常已随 plasma 安装）
```
- `kate`$^{\texttt{EXTRA}}$：KDE 高级文本编辑器。

```bash
sudo pacman -S code
```
- `code`$^{\texttt{EXTRA}}$：Visual Studio Code 开源版本。

（VSCodium 和 Sublime Text 可通过 AUR 安装，将在后续章节介绍）

#### 编程语言支持

```bash
sudo pacman -S gcc
```
- `gcc`$^{\texttt{CORE}}$：GNU 编译器套件（通常已随 `base-devel` 安装，若未安装则执行此命令）。

```bash
sudo pacman -S python python-pip
```
- `python`$^{\texttt{EXTRA}}$：Python 解释器。
- `python-pip`$^{\texttt{EXTRA}}$：Python 包管理器。

```bash
sudo pacman -S jdk-openjdk
```
- `jdk-openjdk`$^{\texttt{EXTRA}}$：最新版 OpenJDK 开发工具包（也可指定版本如 `jdk17-openjdk`）。

### 配置软件源与 AUR 助手

#### 开启 32 位支持库（multilib）

编辑 `/etc/pacman.conf`，找到 `[multilib]` 部分，去掉其前后两行的注释。

```bash
sudo vim /etc/pacman.conf
```
- 编辑 Pacman 配置文件。

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
sudo pacman -Syyu
```
- `-Syyu`：刷新软件包数据库（`-yy` 强制刷新）并进行完整系统更新（`-u`）。

```bash
sudo pacman -S archlinuxcn-keyring yay
```
- `archlinuxcn-keyring`$^{\texttt{CN}}$：Arch Linux CN 仓库的 GPG 密钥环。
- `yay`$^{\texttt{CN}}$：AUR 助手（Yet Another Yogurt）。

如果安装 `archlinuxcn-keyring` 时报密钥信任错误，执行以下命令后重试：

```bash
sudo pacman-key --lsign-key "farseerfc@archlinux.org"
```
- `pacman-key`：管理 Pacman 的 GPG 密钥。
- `--lsign-key`：本地签署指定密钥（信任该密钥）。

#### 检查家目录

确保用户家目录下的常见目录（如 `Downloads`、`Documents` 等）已创建，若没有则运行：

```bash
xdg-user-dirs-update
```
- `xdg-user-dirs-update`：根据 `/etc/xdg/user-dirs.defaults` 更新用户常用目录。


## 配置中文字体与输入法（fcitx5）

> 预计耗时：10 分钟（含两种方案选择）

本节提供两种输入方案，你可以根据自己的喜好选择：

- **方案一：fcitx5 自带拼音**（简单易用，适合大多数用户）
- **方案二：Rime + 雾凇拼音词库**（高度可定制，词库丰富，适合进阶用户）

### 安装中文字体（通用）

无论选择哪种输入法，都需要先安装中文字体：

```bash
sudo pacman -S noto-fonts noto-fonts-cjk wqy-microhei wqy-zenhei
```
- `noto-fonts-cjk`$^{\texttt{EXTRA}}$：Google 的字体。
- `noto-fonts-cjk`$^{\texttt{EXTRA}}$：Noto Fonts 的 CJK 字体。
- `wqy-microhei`$^{\texttt{EXTRA}}$：文泉驿微米黑。
- `wqy-zenhei`$^{\texttt{EXTRA}}$：文泉驿正黑。

### 安装输入法框架

两种方案都基于 fcitx5，首先安装核心框架：

```bash
sudo pacman -S fcitx5-im fcitx5-configtool
```
- `fcitx5-im`$^{\texttt{EXTRA}}$：fcitx5 输入法基础包组（含主程序、GTK/Qt 模块等）。
- `fcitx5-configtool`$^{\texttt{EXTRA}}$：图形配置工具。

### 配置输入法环境变量

由于我们使用 Wayland，需要确保环境变量正确设置。我们在前面的章节已经将配置写入了 `/etc/environment`，此处可以验证一下：

```bash
cat /etc/environment
```
- `cat`：查看文件内容。

应该包含以下内容：

```
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
SDL_IM_MODULE=fcitx
```

### 选择并配置输入法

#### 方案一：使用 fcitx5 自带拼音

如果你希望快速上手，可以直接使用 fcitx5 自带的拼音输入法。

```bash
sudo pacman -S fcitx5-chinese-addons
```
- `fcitx5-chinese-addons`$^{\texttt{EXTRA}}$：fcitx5 中文插件（包含拼音、双拼等）。

然后进行图形化配置：
- 打开“系统设置” > “区域设置” > “输入法”。
- 如果提示“没有输入法正在运行”，点击“运行 Fcitx”。
- 点击“添加输入法”，找到“简体中文”下的“Pinyin”并添加。

#### 方案二：使用 Rime + 雾凇拼音词库（推荐进阶用户）

Rime（中州韵）是一款强大的输入法引擎，配合雾凇拼音词库可以获得更丰富的词库和更好的输入体验。

```bash
sudo pacman -S fcitx5-rime rime-ice-git
```
- `fcitx5-rime`$^{\texttt{EXTRA}}$：fcitx5 的 Rime 引擎支持。
- `rime-ice-git`$^{\texttt{CN}}$：雾凇拼音词库。


创建 Rime 用户配置目录：

```bash
mkdir -p ~/.local/share/fcitx5/rime
```
- `mkdir -p`：创建目录（已存在则不报错）。

配置雾凇拼音为默认方案。创建并编辑 `~/.local/share/fcitx5/rime/default.custom.yaml`：

```bash
vim ~/.local/share/fcitx5/rime/default.custom.yaml
```

输入以下内容：

```yaml
patch:
  # 仅使用「雾凇拼音」的默认配置，配置此行即可
  __include: rime_ice_suggestion:/
  # 以下根据自己所需自行定义
  __patch:
    menu/page_size: 5   # 每页候选词个数，可自定义
```

保存并退出。

添加 Rime 输入法到系统：
- 打开“系统设置” > “区域设置” > “输入法”。
- 点击“运行 Fcitx”（如果尚未运行）。
- 点击“添加输入法”，找到“汉语”下的“中州韵 (Rime)”并添加。

重新部署 Rime：

```bash
fcitx5-remote -r
```
- `fcitx5-remote`：向 fcitx5 进程发送控制命令。
- `-r`：重新部署（重新加载配置和词库）。

> **提示**：Rime 的配置非常灵活，你可以通过修改 `~/.local/share/fcitx5/rime/` 下的各种 `.yaml` 文件来自定义输入行为。更多配置请参考 [Rime 官方文档](https://rime.im/docs/)。

> **Wayland 下的输入法提示**：在某些基于 Chromium 的应用程序（如 VS Code、Electron 应用）中，可能需要添加启动参数 `--enable-features=UseOzonePlatform --ozone-platform=wayland --enable-wayland-ime` 来启用输入法支持。

## 显卡驱动

> 预计耗时：10 分钟（根据硬件调整）

**注意**：虚拟机通常不需要安装显卡驱动。**进行此部分操作前，强烈建议先创建系统快照（如使用 Timeshift），以便在出现问题时回滚。**

### 集成显卡

#### Intel 核芯显卡

```bash
sudo pacman -S mesa lib32-mesa vulkan-intel lib32-vulkan-intel
```
- `mesa`$^{\texttt{EXTRA}}$：开源 3D 图形库（OpenGL/Vulkan 实现）。
- `lib32-mesa`$^{\texttt{MULTILIB}}$：32 位 Mesa 库（兼容 32 位应用）。
- `vulkan-intel`$^{\texttt{EXTRA}}$：Intel 显卡的 Vulkan 驱动。
- `lib32-vulkan-intel`$^{\texttt{MULTILIB}}$：32 位 Intel Vulkan 驱动。

> 不建议安装 `xf86-video-intel`，使用 Xorg 内置的 `modesetting` 驱动即可。对于 Wayland，mesa 和 vulkan 驱动已足够。

#### AMD 集成显卡

需要先确定你的显卡架构（GCN 版本），再选择驱动。

- **GCN 3 架构及更新**（多数 Ryzen 处理器集显）：安装开源 `AMDGPU` 驱动。

```bash
sudo pacman -S mesa lib32-mesa xf86-video-amdgpu vulkan-radeon lib32-vulkan-radeon
```
- `xf86-video-amdgpu`$^{\texttt{EXTRA}}$：Xorg 的 AMDGPU 视频驱动。
- `vulkan-radeon`$^{\texttt{EXTRA}}$：AMD 显卡的 Vulkan 驱动（Radeon 系列）。
- `lib32-vulkan-radeon`$^{\texttt{MULTILIB}}$：32 位 AMD Vulkan 驱动。

- **GCN 2 架构及更老**：安装开源 `ATI` 驱动。

```bash
sudo pacman -S mesa lib32-mesa xf86-video-ati
```
- `xf86-video-ati`$^{\texttt{EXTRA}}$：Xorg 的 ATI 视频驱动（旧款 AMD 显卡）。

### 独立显卡

#### NVIDIA 独立显卡

- **Turing 架构及更新（GTX 1600 系列 / RTX 系列）**：安装 `nvidia-open` 开源内核模块。

```bash
sudo pacman -S nvidia-open nvidia-settings lib32-nvidia-utils
```
- `nvidia-open`$^{\texttt{EXTRA}}$：NVIDIA 开源内核模块（Turing+ 架构）。
- `nvidia-settings`$^{\texttt{EXTRA}}$：NVIDIA 控制面板工具。
- `lib32-nvidia-utils`$^{\texttt{MULTILIB}}$：32 位 NVIDIA 工具库。

- **较新型号（Maxwell 至 Ampere 架构）**：安装闭源驱动 `nvidia-580xx-dkms`$^{\texttt{AUR}}$。

```bash
yay -S nvidia-580xx-dkms
```
- `nvidia-580xx-dkms`$^{\texttt{AUR}}$：NVIDIA 580xx 系列闭源驱动（DKMS 版本）。

- **GeForce 400 \~ 900 系列（Fermi 至 Maxwell）**：安装 `nvidia-390xx-dkms`$^{\texttt{AUR}}$。

- **更老的显卡**：安装开源驱动 `nouveau`。

```bash
sudo pacman -S mesa lib32-mesa xf86-video-nouveau
```
- `xf86-video-nouveau`$^{\texttt{EXTRA}}$：NVIDIA 开源驱动（Nouveau）。

安装 NVIDIA 闭源驱动后，需编辑 `/etc/mkinitcpio.conf`，在 `HOOKS` 行中删除 `kms`，然后重新生成镜像：

```bash
sudo vim /etc/mkinitcpio.conf   # 删除 kms
```
- 编辑 mkinitcpio 配置文件，移除 `kms`（内核模式设置）钩子以避免冲突。

```bash
sudo mkinitcpio -P
```
- `mkinitcpio -P`：为所有已安装的内核重新生成 initramfs 镜像。

#### AMD 独立显卡

参考上文“AMD 集成显卡”部分，根据架构选择 `AMDGPU` 或 `ATI` 驱动。

### 双显卡（集显 + 独显）

#### NVIDIA Optimus 技术（NVIDIA 独显 + Intel/AMD 集显）

推荐使用 `optimus-manager` 进行切换。

1. 安装驱动：同时安装集显驱动和对应的 NVIDIA 驱动（建议使用 `nvidia` 或 `nvidia-open`）。
2. 安装 `optimus-manager` 及其图形前端：

```bash
yay -S optimus-manager optimus-manager-qt
```
- `optimus-manager`$^{\texttt{AUR}}$：NVIDIA Optimus 切换工具。
- `optimus-manager-qt`$^{\texttt{AUR}}$：optimus-manager 的 Qt 图形界面。

3. 启用服务并重启：

```bash
sudo systemctl enable optimus-manager.service
```
- 启用 optimus-manager 服务。

```bash
reboot
```

4. 重启后，在系统托盘的 `optimus-manager-qt` 图标中可以选择“仅集显”、“仅独显”或“动态切换”模式。

**动态切换模式使用说明**：
在“动态切换”模式下，默认使用集显。若需为特定程序启用独显，有两种方法：

- 使用 `prime-run` 命令（需安装 `nvidia-prime`$^{\texttt{EXTRA}}$）：

```bash
prime-run steam   # 以独显运行 Steam
```
- `prime-run`：在 NVIDIA 显卡上运行指定程序。

- 手动添加环境变量：

```bash
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia __VK_LAYER_NV_optimus=NVIDIA_only 程序名
```

#### AMD 双显卡（AMD 独显 + AMD 集显）

使用 PRIME 技术的 `DRI_PRIME` 环境变量进行切换。

- 测试集显性能：

```bash
glmark2
```
- `glmark2`$^{\texttt{EXTRA}}$：OpenGL 性能测试工具。

- 测试独显性能：

```bash
DRI_PRIME=1 glmark2
```
- `DRI_PRIME=1`：指定使用第二个 GPU（通常为独显）。

- 以独显运行程序：

```bash
DRI_PRIME=1 程序名
```


## 系统配置与优化

> 预计耗时：20 分钟（含阅读各子项）

本章节涵盖安装后的系统配置、内核管理、能耗控制、备份策略、远程访问等实用内容。所有配置均为可选操作，请根据自身需求选择性执行。

### 可选内核

Linux 内核提供多个版本可选。`linux` 为官方版本，适用于大多数场景。此外也可选用以下第三方内核：

- **linux-zen**：高性能内核，基于逆向优化，但能耗较高。
- **linux-lts**：功耗较低，但可能与部分软件不兼容。
- **linux-hardened**：注重安全性的内核，包含更多加固补丁，适合对安全要求较高的场景。
- **linux-ck**：包含 Con Kolivas 的补丁集，针对桌面交互响应进行优化，在桌面使用场景下可能有更好的手感。

安装内核后，务必重新执行 `grub-mkconfig` 以刷新启动项。启动时选择“高级选项”即可切换内核。

```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

### TLP 能耗控制（笔记本用户）

对笔记本用户而言，TLP 可帮助调节能耗设置，较为实用。

安装命令：

```bash
sudo pacman -S tlp tlp-gtk
```
- `tlp`$^{\texttt{EXTRA}}$：高级电源管理工具。
- `tlp-gtk`$^{\texttt{EXTRA}}$：TLP 的 GTK 图形界面。

**配置文件**：`/etc/tlp.conf`

**常用配置项**：
- CPU 调频策略：`CPU_SCALING_GOVERNOR_ON_AC=performance`（插电时性能优先），`CPU_SCALING_GOVERNOR_ON_BAT=powersave`（电池时节能优先）
- CPU 频率限制：`CPU_SCALING_MIN_FREQ_ON_AC=800000`、`CPU_SCALING_MAX_FREQ_ON_AC=3500000`
- 硬盘电源管理：设置硬盘空闲超时时间
- USB 自动挂起：空闲时自动挂起 USB 设备

**电源模式切换**（需安装 `tlp-pd`）：

```bash
sudo pacman -S tlp-pd
```

安装后可在 KDE/GNOME 的电源管理界面中直接切换“性能”、“平衡”、“节能”模式。

**图形界面**：`tlpui`（GTK）或 `slimbookbattery`（支持 AMD/NVIDIA）。

**启用 TLP 服务前**，建议先屏蔽可能与 TLP 冲突的服务：

```bash
sudo systemctl mask systemd-rfkill.service systemd-rfkill.socket
```

{% callout type=warning %}
Linux 下没有数值保护机制，请合理调节，~~系统死了别来找我~~。
{% endcallout %}

- **无线电** → 自动关闭指定网络设备：休眠时关闭网卡。若合盖时仍需后台任务（如 `sudo pacman -Syu`），建议关闭此功能。

### Timeshift 备份

滚动更新一旦中断可能导致不确定后果（例如内核更新失败可能连带损坏 initramfs 甚至引导项），因此备份在 Arch 中尤为重要。

安装 Timeshift：

```bash
sudo pacman -S timeshift
```
- `timeshift`$^{\texttt{EXTRA}}$：系统快照备份与恢复工具。

**定时备份依赖**：Timeshift 需要 cron 调度器才能自动执行定时快照。安装后需启用 `cronie.service`：

```bash
sudo systemctl enable --now cronie.service
```

若不想使用 cron，可安装 `timeshift-systemd-timer`$^{\texttt{AUR}}$ 替代。

**手动配置快照规则**：也可直接编辑 `/etc/timeshift/timeshift.json`。以下是一个 rsync 模式的配置示例（保留 3 个每周快照，排除缓存目录）：

```json
{
  "backup_device_uuid": "root-partition-UUID",
  "btrfs_mode": "false",
  "schedule_weekly": "true",
  "count_weekly": "3",
  "exclude": [
    "/var/cache/**",
    "/var/tmp/**",
    "+ /home/archie/.config/***",
    "/home/archie/**"
  ]
}
```

**将快照备份到外部设备**：可将快照目录设置在外部硬盘或网络存储上。

**命令行恢复**：通过 `timeshift --restore` 从外部存储恢复快照。

在启动菜单中打开 Timeshift，跟随向导完成设置。一般建议保留 5 个每日备份，其余按需调整。

### 设置休眠

{% callout type=warning title="注意（内存与交换空间大小）" %}
请勿在内存超大的机器上配置休眠。此类机器休眠与唤醒耗时显著，且会带来大量硬盘读写。
{% endcallout %}

打开 Plasma 设置 → 电源 → 使用电池供电时，将“睡眠选项”改为“混合睡眠”。

如需更激进的休眠策略，可启用“睡眠后立即休眠”，但请注意睡眠后将无法运行后台服务。

### Pacman 实用配置

编辑 `/etc/pacman.conf`，取消注释或添加以下行以改善使用体验：

```bash
sudo vim /etc/pacman.conf
```

```ini
# 启用并行下载（同时下载 5 个包）
ParallelDownloads = 5
# 启用彩色输出
Color
# 仅保留已安装包的缓存，删除未安装包的缓存文件
CleanMethod = KeepInstalled
```

`KeepInstalled` 会清理缓存中那些当前系统未安装的软件包 tarball，在节省磁盘空间的同时保留已安装软件的降级能力。

**更新前预览**：

```bash
sudo pacman -Syu --print
```
`--print` 仅显示更新计划而不实际执行，可用于提前评估更新范围和潜在风险。

**忽略特定包更新**：

```bash
sudo pacman -Syu --ignore firefox
```

**安装时跳过已安装的包**：

```bash
sudo pacman -S --needed 包名1 包名2
```

### SSH 远程登录

若需通过局域网或互联网远程管理你的 Arch 机器，SSH 是最常用且安全的方案。

#### 安装与启动

```bash
sudo pacman -S openssh
```
- `openssh`$^{\texttt{CORE}}$：SSH 协议的开源实现（服务端和客户端）。

```bash
sudo systemctl enable sshd
sudo systemctl start sshd
```

查看状态：

```bash
sudo systemctl status sshd
```

#### 基本连接

在另一台设备上执行：

```bash
ssh 用户名@IP地址
```

例如：`ssh arch@192.168.1.100`

首次连接会提示确认主机指纹，输入 `yes` 后按提示输入密码即可登录。

#### 密钥认证（免密登录）

在客户端生成密钥对（如已有则跳过）：

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

将公钥复制到 Arch 机器：

```bash
ssh-copy-id 用户名@IP地址
```

测试免密登录：再次执行 `ssh` 应不再需要密码。

#### 安全配置（可选）

编辑 `/etc/ssh/sshd_config`，建议修改以下内容：

```
PermitRootLogin no
PasswordAuthentication no
# 更换端口（如 2222）
Port 2222
# 禁止空密码登录
PermitEmptyPasswords no
# 限制登录尝试次数
MaxAuthTries 3
# 仅允许特定用户登录
AllowUsers 用户名1 用户名2
```

修改后重启服务：

```bash
sudo systemctl restart sshd
```

若更改了端口，客户端连接时需加上 `-p 端口号`。

**启用 Fail2ban**：自动封禁多次登录失败的 IP。

```bash
sudo pacman -S fail2ban
sudo systemctl enable --now fail2ban
```

#### 常用客户端工具

- **Linux / macOS**：系统自带 `ssh`
- **Windows**：PowerShell 或 PuTTY
- **手机**：JuiceSSH（Android）、Termius（跨平台）

### 切换会话

在 Arch Linux 中按 `^![F1, F12]`（即 `Ctrl-Alt-F1` ~ `Ctrl-Alt-F12`）可以切换会话，默认的会话是 1，SDDM 在会话 2。

比如，在桌面（已登录）可以按 `^!F3` 切换到一个纯 tty，原会话会保留，可以用来执行一些耗内存较大的任务，如 `npm build` 等。

如果你需要在 tty 会话打开桌面环境，运行 `plasmashell`。

### 跨系统传输文件与磁盘空间

如果你使用双系统，那么可能需要跨系统传输文件和空间。

**传输文件**：我们可以开一块 FAT / NTFS 的分区来传输，以 FAT 为例：

首先缩小你的 Btrfs 分区，新增一块 Linux Filesystem 分区。格式化：

```bash
sudo mkfs.fat -F32 /dev/sdXX
```

然后就可以跨系统传输。

**传输磁盘空间**：

- **从其他系统到 Arch**：关闭硬盘加密（如 BitLocker 或 Apple FileVault），打开另一个系统缩小磁盘，新建一块 FAT 空间。回到 Arch，运行：

```bash
df -h                # 查看刚才开的分区
sudo btrfs device add /dev/sdXX   # 添加到分区
```

- **从 Arch 到其他系统**：进入 Live USB，打开 `cfdisk`，选中目标分区 resize 到合适大小，分出来的分区创建目标系统的文件系统（Windows：NTFS；macOS：APFS Data；Linux：Linux Filesystem），然后 `reboot` 到目标系统。如果分区和待扩展分区连续，直接进行扩展；如果不连续，可以尝试 resize 中间的分区来移动，但中间有 Swap 分区则无法扩展，只能再新建一个分区。

### 其他补充

**ZRAM（压缩内存交换）**：对于内存较小的机器，ZRAM 可在内存中划分压缩区域作为交换空间。安装配置工具：

```bash
sudo pacman -S zram-generator
```

创建 `/etc/systemd/zram-generator.conf`：

```ini
[zram0]
zram-size = ram / 2
compression-algorithm = zstd
```

**swappiness 调整**：控制系统在内存充足时使用 swap 的倾向。默认值 60，数值越小越倾向于使用物理内存：

```bash
sudo sysctl vm.swappiness=10
```

永久生效需写入 `/etc/sysctl.d/99-swappiness.conf`：

```
vm.swappiness = 10
```

**SSD TRIM**：对 SSD 硬盘，定期执行 TRIM 可维持写入性能。启用每周自动 TRIM：

```bash
sudo systemctl enable --now fstrim.timer
```

**systemd-oomd**：当系统内存不足时自动杀死占用内存过多的进程，防止系统卡死：

```bash
sudo systemctl enable --now systemd-oomd
```

**加快关机/重启速度**：减少 systemd 服务停止的超时等待时间。编辑 `/etc/systemd/system.conf`：

```ini
DefaultTimeoutStopSec=10s
```


## 终端篇

> 预计耗时：10 分钟（配置 Shell 和插件）

### Linux 常用命令与终端键位

| 命令 | 操作或解释 | 包 |
|---|---|---|
| `cd` | 切换目录 | linux in Core |
| `md` | 新建目录 | - |
| `mv` | 移动或重命名 | - |
| `cp` | 复制 | - |
| `rm` | 删除 | - |
| `man` | 查看命令的帮助 | man in Core |
| `cat` | 查看文件内容 | linux in Core |
| `vim` | 终端编辑器，编辑文件 | vim in Extra |
| `chsh` | 切换默认 Shell | linux in Core |
| `pacman` | 包管理器 | base in Core |
| `curl` | 从网络上下载内容 | curl in Core |
| `pkill` | 停止进程 | base in Core |

**键位**：

| 键位 | 操作 |
|---|---|
| `^C` | 停止当前任务（SIGTERM 15） |
| `^D` | 关闭当前进程，可以用于关闭终端 |
| `^Z` | 挂起当前进程（SIGSTOP 18），使用 `fg` 恢复 |

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

**Askpass sudo**：弹出密码框并显示输入密码（需安装 `ksshaskpass`）。

```bash
alias sudo="SUDO_ASKPASS=ksshaskpass sudo -A"
```

**Pacman 自动提权**：

```bash
alias pacman="sudo pacman"
```

**简化常用命令**：

```bash
alias ls='ls --color=auto'
alias ll='ls -alF'
alias la='ls -A'
alias grep='grep --color=auto'
alias update='sudo pacman -Syu'
```

**自动添加文件单位**：

```bash
alias df="df -h"
```

**通过 `export` 设置环境变量**，例如指定 Shell 专用语言：

```bash
export LANG="zh-CN"   # 当全局语言未设为中文时可生效
```

更多配置可按需自行添加。

### 终端模拟器的选择与配置

我自己习惯使用 Kitty（`kitty`$^{\texttt{EXTRA}}$），可以调整的设置比 Konsole 丰富很多。

进入 Kitty 后会发现这个 tty 没有界面组件，按下 `^Shift-F2` 打开配置编辑器，配置做了折叠，按下右箭头展开。以下是一些常用配置项：

- **背景颜色和字体**：`Appearance.color-scheme`（选择预置配色方案，如 `Catppuccin`、`Tokyo Night`）
- **标签栏**：`Tabs.tab-side`（我这里选择 `top`）
- **快捷键**：`Hotkeys`（可自定义所有按键绑定）

除上述基础项外，Kitty 还支持大量进阶调整，以下为几个实用例子：

- **字体大小与行间距**：在配置中搜索 `font_size`（默认 11.0）和 `adjust_line_height`（可设 `-2` 或 `2` 来微调行距）。
- **光标样式与闪烁**：`cursor_shape` 可选 `block`、`beam`、`underline`；`cursor_blink_interval` 设为 `0` 可禁用闪烁。
- **滚动历史行数**：`scrollback_lines` 默认为 2000，可按需增大（如 `10000`）。
- **窗口背景透明度**：`background_opacity` 设为 `0.8`（0~1 之间），配合 `dynamic_background_opacity` 可让快捷键动态调节（如 `Ctrl+Shift+up/down`）。
- **背景模糊（需 compositor 支持）**：`background_blur` 设为 `1` 或 `2`（数值越大模糊越强），并确保 `blur_radius` 非零。
- **会话保存与恢复**：在 `shell_integration` 中启用 `session`，关闭 Kitty 时会自动保存当前标签页和布局，下次打开自动恢复。

**常用键位**（K → Kitty (Ctrl+Shift)）：

| 按键 | 操作或命令 |
|---|---|
| K-F2 | 打开配置文件编辑器 |
| K-F3 | 命令面板 |
| K-T | 新标签页 |
| K-Q | 关闭标签页 |
| K-N | 分屏，新建容器 |
| K-W | 关闭容器 |

所有配置修改实时生效，无需重启 Kitty。若想永久保存，点击编辑器中的“保存”即可写入 `~/.config/kitty/kitty.conf`。更多配置项可参考 [官方文档](https://sw.kovidgoyal.net/kitty/conf.html)。


## 桌面篇

> 预计耗时：15 分钟（美化与字体设置）

以下以 KDE Plasma 为例，部分配置可能不兼容其他桌面环境，会注明兼容性。

### 字体配置

系统界面字体推荐使用 Google 开发的 Noto Fonts 字体包。

```bash
sudo pacman -S noto-fonts noto-fonts-emoji noto-fonts-cjk
```

| 字体名称 | 包名 | 兼容性 |
|---|---|---|
| Noto Fonts | noto-fonts | UTF-8 Basic，UI 兼容 |
| Noto Fonts CJK | noto-fonts-cjk | 可以使用繁体字和生僻字 |
| 文泉驿正黑 | wqy-zenhei | 有良好的 UI 兼容，但对次像素渲染几乎不兼容，一些 LCD 屏幕可能表现异常 |

等宽字体选择众多，如 Jetbrains Mono、Consolas 等。此处以 Monaspace 为例：

```bash
sudo pacman -S monaspace
```

| 字体名称 | 包名 | 兼容性 | 连字和 OpenType 特性 |
|---|---|---|---|
| Monospace | Plasma 自带 | 良好 | 无 |
| Hack | Plasma 自带 | 良好 | 无 |
| Jetbrains Mono | jetbrains-mono | 良好 | 支持连字 |
| Fira Code | fira-code | 良好 | 支持连字 |
| Monaspace | monaspace | 中等，在 tty 环境中可能出现少量显示异常 | 支持连字和纹理修复 |
| Consolas | consolas | 良好 | 无 |

在 **Plasma 设置 → 字体** 处更换字体和字号。

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

**Grub 主题**：访问 [grub-theme - GitHub Topic](https://github.com/topics/grub-theme) 找到合适的主题下载，使用 `sudo` 运行 `install.sh`。然后编辑 `/etc/grub.conf`，修改 `theme` 的值。

**SDDM 主题**：访问 [sddm-theme - GitHub Topic](https://github.com/topics/sddm-theme)，下载主题，同样使用 `sudo` 运行 `install.sh`。编辑 `/etc/sddm.conf`，修改 `theme` 的值。


## 日常管理篇

> 预计耗时：10 分钟（阅读与理解）

本章介绍 Arch Linux 日常使用中的重要注意事项及实用维护技巧。

### 系统更新注意事项

Arch 为滚动发行版，必须进行完整升级，不支持部分更新。请始终使用：

```bash
sudo pacman -Syu
```

**禁止**使用 `pacman -Sy` 或单独 `pacman -S <包名>` 而不执行完整升级，否则可能导致依赖冲突或系统不稳定。

建议每周至少更新一次，避免因积压过多更新而产生冲突。

#### 如果你真的滚挂了

虽然这种情况较少见，但若在更新安装阶段意外中断，**不要重启**，也不要关闭当前终端。先尝试排查问题，若问题较浅，可再次执行 `pacman -Syu`。

若已无法执行更新，立即打开 Timeshift 选择一个快照进行恢复。

若更严重——引导直接崩溃无法进入系统，可尝试手动修复，但更推荐使用 Arch Live USB 启动，执行 `arch-chroot`，然后使用命令行的 Timeshift 恢复。

### Sudo 的安全与便捷配置

sudo 是日常提权工具，使用中需注意以下要点。

#### 编辑 sudoers 的正确方法

**必须**使用 `visudo` 命令，该命令会检查语法错误，防止锁死系统。

```bash
sudo visudo
```

#### 常用配置项

在 `/etc/sudoers` 或 `/etc/sudoers.d/` 下添加文件：

- **允许 wheel 组用户执行任何命令（需密码）**：
  ```
  %wheel ALL=(ALL:ALL) ALL
  ```

- **允许 wheel 组无密码执行 pacman（谨慎使用）**：
  ```
  %wheel ALL=(ALL:ALL) NOPASSWD: /usr/bin/pacman
  ```

- **设置密码重试次数与超时时间**：
  ```
  Defaults passwd_tries=3, timestamp_timeout=5
  ```

{% callout type=warning %}
`NOPASSWD` 会降低系统安全性，仅建议在单用户个人电脑上针对特定命令（如 `pacman`）使用，切勿为 `ALL` 命令设置 `NOPASSWD`。
{% endcallout %}

#### 安全使用习惯

- **警惕破坏性命令**：执行 `sudo rm -rf`、`sudo dd` 等命令前，务必再三确认路径。
- **谨慎对待一行式安装命令**：尤其包含 `curl ... | sudo bash` 的命令。建议先下载脚本并人工审计：

```bash
curl -fsSL https://example.com/install.sh -o install.sh
less install.sh   # 检查
sudo bash install.sh
```

若脚本中包含 `rm -rf`、`/dev`、`/sys` 等可疑操作，切勿运行。

- **小心使用 `sudo !!`**：建议先用 `echo !!` 查看内容，再决定是否执行。

### 清理系统垃圾

长期使用会积累大量无用包和缓存。

**清理 pacman 缓存**：

```bash
sudo pacman -S pacman-contrib   # 安装 paccache
sudo paccache -r                # 保留最近 3 个版本
```

**彻底清理**（不推荐常规使用）：

```bash
sudo pacman -Scc
```

**删除孤儿包**：

```bash
sudo pacman -Rns $(pacman -Qtdq)
```

可将此命令添加到别名中。

### 回滚与故障恢复

**单软件降级**：

```bash
sudo pacman -U /var/cache/pacman/pkg/包名-旧版本.pkg.tar.zst
```

**系统整体回滚**：使用 Timeshift 从备份还原。建议在每次重大更新前手动创建快照。

**内核问题恢复**：在 GRUB 启动菜单中选择“高级选项”，使用 `linux-lts` 或其他备用内核启动，然后修复原内核。

### 日志查看与调试（Journalctl）

```bash
journalctl -xe                      # 显示最近的错误及详细信息
journalctl -p 3 -b                  # 显示本次启动的所有错误级别日志
journalctl -u NetworkManager        # 查看特定服务的日志
```

**限制日志大小**：编辑 `/etc/systemd/journald.conf`：

```ini
SystemMaxUse=200M
SystemMaxFileSize=50M
MaxRetentionSec=30day
```

**清理旧日志**：

```bash
sudo journalctl --vacuum-time=1d
sudo journalctl --vacuum-size=200M
```

**日志换行显示**：在 `~/.zshrc` 或 `~/.bashrc` 中添加：

```bash
export SYSTEMD_LESS="FRXMK"   # 换行而非截断
```

**仅查看最新日志（加速查询）**：

```bash
journalctl --file /var/log/journal/*/system.journal -f
```

分析启动慢的原因：

```bash
systemd-analyze blame
```

### 其他

**防火墙**：安装并启用 ufw 或 firewalld。

```bash
sudo pacman -S ufw
sudo ufw enable
sudo systemctl enable ufw
```

**SELinux / AppArmor**：Arch 对两者均提供支持，但配置较为复杂。普通桌面用户通常无需额外配置。

## 结语

至此，你已经完成了一个完整的 Arch Linux 系统从零到一的搭建过程。从分区到内核，从桌面环境到日常工具，你亲手构建了一个属于自己的、高度可控的 Linux 系统。

这一路走来，你可能遇到了各种各样的问题：网络配置不顺利、分区表搞错、GRUB 引导失败、显卡驱动黑屏……但你都一一克服了。这正是 Arch 之道——**知其然，更知其所以然**。

当你使用其他“开箱即用”的发行版时，那些被自动化脚本隐藏起来的细节，如今对你而言已不再是秘密。你知道系统是如何启动的，知道配置文件在哪里，知道如何排查问题，知道如何回滚修复。这种掌控感，是任何一键安装都无法给予的。

**一些最后的建议：**

1. **养成阅读 ArchWiki 的习惯**。它是最权威、最全面的信息来源，大部分问题都能在上面找到答案。
2. **谨慎对待每次更新**。更新前不妨逛逛 [Arch Linux 官网](https://archlinux.org/) 或 [Arch Linux 中文论坛](https://bbs.archlinuxcn.org/)，看看是否有重大变更公告。
3. **定期备份**。Timeshift 快照是你最可靠的保险，养成大更新前手动创建快照的习惯。
4. **探索与分享**。Arch 的乐趣不仅在于使用，更在于探索。去发现新的软件、新的配置技巧，也别忘了把你的经验分享给社区。

**Happy Arching!**

## 版权声明与致谢

### 版权声明

本作品（《Arch Linux 安装与配置教程》）采用 **知识共享署名 - 相同方式共享 4.0 国际许可协议（CC BY-SA 4.0）** 进行许可。

您可以自由地：

- **共享** — 在任何媒介以任何形式复制、发行本作品
- **演绎** — 修改、转换或以本作品为基础进行创作

惟须遵守下列条件：

- **署名** — 您必须给出适当的署名，提供指向本许可协议的链接，同时标明是否对原始作品作了修改。您可以用任何合理的方式来署名，但是不得以任何方式暗示许可人为您或您的使用背书。
- **相同方式共享** — 如果您再混合、转换或者基于本作品进行创作，您必须基于与原先许可相同的许可协议来分发您的贡献。

完整的许可协议文本请见：<https://creativecommons.org/licenses/by-sa/4.0/legalcode.zh-Hans>


### 致谢

本教程在编写过程中，参考并整合了大量来自 **[《archlinux 简明指南》](https://arch.icekylin.online/)** 的内容。该指南由 icekylin 等贡献者维护，是一份优秀的中文 Arch Linux 安装指南，对本教程的完善起到了重要的参考作用。特此感谢原作团队的卓越工作！

原作采用 **CC BY-SA 4.0** 许可，本教程遵循相同的许可协议。

本文在编写与修订过程中，使用了 AI 辅助工具进行内容完善、结构优化与校对，以确保技术细节的准确性和表述的清晰度，作者保证贡献不少于 AI（~~都写了这么多再改难道还可能贡献小于ai嘛~~）。

同时，本文多处配置细节及最佳实践参考了 [ArchWiki](https://wiki.archlinux.org/) 的官方文档。ArchWiki 是 Linux 世界最全面、最可靠的知识库之一，特此向 Arch 社区及所有 Wiki 贡献者致以诚挚的感谢。
