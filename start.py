#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HexoConsole - 终端交互式 Hexo 生成与部署工具
功能：通过 W/S 切换任务，E 执行，Q 退出
修复方式：硬编码 Node 绝对路径（适用于 macOS/Linux）
Node 路径: /Users/JohnCh/.nvm/versions/node/v18.20.4/bin/node
"""

import os
import sys
import subprocess
import shutil
from threading import Event

# ---------- 跨平台单字符输入 ----------
def getch():
    """跨平台获取单个按键，无需回车"""
    try:
        if os.name == 'nt':
            import msvcrt
            return msvcrt.getch().decode('utf-8', errors='ignore')
        else:
            import termios
            import tty
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
    except ImportError:
        return input("> ")[:1]
    except Exception:
        return ''

# ---------- 全局路径变量（硬编码 Node 路径）----------
# 硬编码为您的 nvm 别名 'blog' 对应的 Node 路径
NODE_PATH = "/Users/JohnCh/.nvm/versions/node/v18.20.4/bin/node"
HEXO_PATH = None      # 自动查找
NETLIFY_PATH = None   # 自动查找

def init_paths():
    """初始化命令路径：Node 硬编码，hexo/netlify 自动查找"""
    global NODE_PATH, HEXO_PATH, NETLIFY_PATH

    # 1. 验证硬编码的 Node 路径是否存在
    if not os.path.isfile(NODE_PATH):
        print(f"❌ 硬编码 Node 路径不存在: {NODE_PATH}")
        print("   请确认路径正确，或修改脚本中的 NODE_PATH 变量。")
        sys.exit(1)
    print(f"✅ 使用硬编码 Node: {NODE_PATH}")

    # 2. 查找 hexo 可执行文件（优先项目本地，其次全局）
    HEXO_PATH = shutil.which('hexo')
    if not HEXO_PATH:
        local_hexo = os.path.join(os.getcwd(), 'node_modules', '.bin', 'hexo')
        if os.path.isfile(local_hexo):
            HEXO_PATH = local_hexo
    if not HEXO_PATH:
        print("❌ 未找到 hexo 命令，请全局安装: npm install -g hexo-cli")
        sys.exit(1)
    print(f"✅ 找到 hexo: {HEXO_PATH}")

    # 3. 查找 netlify 可执行文件
    NETLIFY_PATH = shutil.which('netlify')
    if not NETLIFY_PATH:
        local_netlify = os.path.join(os.getcwd(), 'node_modules', '.bin', 'netlify')
        if os.path.isfile(local_netlify):
            NETLIFY_PATH = local_netlify
    if not NETLIFY_PATH:
        print("❌ 未找到 netlify 命令，请全局安装: npm install -g netlify-cli")
        sys.exit(1)
    print(f"✅ 找到 netlify: {NETLIFY_PATH}")

# ---------- 任务定义（使用绝对路径模板）----------
TASKS = [
    {
        "name": "生成 (hexo generate)",
        "cmd_template": "{node} {hexo} generate"
    },
    {
        "name": "启动 (hexo server)",
        "cmd_template": "{node} {hexo} server"
    },
    {
        "name": "生成并启动",
        "cmd_template": "{node} {hexo} generate && {node} {hexo} server"
    },
    {
        "name": "部署 (netlify deploy preview)",
        "cmd_template": "{node} {netlify} deploy"
    },
    {
        "name": "部署 (netlify deploy production)",
        "cmd_template": "{node} {netlify} deploy --prod"
    }
]

class HexoConsole:
    def __init__(self):
        self.current_index = 0
        self.running = True

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_menu(self):
        self.clear_screen()
        print("\n" + "=" * 50)
        print("          Hexo 生成与部署控制台 (Node: 硬编码 v18.20.4)")
        print("=" * 50)
        print()
        for i, task in enumerate(TASKS):
            prefix = "> " if i == self.current_index else "  "
            print(f"{prefix}{task['name']}")
        print()
        print("-" * 50)
        print("当前选中:", TASKS[self.current_index]["name"])
        print("操作: [W/S] 上下切换  [E] 执行选中任务  [Q] 退出")
        print("=" * 50)

    def execute_current(self):
        """执行当前选中的任务，使用绝对路径直接调用"""
        task = TASKS[self.current_index]
        cmd = task["cmd_template"].format(
            node=NODE_PATH,
            hexo=HEXO_PATH,
            netlify=NETLIFY_PATH
        )

        print(f"\n▶ 正在执行: {task['name']}")
        print(f"  命令: {cmd}\n")

        try:
            process = subprocess.Popen(
                cmd,
                shell=True,
                executable='/bin/bash' if os.name != 'nt' else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            for line in process.stdout:
                print(line, end='')

            process.wait()
            if process.returncode == 0:
                print("\n✅ 执行成功！")
            else:
                print(f"\n❌ 执行失败，返回码: {process.returncode}")

        except FileNotFoundError as e:
            print(f"\n❌ 命令未找到: {e}")
        except Exception as e:
            print(f"\n❌ 执行异常: {e}")

        input("\n按 [Enter] 返回菜单...")

    def run(self):
        while self.running:
            self.print_menu()
            key = getch().lower()

            if key == 'w':
                self.current_index = (self.current_index - 1) % len(TASKS)
            elif key == 's':
                self.current_index = (self.current_index + 1) % len(TASKS)
            elif key == 'e':
                self.execute_current()
            elif key == 'q':
                self.running = False
                self.clear_screen()
                print("👋 已退出 HexoConsole。\n")

if __name__ == "__main__":
    if not os.path.exists('_config.yml'):
        print("⚠️ 警告：当前目录未找到 _config.yml，可能不是 Hexo 项目根目录。")
        print("   请切换到 Hexo 博客目录后再运行此工具。\n")
        input("按 [Enter] 继续...")

    init_paths()
    console = HexoConsole()
    console.run()