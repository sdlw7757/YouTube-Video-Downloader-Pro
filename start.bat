@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 设置标题和窗口大小
title YouTube Downloader
mode con cols=100 lines=30

:: 获取当前目录
set "CURRENT_DIR=%~dp0"
set "CURRENT_DIR=%CURRENT_DIR:~0,-1%"

:: 检查必要的文件是否存在
if not exist "%CURRENT_DIR%\youtube_downloader.py" (
    echo 错误: 找不到 youtube_downloader.py 文件
    echo 请确保此批处理文件与 youtube_downloader.py 文件在同一目录下
    pause
    exit /b 1
)

:: 启动Python程序
"%CURRENT_DIR%\python\python.exe" "%CURRENT_DIR%\youtube_downloader.py"

:: 检查程序退出状态
if %errorlevel% neq 0 (
    echo.
    echo 程序异常退出，错误代码: %errorlevel%
    pause
)

exit