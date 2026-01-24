@echo off
chcp 65001 >nul
echo ========================================
echo 字幕语料库检索工具 - 调试模式
echo ========================================
echo.
echo 启动中...调试信息将显示在此窗口
echo.
python CorpusSearchTool.py
echo.
echo 程序已退出，按任意键关闭窗口...
pause >nul