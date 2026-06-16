---
title: 复活老 Mac：Intel MacBook Air 刷 Arch 指南
date: 2026-06-15 21:20:00
tags: 系统
category:
  - 教程
  - 生活
author: John Chiao
---

2012 年中款 MacBook Air，放在今天跑 macOS 已经像老牛拉破车了——系统臃肿、更新停止、风扇呼呼转。但硬件的底子其实不差：Intel Core i5、4GB 内存、512GB SSD，放到 Linux 世界里，这份配置仍算得上体面。更何况今天的 macOS 已经不再支持这台老机器，即便强行装上新版，软件也大多不兼容——App Store 里很多应用需要 macOS 11+，而它最高只能停在 Catalina，连 Homebrew 都开始劝退了（`Homebrew 不推荐您继续使用 macOS 10.15` 之类）。

所以不如换个活法，让它跑 Arch Linux。

## 0. Arch 适合你吗？

在动手之前，先回答一个关键问题：**Arch 真的适合你吗？** 别被“I use Arch btw”的优越感带偏了——Arch 不是另一个 Ubuntu，你得先搞清楚差异。

- **Windows** 是你交钱买来的黑箱——GUI 点来点去，能用就行，出问题靠重启大法。
- **Ubuntu** 是加了很多层包装的 Linux——预装桌面环境、驱动、软件管理工具，基本上装好就能用，对新手极其友好。但它的预装意味着你接受别人的选择，而不是你的选择。
- **Arch** 不一样。它从零开始——没有预装桌面环境，没有预装网卡驱动管理器，甚至刚装完连 `sudo` 都没有。Arch 给你的是一个空的“乐高箱”——从内核到桌面环境的每一块都由你亲手搭建，意味着你需要了解自己在做什么，也需要愿意花时间去读官方 Wiki（那是世界上最好的 Linux 文档之一）。

所以 Arch 适合这样的人：

- 想真正**学会** Linux，而不是停留在“会用”
- 愿意**手动配置**每一层，从网络到桌面
- 不介意**偶尔折腾**，甚至觉得这是一种乐趣

如果你符合这些，那就继续往下。

## 1. 准备你的 Mac

在彻底告别 macOS 之前，需要做几项关键准备工作——备份色彩配置、处理固件、规划分区。**这些步骤的顺序很重要**，尤其是曾经折腾过 Hackintosh 的机器。

### 保存 ICC 色彩配置文件

macOS 的色彩管理比 Linux 默认配置好很多，尤其是 MacBook Air 这块 TN 屏，出厂校准文件能让显示效果提升不少。在 macOS 中导出当前的屏幕色彩配置文件：

1. 打开“系统设置” → “显示器” → “色彩”选项卡。
2. 记下当前选中的色彩描述文件（例如 `Color LCD` 或某个自定义文件）。
3. 打开“色彩” → “显示描述文件” → “打开描述文件”。
4. 在弹出的窗口中，点击工具栏的“导出”按钮，将 `.icc` 文件保存到 U 盘或外置硬盘。

安装 Arch 后，在 KDE 系统设置 → 显示器 → 色彩配置中导入这个 `.icc` 文件，即可恢复原本的屏幕观感。

### 固件更新（重要！）

大量用户在 Wiki 中指出，macOS 是安装 Mac 固件更新的**唯一方式**，在安装 Arch 之前，请先确保固件更新到最新。

**如果你从未安装过 Hackintosh 或第三方引导器**，只需正常更新 macOS 固件：连接电源，打开 App Store 或系统设置中的“软件更新”，安装所有可用的更新（包括 macOS 版本更新和固件更新）。重启后再检查一次，确保固件处于最新版本。

**如果你曾安装过 Hackintosh（黑苹果）并刷入了非官方的 SMBIOS 机型信息（这也是我的情况）**，那么你的 Mac 硬件固件可能被篡改或锁死在非兼容状态。直接安装 Linux 会遇到各种奇怪问题（如电源管理失效、USB 口不识别、PCIe 设备丢失）。**必须先把 Mac 刷回原本兼容的系统**，恢复原厂固件状态。

具体回刷步骤：

1. **制作 macOS Sierra 安装 U 盘**  
   从 Apple 官网下载 macOS Sierra 的 ISO 镜像（注意是官方原版，不是黑苹果整合版）。使用 `dd` 或 `createinstallmedia` 命令制作启动 U 盘。

