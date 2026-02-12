#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HexoConsole - 终端交互式 Hexo 生成与部署工具
功能：通过 W/S 切换任务，E 执行，Q 退出
所有命令均使用 nvm 别名 'blog' 指定的 Node 版本运行
"""

import os
import sys
import subprocess
from threading import Event

# ---------- 跨平台单字符输入 ----------
def getch():
    """跨平台获取单个按键，无需回车"""
    try:
        # Windows
        if os.name == 'nt':
            import msvcrt
            return msvcrt.getch().decode('utf-8', errors='ignore')
        # Unix / Linux / macOS
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
        # 备选方案：使用 input（需要按回车）
        return input("> ")[:1]
    except Exception as e:
        return ''

# ---------- 任务定义 ----------
TASKS = [
    {
        "name": "生成 (hexo generate)",
        "command": "nvm exec blog hexo generate"
    },
    {
        "name": "启动 (hexo server)",
        "command": "nvm exec blog hexo server"
    },
    {
        "name": "生成并启动",
        "command": "nvm exec blog hexo generate && nvm exec blog hexo server"
    },
    {
        "name": "部署 (netlify deploy preview)",
        "command": "nvm exec blog netlify deploy"
    },
    {
        "name": "部署 (netlify deploy production)",
        "command": "nvm exec blog netlify deploy --prod"
    }
]

class HexoConsole:
    def __init__(self):
        self.current_index = 0      # 当前选中任务索引
        self.running = True

    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_menu(self):
        """绘制主菜单"""
        self.clear_screen()
        print("\n" + "=" * 50)
        print("          Hexo 生成与部署控制台 (Node: blog)")
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
        """执行当前选中的命令"""
        task = TASKS[self.current_index]
        cmd = task["command"]

        print(f"\n▶ 正在执行: {task['name']}")
        print(f"  命令: {cmd}\n")

        try:
            # 使用 shell=True 以便支持 && 和 nvm 命令
            # 设置 bufsize=1 实现行缓冲，实时输出
            process = subprocess.Popen(
                cmd,
                shell=True,
                executable='/bin/bash' if os.name != 'nt' else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            # 实时打印输出
            for line in process.stdout:
                print(line, end='')

            process.wait()
            if process.returncode == 0:
                print("\n✅ 执行成功！")
            else:
                print(f"\n❌ 执行失败，返回码: {process.returncode}")

        except FileNotFoundError:
            print("\n❌ 命令未找到，请确认已安装 nvm/Hexo/Netlify CLI 并设置别名 'blog'")
        except Exception as e:
            print(f"\n❌ 执行异常: {e}")

        input("\n按 [Enter] 返回菜单...")

    def run(self):
        """主循环"""
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
            # 忽略其他按键

if __name__ == "__main__":
    # 检查是否在 Hexo 项目目录（可选）
    if not os.path.exists('_config.yml'):
        print("⚠️ 警告：当前目录未找到 _config.yml，可能不是 Hexo 项目根目录。")
        print("   请切换到 Hexo 博客目录后再运行此工具。\n")
        input("按 [Enter] 继续...")

    console = HexoConsole()
    console.run()