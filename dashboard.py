import json
import os
import webbrowser
import sys
import time

TASKS_FILE = "tasks.json"
CONFIG_FILE = "config.json"

def load_json(filepath):
    """安全加载 JSON 文件"""
    if not os.path.exists(filepath):
        print(f"⚠️  找不到配置文件: {filepath}")
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"❌ 配置文件格式错误: {filepath}")
        return None

def show_tasks():
    """展示今日待办"""
    data = load_json(TASKS_FILE)
    if not data:
        return
    
    print("\n" + "="*40)
    print(f"📅 今日待办 ({data.get('date', '未设置日期')})")
    print("="*40)
    for idx, task in enumerate(data.get("tasks", []), 1):
        print(f"  [ ] {idx}. {task}")
    print("="*40 + "\n")

def launch_environment():
    """启动预设的学习环境"""
    data = load_json(CONFIG_FILE)
    if not data:
        return
    
    items = data.get("launch_items", [])
    if not items:
        print("📭 没有配置任何启动项。")
        return

    print("\n🚀 正在启动你的学习环境...")
    for item in items:
        name = item.get("name")
        target = item.get("target")
        item_type = item.get("type")
        
        print(f"  -> 正在打开: {name} ...")
        if item_type == "url":
            webbrowser.open(target)
        elif item_type == "app":
            try:
                os.startfile(target)  # Windows
            except AttributeError:
                import subprocess
                subprocess.Popen(["open", target]) # macOS
        time.sleep(0.5)
    
    print("✅ 环境启动完成！开始专注吧！\n")

def show_ai_prompt():
    """展示 AI 专注提示词"""
    prompt_file = "focus_prompt.md"
    if not os.path.exists(prompt_file):
        print("⚠️ 找不到 AI 提示词文件。")
        return
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt = f.read()
    
    print("\n" + "="*40)
    print("🧠 专注番茄钟 AI 提示词 (请复制以下内容发给 AI)")
    print("="*40)
    print(prompt)
    print("="*40 + "\n")

def main():
    while True:
        print("\n" + "="*40)
        print("🎓 欢迎使用 CLI 学习工作台")
        print("="*40)
        print("  1. 查看今日待办")
        print("  2. 一键启动学习环境")
        print("  3. 获取 AI 专注提示词")
        print("  0. 退出")
        print("="*40)
        
        choice = input("请输入选项 (0-3): ").strip()
        
        if choice == '1':
            show_tasks()
        elif choice == '2':
            launch_environment()
        elif choice == '3':
            show_ai_prompt()
        elif choice == '0':
            print("👋 再见！祝你学习愉快！")
            sys.exit(0)
        else:
            print("❌ 无效选项，请重新输入。")

if __name__ == "__main__":
    main()
