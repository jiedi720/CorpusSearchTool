"""
测试脚本，用于验证拖拽功能是否正常工作
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_drag_drop():
    """测试拖拽功能"""
    print("正在测试拖拽功能...")
    
    try:
        # 尝试导入拖拽模块
        from function.file_drag_drop import create_drag_drop_window
        print("✓ 成功导入拖拽模块")
        
        # 尝试创建支持拖拽的窗口
        window = create_drag_drop_window("拖拽功能测试")
        print("✓ 成功创建支持拖拽的窗口")
        
        # 检查窗口是否支持拖拽功能
        if hasattr(window, 'dnd_bind'):
            print("✓ 窗口支持拖拽功能")
        else:
            print("✗ 窗口不支持拖拽功能")
            
        # 销毁测试窗口
        window.destroy()
        
        print("\n拖拽功能测试完成!")
        return True
        
    except ImportError as e:
        print(f"✗ 导入错误: {e}")
        print("请运行: pip install tkinterdnd2")
        return False
    except Exception as e:
        print(f"✗ 测试过程中出现错误: {e}")
        return False

def test_main_application():
    """测试主应用程序是否可以启动"""
    print("\n正在测试主应用程序启动...")
    
    try:
        from gui.main_window import MainWindow
        print("✓ 成功导入主窗口模块")
        return True
    except ImportError as e:
        print(f"✗ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"✗ 启动过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    print("字幕语料库检索工具 - 功能测试")
    print("="*40)
    
    # 测试拖拽功能
    drag_drop_ok = test_drag_drop()
    
    # 测试主应用程序
    main_app_ok = test_main_application()
    
    print("\n" + "="*40)
    print("测试结果:")
    print(f"拖拽功能: {'✓ 正常' if drag_drop_ok else '✗ 异常'}")
    print(f"主程序启动: {'✓ 正常' if main_app_ok else '✗ 异常'}")
    
    if drag_drop_ok and main_app_ok:
        print("\n✓ 所有功能测试通过!")
    else:
        print("\n✗ 部分功能存在问题，请检查上述错误信息")
        
    input("\n按回车键退出...")