2. **从 U 盘启动并抹盘安装**  
   关机，插上 U 盘，开机按住 `Option` 键，选择 U 盘启动。进入“磁盘工具”，将内置 SSD 整个抹掉为 **Mac OS Extended (Journaled)**（即 HFS+） 格式，GUID 分区表。然后安装 macOS Sierra。

3. **降级到该型号支持的原始系统**  
   2012 年中 MacBook Air（MacBookAir5,2）出厂预装 OS X 10.8 Mountain Lion。安装 Sierra 后，它会自动将 EFI 固件更新到兼容版本，但部分修改过的 SMBIOS 信息可能仍残留。**建议在 Sierra 环境下强制删除遗留的 SMBIOS 数据**：
   - 打开终端，运行 `sudo nvram -c` 清除 NVRAM。
   - 重启，再次进入恢复模式（Command+R），打开终端，执行 `sudo firmwarepasswd -delete` 删除可能存在的固件密码。
   - 完全关机，按住 Control, Option, Shift 和电源键，静置 60 秒，让固件彻底复位。

4. **删除 SMBIOS 机型信息**  
   在 macOS Sierra 中安装 Clover Configurator 或 OpenCore Lagacy Patcher，检查当前 SMBIOS 是否仍显示为非本机型号（比如我之前刷了 MacBookPro9,2）。如果不对，请改回原来的机型，并关闭形如 `BIOS Spoof` 的选项。

5. **通过 App Store 更新到最新受支持系统**  
   固件和 SMBIOS 恢复原厂后，连接网络，打开 App Store，更新到该 Mac 能安装的最新 macOS（例如 Catalina 或 High Sierra）。这一步会下载并安装苹果官方发布的最后一代固件更新。完成后再重启一次，确保所有更新都已应用。

6. **关闭 SIP**
   更新后重启进恢复终端输入 `csrutil disable`，这是安装第三方引导的基础。

做完上述流程后，你的 Mac 固件已完全恢复到原厂标准状态，可以安心安装 Linux。

### 规划分区

我的 Air 有 512GB 硬盘，但 macOS 几乎已经没法用了——软件大多不兼容，连浏览器都停止更新，更别提日常办公或开发。与其保留一个臃肿且无用的 macOS，不如彻底释放这块 512GB 的 SSD，全部交给 Arch Linux。

**在动手之前，请备份所有重要数据**（照片、文档、代码等）到外置硬盘或云存储。因为接下来的操作会完全擦除整个硬盘。

如果你确实还想着偶尔切回 macOS，可以保留一个很小的分区（例如 64GB），但根据实际体验，2012 款 Air 跑 Catalina 已经很吃力，而且许多现代软件（Chrome 新版、VS Code、Office 等）都不再支持。**强烈建议直接单系统，一步到位。**

单系统的好处：

- 不需要处理双引导的复杂 EFI 分区冲突（macOS 默认 EFI 只有 200MB，而 Arch 需要至少 300MB 以上）
- 硬盘全部空间归 Linux 自由分配，可以充分用上 Btrfs 的快照和压缩功能
- 避免 macOS 不定期的系统更新覆盖 GRUB 引导

因此，在后续的安装步骤中，我们会用 `cfdisk` 完全重建分区表，不再保留任何 macOS 痕迹。准备工作完成后，就可以制作 Live USB 并开始安装了。

## 2. 选择 Bootloader

Intel Mac 的 EFI 实现和普通 PC 不太一样——它对非 macOS 系统有诸多限制，选对引导器至关重要。这里有三个选择：

**OpenCore（推荐）**。OpenCore 本身是黑苹果社区的产物，但它同样可以作为 Linux 引导器。它最大的优势是能向系统“注入”伪造的硬件信息，让 Arch 绕过 Apple 的硬件限制——比如默认情况下 Intel Mac 会禁止非 macOS 系统使用集成的 Intel 显卡（即“看门狗 watchdog”），OpenCore 可以绕过这一限制。如果你打算在 Mac 上长期用 Linux，OpenCore 是最值得投入的方案。

**rEFInd**。rEFInd 是图形化的启动管理器，配置相对简单。它同样能处理 macOS 版本伪装和 SIP 等限制。不要求 OpenCore 复杂配置的话，rEFInd 是个极佳选择。安装时只需注意在 `/boot/EFI/refind/refind.conf` 配置文件中添加 Linux 的引导配置。

