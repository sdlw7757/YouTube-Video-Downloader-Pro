YouTube视频下载器 PRO
<img width="941" height="625" alt="捕获" src="https://github.com/user-attachments/assets/314a8c51-78dc-4a41-99b9-55814ca85fd7" />

一个简单易用的YouTube视频下载工具，支持多种功能和格式。

## 项目结构

```
YouTube视频下载器Pro/
├── start.bat                 # 程序启动脚本
├── youtube_downloader.py     # 主程序文件
├── yt-dlp.exe               # YouTube下载核心工具
├── ffmpeg.exe               # 视频处理工具
├── ffprobe.exe              # 媒体信息分析工具
├── youtube.com_cookies.txt  # Cookies文件（可选）
├── README.md                # 项目说明文件
└── _internal/               # 内部依赖文件夹
    ├── python/              # Python运行环境
    └── 其他依赖文件...
```

## 功能特点

- 🎯 **简单易用**：双击[start.bat]即可启动程序
- 🌐 **多格式支持**：支持MP4、MKV、WebM等多种视频格式
- 🔧 **高质量下载**：自动选择最佳视频质量进行下载
- 📂 **自定义保存路径**：可选择视频保存位置，默认保存到桌面
- 🍪 **Cookies支持**：支持使用Cookies文件下载需要登录的视频
- 🌍 **无Cookies模式**：可选择不使用Cookies下载公开视频
- 📋 **右键粘贴**：在输入框中支持右键粘贴功能
- 📊 **进度显示**：实时显示下载进度和状态
- 🎬 **播放器兼容**：使用H.264+AAC编码确保视频在各种播放器中正常播放

## 系统要求

- Windows 7及以上版本
- 无需额外安装Python环境

## 安装与使用

### 1. 下载程序

从GitHub下载最新版本的程序包并解压到任意目录。

### ├── yt-dlp.exe ──             # YouTube下载核心工具
### ├── ffmpeg.exe  ──           # 视频处理工具
### ├── ffprobe.exe ──         # 媒体信息分析工具

以上三个文件需额外下载至项目根目录
1.  **yt-dlp**: Download from [https://github.com/yt-dlp/yt-dlp/releases](https://github.com/yt-dlp/yt-dlp/releases)
2.  **ffmpeg & ffprobe**: Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

### 2. 启动程序

双击[start.bat]文件启动程序。

### 3. 下载视频

1. 在"视频URL"输入框中粘贴YouTube视频链接（支持右键粘贴）
2. 选择保存路径（默认为桌面）
3. 点击"开始下载"按钮
4. 等待下载完成

## 高级功能

### Cookies设置

对于需要登录的视频，您需要提供YouTube的cookies文件：

1. 安装浏览器扩展"Get cookies.txt" 推荐火狐浏览器并登录
2. 登录YouTube账户
3. 使用扩展导出Cookie并保存为txt文件
4. 在程序界面中选择该文件路径

### 格式选择

程序支持多种输出格式：
- MP4（默认，兼容性最好）
- MKV（支持更多编码格式）
- WebM（Google开发的开放格式）

### 质量选择

程序会自动选择最佳质量下载，也可根据需要选择特定分辨率。

## 常见问题

### Q: 下载速度很慢怎么办？
A: 下载速度受多种因素影响：
- 网络连接质量
- YouTube服务器限制
- 同时下载的视频数量
- 是否使用了代理或VPN

### Q: 为什么某些视频无法下载？
A: 可能的原因包括：
- 视频受地区限制
- 视频需要登录才能观看
- Cookies文件已过期
- 视频已被删除或设为私有

### Q: 程序提示找不到文件怎么办？
A: 请确保以下文件在程序目录中：
- [youtube_downloader.py]
- [yt-dlp.exe]
- [start.bat]

## 技术说明

### 核心组件

- **yt-dlp**：基于youtube-dl的增强版下载工具
- **Python**：程序运行环境（已包含）
- **FFmpeg**：视频处理工具（用于格式转换）

### 编码规范

下载的视频使用H.264视频编码和AAC音频编码，这是最广泛支持的格式组合，确保在各种播放器中都能正常播放。

## 免责声明

本工具仅供个人学习和研究使用，请遵守相关法律法规，不要用于商业用途。下载受版权保护的内容可能违反当地法律，请在使用前了解相关法律规定。

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本的YouTube视频下载功能
- 支持Cookies认证
- 支持多种视频格式

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

本项目基于MIT许可证发布。
