import os
import subprocess
import sys
import shutil

def remove_directory(path):
    """彻底删除目录"""
    if os.path.exists(path):
        print(f"[Info] Removing directory: {path}")
        try:
            shutil.rmtree(path)
            return True
        except Exception as e:
            print(f"[Error] Failed to remove {path}: {e}")
            return False
    return True

def move_subfolders(src_dir, dst_dir):
    """将源目录下的所有子文件夹移动到目标目录"""
    if not os.path.exists(src_dir):
        return True
    
    print(f"[Info] Moving subfolders from {src_dir} to {dst_dir}")
    success = True
    
    for item in os.listdir(src_dir):
        item_path = os.path.join(src_dir, item)
        if os.path.isdir(item_path):
            dst_item_path = os.path.join(dst_dir, item)
            
            # 如果目标目录已存在，先删除
            if os.path.exists(dst_item_path):
                if not remove_directory(dst_item_path):
                    success = False
                    continue
            
            try:
                shutil.move(item_path, dst_dir)
                print(f"[Info] Moved: {item} -> {dst_dir}")
            except Exception as e:
                print(f"[Error] Failed to move {item}: {e}")
                success = False
    
    return success

def main():
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 获取当前文件夹名称
    folder_name = os.path.basename(current_dir)
    
    # 构建 spec 文件路径
    spec_file = f"{folder_name}.spec"
    
    print("============================================")
    print(f"  PyInstaller Build Script")
    print("============================================")
    print(f"Current directory: {current_dir}")
    print(f"Folder name: {folder_name}")
    print(f"Spec file: {spec_file}")
    print()
    
    # 检查 spec 文件是否存在
    if not os.path.exists(spec_file):
        print(f"[Error] Spec file '{spec_file}' not found!")
        input("Press Enter to exit...")
        return 1
    
    # 执行打包前的检查
    print("[Info] Pre-build checks...")
    
    # 检查是否同时存在 build 和 dist 文件夹
    build_dir = "build"
    dist_dir = "dist"
    
    if os.path.exists(build_dir) and os.path.exists(dist_dir):
        print(f"[Warning] Found both {build_dir} and {dist_dir} directories!")
        # 1. 彻底删除 build 文件夹
        remove_directory(build_dir)
        # 2. 把 dist 文件夹里的子文件夹移到当前目录
        if move_subfolders(dist_dir, current_dir):
            # 3. 彻底删除 dist 文件夹
            remove_directory(dist_dir)
        print("[Info] Both directories processed. Stopping build.")
        input("Press Enter to exit...")
        return 0
    
    # 检查是否已有 build 文件夹
    if os.path.exists(build_dir):
        print(f"[Warning] Found existing {build_dir} directory!")
        remove_directory(build_dir)
        print("[Info] Build directory removed. Stopping build.")
        input("Press Enter to exit...")
        return 0
    
    # 检查是否已有 dist 文件夹
    if os.path.exists(dist_dir):
        print(f"[Warning] Found existing {dist_dir} directory!")
        # 移动 dist 文件夹里的子文件夹到当前目录
        if move_subfolders(dist_dir, current_dir):
            # 彻底删除 dist 文件夹
            remove_directory(dist_dir)
        print("[Info] Dist directory processed. Stopping build.")
        input("Press Enter to exit...")
        return 0
    
    # 检查 Python 版本
    print("[Info] Checking Python version...")
    python_version = sys.version
    print(f"[Info] Python version: {python_version.strip()}")
    print()
    
    # 检查 requirements.txt 并安装依赖
    requirements_file = "requirements.txt"
    if os.path.exists(requirements_file):
        print(f"[Info] Found {requirements_file}, installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], check=True)
        print()
    else:
        print(f"[Warning] {requirements_file} not found, skipping dependency installation")
        print()
    
    # 执行 PyInstaller 命令
    print(f"[Info] Starting build process with PyInstaller...")
    print(f"[Command] {sys.executable} -m PyInstaller {spec_file}")
    print()
    
    try:
        # 在新的命令行窗口中执行 PyInstaller
        cmd_command = f"{sys.executable} -m PyInstaller {spec_file}"
        print(f"[Info] Opening new CMD window to run: {cmd_command}")
        
        subprocess.run(
            ["start", "cmd", "/c", cmd_command],
            shell=True,
            check=True
        )
        
        print("[Info] Build process started in new window!")
        print("[Info] Please check the new CMD window for build progress.")
        print()
        
        # 等待用户确认
        input("Press Enter to continue after build completes...")
        
        # 打包后的处理
        print("\n[Info] Post-build processing...")
        
        # 1. 彻底删除生成的 build 文件夹
        remove_directory(build_dir)
        
        # 2. 把 dist 文件夹里的子文件夹移到当前目录
        move_subfolders(dist_dir, current_dir)
        
        # 3. 彻底删除 dist 文件夹
        remove_directory(dist_dir)
        
        print("\n[Info] Post-build processing completed!")
        print()
        
        # 显示最终结果
        print("[Info] Build completed successfully!")
        print(f"[Info] Output files are now in the current directory.")
        
        # 移除运行后生成的 __pycache__ 文件夹
        pycache_dir = os.path.join(current_dir, "__pycache__")
        remove_directory(pycache_dir)
        
        return 0
    except subprocess.CalledProcessError as e:
        print(f"[Error] Failed to start build process: {e}")
        
        # 移除运行后生成的 __pycache__ 文件夹
        pycache_dir = os.path.join(current_dir, "__pycache__")
        remove_directory(pycache_dir)
        
        input("Press Enter to exit...")
        return 1
    except Exception as e:
        print(f"[Error] Unexpected error: {e}")
        
        # 移除运行后生成的 __pycache__ 文件夹
        pycache_dir = os.path.join(current_dir, "__pycache__")
        remove_directory(pycache_dir)
        
        input("Press Enter to exit...")
        return 1

if __name__ == "__main__":
    sys.exit(main())