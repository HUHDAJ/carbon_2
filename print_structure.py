#!/usr/bin/env python
"""
打印项目结构
"""
import os
from pathlib import Path

def print_directory_tree(root_dir, prefix="", max_depth=6, current_depth=0):
    """打印目录树"""
    if current_depth > max_depth:
        return
    
    items = list(root_dir.iterdir())
    items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        
        if item.is_dir():
            print(f"{prefix}{'└── ' if is_last else '├── '}{item.name}/")
            
            new_prefix = prefix + ("    " if is_last else "│   ")
            if item.name not in ['.venv', '__pycache__', '.git', 'node_modules']:
                print_directory_tree(item, new_prefix, max_depth, current_depth + 1)
        else:
            size = item.stat().st_size
            size_str = f" ({size:,} bytes)" if size > 0 else " (empty)"
            print(f"{prefix}{'└── ' if is_last else '├── '}{item.name}{size_str}")

def main():
    # 获取项目根目录
    current_dir = Path(os.getcwd())
    print(f"当前目录: {current_dir}")
    
    print("\n" + "="*80)
    print("项目结构:")
    print("="*80)
    print_directory_tree(current_dir, max_depth=4)

if __name__ == "__main__":
    main()