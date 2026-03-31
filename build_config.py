#!/usr/bin/env python3
"""
《经典炸弹人》复刻版 - PyInstaller打包配置脚本
使用方法: python build_config.py
"""

import PyInstaller.__main__
import platform
import os
import sys


def configure_console_encoding():
    """尽量让脚本在 Windows CI 中安全输出 Unicode 日志。"""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None or not hasattr(stream, "reconfigure"):
            continue
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            # 某些环境下标准流不可重配，保持默认配置继续运行。
            pass

def build_for_current_platform():
    """为当前平台构建可执行文件"""
    system = platform.system().lower()

    print(f"🔨 开始为 {system.upper()} 平台打包...")

    # 基础参数配置
    common_args = [
        'main.py',
        '--name=Bomberman',
        '--windowed',  # 隐藏控制台窗口
        '--onefile',   # 单文件模式（也可改为 --onedir 生成文件夹）
        '--clean',
        '--noconfirm',
    ]

    # 添加资源目录（不同平台分隔符不同）
    if system == 'windows':
        common_args.append('--add-data=assets;assets')
        # 如果有图标文件
        if os.path.exists('assets/images/icon.ico'):
            common_args.append('--icon=assets/images/icon.ico')
    else:  # macOS 和 Linux
        common_args.append('--add-data=assets:assets')
        # macOS 可以使用 .icns，Linux 使用 .png
        if system == 'darwin' and os.path.exists('assets/images/icon.icns'):
            common_args.append('--icon=assets/images/icon.icns')

    # 平台特定配置
    if system == 'darwin':  # macOS
        common_args.extend([
            '--osx-bundle-identifier=com.yourgame.bomberman',
            '--target-arch=universal2',  # 同时支持Intel和Apple Silicon
        ])
    elif system == 'windows':
        # 如果有版本信息文件
        if os.path.exists('version_info.txt'):
            common_args.append('--version-file=version_info.txt')
    elif system == 'linux':
        # Linux 特定配置（如果需要）
        pass

    print(f"📦 打包参数: {' '.join(common_args)}")

    try:
        PyInstaller.__main__.run(common_args)
        print(f"✅ 打包完成！输出位置: dist/")
        print(f"💡 提示: 可执行文件位于 dist/ 目录中")
    except Exception as e:
        print(f"❌ 打包失败: {e}")
        return False

    return True

def main():
    """主函数"""
    configure_console_encoding()
    print("=" * 60)
    print("《经典炸弹人》复刻版 - 自动打包工具")
    print("=" * 60)

    # 检查 main.py 是否存在
    if not os.path.exists('main.py'):
        print("❌ 错误: 找不到 main.py 文件！")
        print("💡 请确保在项目根目录运行此脚本。")
        return

    # 检查 assets 目录
    if not os.path.exists('assets'):
        print("⚠️  警告: 找不到 assets/ 目录，游戏资源可能缺失。")
        response = input("是否继续打包？(y/n): ")
        if response.lower() != 'y':
            print("⏹️  打包已取消。")
            return

    # 执行打包
    success = build_for_current_platform()

    if success:
        print("\n" + "=" * 60)
        print("🎉 打包成功！")
        print("=" * 60)
        print("\n📋 下一步:")
        print("  1. 在 dist/ 目录查找可执行文件")
        print("  2. 测试可执行文件是否正常运行")
        print("  3. 确认游戏资源是否正确加载")
        print("  4. 检查游戏功能是否完整")

if __name__ == '__main__':
    main()
