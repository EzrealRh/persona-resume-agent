#!/usr/bin/env python3
"""
Persona Resume Agent - Vault 初始化脚本（MCP 模式）
将 assets/vault-template 复制到 Obsidian vault 的 persona/ 子目录下。

用法：
    python init_vault.py                  # 自动检测 Obsidian vault 路径
    python init_vault.py "D:\Obsidian Vault"  # 指定 vault 路径
"""

import os
import sys
import json
import shutil
from pathlib import Path


def get_script_dir():
    return Path(os.path.dirname(os.path.abspath(__file__)))


def get_vault_template_dir():
    script_dir = get_script_dir()
    return script_dir.parent / "assets" / "vault-template"


def detect_obsidian_vault():
    """从 Obsidian 配置中自动检测 vault 路径"""
    if sys.platform == "win32":
        config_path = Path(os.environ.get("APPDATA", "")) / "obsidian" / "obsidian.json"
    else:
        config_path = Path.home() / ".config" / "obsidian" / "obsidian.json"

    if not config_path.exists():
        return None

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        vaults = config.get("vaults", {})
        # 优先选择当前打开的 vault
        for vid, vinfo in vaults.items():
            if vinfo.get("open"):
                return Path(vinfo["path"])
        # 否则返回第一个
        if vaults:
            first = next(iter(vaults.values()))
            return Path(first["path"])
    except (json.JSONDecodeError, KeyError, OSError):
        pass
    return None


def init_vault(vault_path: Path):
    """将 persona 模板复制到 vault 的 persona/ 目录"""
    template_dir = get_vault_template_dir()
    target_dir = vault_path / "persona"

    if not template_dir.exists():
        print(f"错误：模板目录不存在：{template_dir}")
        sys.exit(1)

    if not vault_path.exists():
        print(f"错误：Obsidian vault 目录不存在：{vault_path}")
        sys.exit(1)

    # 检查目标目录
    if target_dir.exists() and any(target_dir.iterdir()):
        print(f"警告：persona 目录已存在且不为空：{target_dir}")
        response = input("是否继续？现有文件不会被覆盖，但同名文件会被跳过。(y/N): ")
        if response.lower() != "y":
            print("已取消。")
            sys.exit(0)
    else:
        target_dir.mkdir(parents=True, exist_ok=True)

    # 复制模板文件
    copied_count = 0
    skipped_count = 0

    for item in template_dir.rglob('*'):
        relative_path = item.relative_to(template_dir)
        target_item = target_dir / relative_path

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

    print("\n" + "=" * 50)
    print("Vault 初始化完成！")
    print(f"  Obsidian vault：{vault_path}")
    print(f"  人物画像目录：{target_dir}")
    print(f"  新建文件：{copied_count} 个")
    print(f"  跳过文件：{skipped_count} 个")
    print("=" * 50)
    print("\n下一步：")
    print("  1. 确保 Obsidian 正在运行，Local REST API 插件已启用")
    print("  2. 在 MCP 客户端中添加 Obsidian MCP 服务器（见 SKILL.md 配置说明）")
    print("  3. 对 AI 助手说：\"开始蒸馏我的人物画像\"")


def main():
    if len(sys.argv) > 1:
        vault_path = Path(sys.argv[1]).expanduser().resolve()
    else:
        vault_path = detect_obsidian_vault()
        if vault_path is None:
            print("错误：无法自动检测 Obsidian vault 路径。")
            print("请手动指定：python init_vault.py <vault路径>")
            sys.exit(1)
        print(f"自动检测到 Obsidian vault：{vault_path}")

    init_vault(vault_path)


if __name__ == "__main__":
    main()
