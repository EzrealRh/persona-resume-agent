#!/usr/bin/env python3
"""
Persona Resume Agent - Vault 初始化脚本
将 assets/vault-template 复制到用户指定目录，创建个人人物画像 Vault。

用法：
    python init_vault.py <目标目录>
    python init_vault.py ~/my-persona-vault
    python init_vault.py D:\Obsidian\my-persona-vault
"""

import os
import sys
import shutil
from pathlib import Path


def get_script_dir():
    """获取脚本所在目录"""
    return Path(os.path.dirname(os.path.abspath(__file__)))


def get_vault_template_dir():
    """获取 Vault 模板目录"""
    script_dir = get_script_dir()
    # 脚本在 scripts/ 目录下，模板在 ../assets/vault-template/
    template_dir = script_dir.parent / "assets" / "vault-template"
    return template_dir


def init_vault(target_dir: str):
    """初始化 Vault"""
    target_path = Path(target_dir).expanduser().resolve()
    template_dir = get_vault_template_dir()

    # 检查模板目录是否存在
    if not template_dir.exists():
        print(f"错误：模板目录不存在：{template_dir}")
        print("请确保在 persona-resume-agent 项目目录下运行此脚本。")
        sys.exit(1)

    # 检查目标目录
    if target_path.exists():
        if any(target_path.iterdir()):
            print(f"警告：目标目录已存在且不为空：{target_path}")
            response = input("是否继续？现有文件不会被覆盖，但同名文件会被跳过。(y/N): ")
            if response.lower() != 'y':
                print("已取消。")
                sys.exit(0)
    else:
        target_path.mkdir(parents=True, exist_ok=True)

    # 复制模板文件
    copied_count = 0
    skipped_count = 0

    for item in template_dir.rglob('*'):
        relative_path = item.relative_to(template_dir)
        target_item = target_path / relative_path

        if item.is_dir():
            target_item.mkdir(parents=True, exist_ok=True)
        else:
            if target_item.exists():
                skipped_count += 1
                print(f"  跳过（已存在）：{relative_path}")
            else:
                target_item.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target_item)
                copied_count += 1
                print(f"  创建：{relative_path}")

    # 输出结果
    print("\n" + "=" * 50)
    print(f"Vault 初始化完成！")
    print(f"  目标目录：{target_path}")
    print(f"  新建文件：{copied_count} 个")
    print(f"  跳过文件：{skipped_count} 个")
    print("=" * 50)
    print("\n下一步：")
    print("  1. 用 Obsidian 打开这个目录作为 Vault")
    print("  2. 对 AI 助手说：\"开始蒸馏我的人物画像\"")
    print("  3. 或者阅读 README.md 了解完整使用方法")
    print("\n提示：")
    print("  - 所有模板文件中的\"待填写\"都需要你和 AI 一起填充")
    print("  - 不需要一次填完，随时可以中断，下次继续")
    print("  - 应聘时把 JD 发给 AI，它会自动从 Vault 中提取素材生成简历")


def main():
    if len(sys.argv) != 2:
        print("用法：python init_vault.py <目标目录>")
        print("示例：python init_vault.py ~/my-persona-vault")
        print("示例：python init_vault.py D:\\Obsidian\\my-persona-vault")
        sys.exit(1)

    target_dir = sys.argv[1]
    init_vault(target_dir)


if __name__ == "__main__":
    main()