**原生 GRUB**。直接安装 GRUB 也可以，但很可能遇到显卡或驱动加载问题。这一方案最精简，麻烦也最多，不推荐给新手。

2012 年的 MacBook Air 不带 T2 芯片，所以免去了禁用安全启动和关闭 SIP 的额外步骤——这也正是选择这台机器练手的原因之一。

## 3. 下载和刷写 Live USB

去 [Arch Linux 官网](https://archlinux.org/download/) 下载最新的 ISO 文件，建议校验一下 SHA256，确保文件完整。

下载完成后插入 U 盘（容量 ≥4GB），用 `dd` 命令刷写。**注意：务必确认 `of=` 后面的设备名，不要搞错，不然会覆盖你的系统盘。**

在 macOS 中块设备通常以 `diskXsY` 的形式表示，前面的数字 $X$ 是设备号，在 dev 设备中是字母，0 对应 a，1 对应 b，以此类推，后面的 $Y$ 是分区号，和 dev 号对应，比如 `disk0s2` 对应 `/dev/sda2`，其中 disk1 转为 a，s2 转为 2。

```bash
# 先确认 U 盘的设备名
diskmanager list
# 假设 U 盘是 /dev/YourDevice，刷写 ISO
sudo dd if=/path/to/archlinux-xxx.iso of=/dev/YourDevice bs=4M status=progress && sync
```

`bs=4M` 提高写入效率，`status=progress` 显示进度，`sync` 确保数据写入完成。

## 4. 启动到 Live

关机，插着 U 盘开机，立刻按住 `Option`（Alt）键不放，直到出现启动盘选择界面。看到黄色的 EFI Boot 图标，那是 U 盘，选中启动。

启动后会看到 GRUB 菜单，选择第一项 "Arch Linux install medium (x86_64, UEFI)"，回车。滚动过大量内核启动信息后，出现 `root@archiso ~ #` 的 shell 提示符——恭喜，你已经进入了 Arch 的 Live 环境。

## 5. 安装前的准备

现在开始真正的安装。

**第一步是网络连接。** 接上 iPhone 的 USB 热点最省事：连接手机后执行 `dhcpcd` 即可自动获取 IP。或者插根网线，或者尝试无线：

```bash
iwctl
device list                # 查看无线网卡，2012款MacBook Air显示为 wlan0
station wlan0 scan         # 扫描Wi-Fi
station wlan0 get-networks # 列出网络
station wlan0 connect "SSID" # 连接（输入密码后即刻连接）
exit
```

**注意**：Broadcom BCM4331 无线网卡在 Live 环境中可能需要额外驱动才能工作，所以强烈推荐优先使用 USB 网络共享或网线，安装完系统再折腾无线驱动会更省事。

**验证网络：** `ping -c 4 archlinux.org`。

**同步系统时间：** `timedatectl set-ntp true`。

**更新镜像源：** 国外的官方源速度可能很慢，编辑 `/etc/pacman.d/mirrorlist`，把 `Server = http://mirrors.ustc.edu.cn/archlinux/` 之类的国内源移到顶部。然后运行 `pacman -Syy` 刷新。

## 6. 分区和挂载

用 `lsblk` 确定硬盘设备名（通常是 `/dev/sda` 或 `/dev/nvme0n1`）。由于已经决定单系统，我们从头新建分区表：

```bash
cfdisk /dev/sda
```

选择 **gpt** 分区表类型。然后创建三个分区（512GB 空间充足，可以分配合理的交换分区大小）：

1. **EFI 系统分区：** 500MB，类型 `EFI System`
2. **交换分区：** 建议 8GB（4GB 内存的两倍，或者根据休眠需求设置），类型 `Linux swap`
3. **根分区：** 剩余所有空间（约 503GB），类型 `Linux filesystem`

写入后退出，格式化分区：

```bash
mkfs.fat -F32 /dev/sda1      # EFI分区格式化为 FAT32
mkswap /dev/sda2 && swapon /dev/sda2  # 交换分区启用
mkfs.btrfs /dev/sda3         # 根分区格式化为 Btrfs
```

**Btrfs 子卷：** Btrfs 支持快照功能，方便做系统回滚。挂载根分区后创建子卷：

```bash
mount /dev/sda3 /mnt
cd /mnt
btrfs subvolume create @          # 根目录子卷
btrfs subvolume create @home       # /home 子卷
cd /
umount /mnt
```

然后挂载子卷和 EFI 分区：

```bash
mount -o compress=zstd,subvol=@ /dev/sda3 /mnt
mkdir -p /mnt/{home,boot}
mount -o compress=zstd,subvol=@home /dev/sda3 /mnt/home
mount /dev/sda1 /mnt/boot
```

`compress=zstd` 启用透明压缩，节省磁盘空间的同时提升读取速度。

## 7. 安装基础系统

用 `pacstrap` 把基础系统装到 `/mnt`：

```bash
pacstrap /mnt base linux linux-firmware btrfs-progs
```

- `base`：Arch 基础包组
- `linux`：内核
- `linux-firmware`：内核固件，包含 Mac 硬件所需的各种驱动
- `btrfs-progs`：Btrfs 工具集

## 8. chroot和安装基础工具

```bash
genfstab -U /mnt >> /mnt/etc/fstab
arch-chroot /mnt
```

设置时区和硬件时钟：

```bash
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
hwclock --systohc
```

设置系统语言环境。编辑 `/etc/locale.gen`，取消 `en_US.UTF-8 UTF-8` 和 `zh_CN.UTF-8 UTF-8` 的注释，然后运行 `locale-gen`。创建 `/etc/locale.conf`，写入 `LANG=en_US.UTF-8`（英文环境兼容性最好，中文显示不会有问题）。

设置主机名：

```bash
echo "macarch" > /etc/hostname
```

编辑 `/etc/hosts` 添加上去。

设置 root 密码：`passwd`。

创建普通用户（Arch 不建议一直用 root 干活）：

```bash
useradd -m -G wheel -s /bin/bash 你的用户名
passwd 你的用户名
```

安装 sudo：`pacman -S sudo`，然后 `visudo` 取消 `%wheel ALL=(ALL:ALL) ALL` 的注释，让 `wheel` 组的用户能用 sudo。

安装网络工具：

```bash
pacman -S networkmanager dhcpcd iwd
systemctl enable NetworkManager
```

## 9. 安装 GRUB

```bash
pacman -S grub efibootmgr
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
grub-mkconfig -o /boot/grub/grub.cfg
```

生成的 GRUB 配置应该能正确识别 Arch。单系统方案下，这就可以直接用了。

## 10. 安装桌面环境（KDE Plasma）和会话管理器

基础系统装完了，但还在命令行里。现在给它装上 KDE Plasma——轻量又现代，对老硬件足够友好。

安装 KDE Plasma（推荐完整版）：

```bash
sudo pacman -S plasma-meta kde-applications-meta sddm
sudo systemctl enable sddm
```

如果 4GB 内存捉襟见肘，也可以装轻量版 `plasma-desktop`，省下不少资源。

安装 Intel 显卡驱动（2012款 MacBook Air 用的是 HD Graphics 4000）：

```bash
sudo pacman -S xf86-video-intel mesa vulkan-intel intel-ucode
```

Intel 微码包 `intel-ucode` 很重要，它能修复 CPU 的硬件 bug，提升稳定性。

重启之后，就能看到 SDDM 的登录界面，选择 Plasma 会话，输入用户名密码——**你的 MacBook Air 现在正式“复活”了，有图形界面了**。

## 11. 网卡驱动（Broadcom）

重启后发现——Wi-Fi 呢？没有。因为 2012 款 MacBook Air 用的是 Broadcom BCM4331 无线网卡，内核主线中缺乏原生支持。

解决方案是安装 `broadcom-wl-dkms` 驱动。但 DKMS 需要内核头文件，所以先：

```bash
sudo pacman -S base-devel dkms linux-headers
```

**如果你已经配置了网络（比如 USB 共享），可以直接安装：**

```bash
sudo pacman -S broadcom-wl-dkms
```

**如果现在没网络（这是常见陷阱）**，就需要另一台电脑下载包文件，拷过来离线安装。最省事的办法是：先用手机 USB 共享网络，安装好 Wi-Fi 驱动后再切换回无线。

安装完驱动后，屏蔽内核自带的冲突驱动：

```bash
sudo nano /etc/modprobe.d/broadcom-wl-dkms.conf
```

写入：

```
blacklist brcm80211
blacklist b43
blacklist b43legacy
```

然后重启：`reboot`。

重启后 Wi-Fi 应该就能用了。验证一下：`lspci -vnn -d 14e4:` 应该能看到 BCM4331 的信息。

## 12. Mac 特性管理（键盘灯，风扇，媒体按键等）

MacBook 装上 Linux 后，很多硬件功能需要手动配置才能正常工作。

**键盘背光控制：** 在 KDE Plasma 下，键盘背光通常能自动识别，可以通过 Fn + F5/F6（或 F5/F6 直接，取决于设置）调节亮度。如果不行，可以安装 `kbdlight`（AUR 中提供）或通过 D-Bus 脚本控制。

**风扇控制：** MacBook 的风扇在 Linux 下默认按 BIOS 预设曲线运行，对温度不敏感。推荐安装 **mbpfan**——一个轻量级守护程序，通过 `coretemp` 和 `applesmc` 内核模块读取 CPU 温度，自动调节风扇转速，在性能和噪音之间取得平衡。

装法：

```bash
# 先启用必要模块
sudo modprobe applesmc
# 安装 mbpfan（AUR 中的版本会自带上 systemd 服务）
yay -S mbpfan-git
sudo systemctl enable --now mbpfan
```

`mbpfan` 的默认配置文件 `/etc/mbpfan.conf` 提供了温度阈值设置，可以根据自己的偏好调整风扇启停的温度点。

**媒体键（音量、亮度、播放控制等）：** KDE Plasma 通常能直接识别 Fn + 功能键的组合。如果不工作，安装 `acpi` 包，然后通过系统的“快捷键”设置手动映射每个功能键的快捷键组合。

**苹果 SMC 模块：** `applesmc` 模块提供了电池状态、温度传感器等信息。确保它已加载：

```bash
sudo modprobe applesmc
echo "applesmc" | sudo tee /etc/modules-load.d/applesmc.conf
```

**触控板增强：** 默认的触控板驱动（`libinput`）支持基础的多点触控。建议安装 `xf86-input-synaptics` 以获得更多配置选项，然后在 `/etc/X11/xorg.conf.d/` 中调整触控板参数，比如开启自然滚动、调节灵敏度等。

## 13. 附加软件源（CN, AUR）

Arch 官方仓库已经很丰富，但有些社区驱动的软件包还在 **AUR（Arch User Repository）** 里，需要 AUR 助手来管理。推荐 **yay**——目前最流行、最稳定的 AUR 助手。

安装 `yay` 有两种常见方式：

- **方法一（通过 Arch Linux CN 仓库）：** 在 `/etc/pacman.conf` 添加 `[archlinuxcn]` 源，`sudo pacman -S archlinuxcn-keyring`，然后 `sudo pacman -S yay`。
- **方法二（手动编译，更传统）：** `git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si`。

安装完成后：

```bash
yay -S 软件包名    # 安装 AUR 包
yay -Syu          # 同时更新官方仓库和 AUR
```

如果把中文源也加上了，很多国内常用软件都能直接 `pacman -S` 安装，不必再自己编译。

## 14. 自定义设置（plasma，终端模拟器(kitty)，powerlevel10k等）

### KDE Plasma 美化

- 系统设置 → 全局主题：Breeze 或去 KDE Store 下载其他主题
- 系统设置 → 图标：推荐 Papirus
- 系统设置 → 工作区行为 → 桌面效果：可以关闭几个不必要的特效节省性能
- KDE 自带的 `kwallet` 可能会频繁弹窗，可以禁用（系统设置 → 应用程序 → KDE 钱包 → 禁用）

### 终端模拟器——Kitty

Konsole 挺好，但 **Kitty** 更现代、更快，支持 GPU 加速和真彩色。安装：

```bash
sudo pacman -S kitty
```

在系统设置中将默认终端从 Konsole 改为 Kitty 即可。

### Powerlevel10k（zsh 主题）

先把 zsh 设为默认 shell：`sudo pacman -S zsh && chsh -s /bin/zsh`。

安装 Oh My Zsh：

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

安装 Powerlevel10k：

```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="powerlevel10k\/powerlevel10k"/' ~/.zshrc
```

重启 zsh（`exec zsh`）后 Powerlevel10k 会自动启动配置向导，按提示选择自己喜欢的样式。**注意：Powerlevel10k 依赖 Nerd Fonts 才能正确显示特殊图标**，在 Kitty 配置中将字体改为 `MesloLGS NF` 或其他 Nerd Fonts。

## 15. 开机动画（Plymouth）

开机时滚动的内核信息行虽然 geek，但不够美观。**Plymouth** 能在启动过程（包括 initramfs 阶段）显示图形动画，让开机体验更顺滑。

安装并配置：

```bash
sudo pacman -S plymouth
```

编辑 `/etc/mkinitcpio.conf`，在 `HOOKS` 数组中找到 `base udev ... filesystems` 这段，把 `plymouth` 加到 `udev` 之后：

```
HOOKS=(base udev plymouth ... filesystems)
```

重新生成 initramfs：

```bash
sudo mkinitcpio -p linux
```

在内核参数中添加 `splash`。编辑 `/etc/default/grub`，修改 `GRUB_CMDLINE_LINUX_DEFAULT`，加入 `splash quiet`：

```
GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet splash"
```

然后 `sudo grub-mkconfig -o /boot/grub/grub.cfg`。

如果 Mac 启动太快，动画一闪而过，可以对 Plymouth 服务加个延迟：

```bash
sudo mkdir -p /etc/systemd/system/plymouth-quit.service.d/
```

创建 drop-in 文件写入 `ExecStartPre=/usr/bin/sleep 5`。

## 16. 功耗控制（TLP）

笔记本续航是关键。**TLP** 是 Linux 下最强大的电源管理工具，无需复杂配置就能显著延长电池寿命。

安装并启用：

```bash
sudo pacman -S tlp tlp-rdw
sudo systemctl enable tlp
sudo systemctl start tlp
```

TLP 的默认配置已基于 Powertop 建议优化，对大部分用户已足够。如果想微调，编辑 `/etc/tlp.conf`：设置充电阈值、USB 自动挂起、Wi-Fi 电源管理等。

与 TLP 配合的还有 `powertop`，可以用来分析和校准功耗：

```bash
sudo pacman -S powertop
sudo powertop --calibrate  # 电池充放电状态下各运行一次
```

配置完 TLP 后，再结合 KDE 系统设置 → 电源管理，对屏幕亮度和键盘背光分别设置“电池供电”和“外接电源”两套策略（比如电池时将屏幕亮度降到 20%、键盘背光降低或关闭），省电效果会非常明显。

## 17. 结尾

到此为止，这台 2012 年的 MacBook Air 已经彻底脱胎换骨——从无法更新、卡顿到不行的 macOS 宿主，变成了完全掌控在自己手中的 Arch Linux 工作站。512GB 的 SSD 给了你充裕的空间，无论是编译代码、存储文档，还是折腾各种发行版，都绰绰有余。开机十几秒到登录界面，KDE Plasma 运行丝滑，Wi-Fi 稳定，风扇不再狂转，电池续航也好了不少。

**最后的忠告：**

1. **定期更新：** `yay -Syu` 每周来一次。滚动发行就像照顾盆栽，不浇水就枯了。

2. **备份配置：** 把重要的 dotfiles（`.zshrc`、`.config/` 等）推送到 GitHub。系统挂了可以快速重建习惯的配置。

3. **拥抱 Arch Wiki：** 遇到问题时，第一个搜索引擎应该用 `site:wiki.archlinux.org` 而不是 Google——那是全世界最好的 Linux 文档。遇到 MacBook 特定的问题，翻翻笔记本对应的型号页面（如 MacBookAir5,2 的专项配置）。

4. **警惕内核更新：** 使用 `broadcom-wl-dkms` 驱动的 Mac 用户要注意，`linux` 内核大版本更新后要同步更新 `linux-headers`，否则 DKMS 模块会无法编译，Wi-Fi 会掉。恢复办法：切回 USB 网络共享，重新安装 `broadcom-wl-dkms`。

最后说一句：手动安装 Arch 的经历本身是一笔很大的财富——它逼着你去理解 UEFI、内核模块、文件系统、systemd 这些概念，而不是把它们当成黑箱。当你第一次从这个小小的 MacBook Air 上看到自己亲手拼出的 Plasma 桌面时，那种感觉，完全不一样。
