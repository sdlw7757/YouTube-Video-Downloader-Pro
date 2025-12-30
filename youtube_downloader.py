import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import threading
import re
import sys

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube视频下载器")
        self.root.geometry("800x500")
        self.root.resizable(True, True)
        
        # 设置中文字体支持
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("SimHei", 10))
        self.style.configure("TButton", font=("SimHei", 10))
        self.style.configure("TEntry", font=("SimHei", 10))
        
        # 变量初始化
        self.url_var = tk.StringVar()
        # 设置默认保存路径为桌面
        self.save_path_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Desktop"))
        self.quality_var = tk.StringVar(value="最佳质量")
        self.yt_dlp_path_var = tk.StringVar(value=os.path.join(os.getcwd(), "yt-dlp.exe"))
        self.cookies_path_var = tk.StringVar(value=os.path.join(os.getcwd(), "youtube.com_cookies.txt"))
        # 添加更好的编码兼容性选项变量
        self.compat_encoding_var = tk.BooleanVar(value=True)
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="就绪")
        # 添加format_var变量定义
        self.format_var = tk.StringVar(value="mp4")
        
        self.create_widgets()
        
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL输入
        ttk.Label(main_frame, text="视频URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=60)
        url_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        # 添加右键菜单以支持粘贴功能
        self.add_context_menu(url_entry)
        
        # yt-dlp路径设置
        ttk.Label(main_frame, text="yt-dlp路径:").grid(row=1, column=0, sticky=tk.W, pady=5)
        yt_dlp_entry = ttk.Entry(main_frame, textvariable=self.yt_dlp_path_var, width=50)
        yt_dlp_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        self.add_context_menu(yt_dlp_entry)
        
        yt_dlp_btn = ttk.Button(main_frame, text="浏览...", command=self.browse_yt_dlp_path)
        yt_dlp_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # Cookies路径设置
        ttk.Label(main_frame, text="Cookies路径:").grid(row=2, column=0, sticky=tk.W, pady=5)
        cookies_entry = ttk.Entry(main_frame, textvariable=self.cookies_path_var, width=50)
        cookies_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)
        self.add_context_menu(cookies_entry)
        
        cookies_btn = ttk.Button(main_frame, text="浏览...", command=self.browse_cookies_path)
        cookies_btn.grid(row=2, column=2, padx=5, pady=5)
        
        # 无Cookie下载选项
        self.no_cookies_var = tk.BooleanVar()
        no_cookies_check = ttk.Checkbutton(main_frame, text="不使用Cookies下载（可能无法下载某些视频）", variable=self.no_cookies_var)
        no_cookies_check.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Cookie帮助按钮
        cookie_help_btn = ttk.Button(main_frame, text="Cookie帮助", command=self.show_cookie_help)
        cookie_help_btn.grid(row=3, column=2, padx=5, pady=5)
        
        # 添加更好的编码兼容性选项
        compat_encoding_check = ttk.Checkbutton(main_frame, text="使用更好的编码兼容性（推荐）", variable=self.compat_encoding_var)
        compat_encoding_check.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # 保存路径
        ttk.Label(main_frame, text="保存路径:").grid(row=5, column=0, sticky=tk.W, pady=5)
        path_entry = ttk.Entry(main_frame, textvariable=self.save_path_var, width=50)
        path_entry.grid(row=5, column=1, sticky=tk.EW, pady=5)
        self.add_context_menu(path_entry)
        
        browse_btn = ttk.Button(main_frame, text="浏览...", command=self.browse_save_path)
        browse_btn.grid(row=5, column=2, padx=5, pady=5)
        
        # 添加格式选择
        ttk.Label(main_frame, text="输出格式:").grid(row=6, column=0, sticky=tk.W, pady=5)
        format_combo = ttk.Combobox(main_frame, textvariable=self.format_var, values=["mp4", "mkv", "webm"], width=10, state="readonly")
        format_combo.grid(row=6, column=1, sticky=tk.W, pady=5)
        
        # 下载按钮
        download_btn = ttk.Button(main_frame, text="开始下载", command=self.start_download)
        download_btn.grid(row=7, column=1, pady=20)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress.grid(row=8, column=0, columnspan=3, sticky=tk.EW, pady=5)
        
        # 进度百分比标签
        self.progress_label = ttk.Label(main_frame, text="0%")
        self.progress_label.grid(row=9, column=1, pady=5)
        
        # 状态标签
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=10, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # 日志文本框
        self.log_text = tk.Text(main_frame, height=10, width=80)
        self.log_text.grid(row=11, column=0, columnspan=3, sticky=tk.EW, pady=5)
        
        # 配置列权重以适应窗口大小变化
        main_frame.columnconfigure(1, weight=1)
        
    def add_context_menu(self, widget):
        """为控件添加右键菜单以支持粘贴功能"""
        context_menu = tk.Menu(widget, tearoff=0)
        context_menu.add_command(label="粘贴", command=lambda: widget.event_generate("<<Paste>>"))
        context_menu.add_command(label="复制", command=lambda: widget.event_generate("<<Copy>>"))
        context_menu.add_command(label="剪切", command=lambda: widget.event_generate("<<Cut>>"))
        
        def show_context_menu(event):
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
                
        widget.bind("<Button-3>", show_context_menu)  # Windows中右键是Button-3
    
    def browse_yt_dlp_path(self):
        """选择yt-dlp.exe路径"""
        file_path = filedialog.askopenfilename(
            title="选择yt-dlp可执行文件",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")]
        )
        if file_path:
            self.yt_dlp_path_var.set(file_path)
    
    def browse_cookies_path(self):
        """选择cookies文件路径"""
        file_path = filedialog.askopenfilename(
            title="选择cookies文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.cookies_path_var.set(file_path)
    
    def browse_save_path(self):
        """选择保存路径"""
        directory = filedialog.askdirectory()
        if directory:
            self.save_path_var.set(directory)
    
    def log(self, message):
        """在日志区域显示消息"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
    
    def update_progress(self, percentage):
        """更新进度条"""
        self.progress_var.set(percentage)
        # 更新进度百分比标签
        self.progress_label.config(text=f"{int(percentage)}%")
        self.root.update_idletasks()
    
    def update_status(self, status):
        """更新状态文本"""
        self.status_var.set(status)
        self.log(status)
    
    def is_valid_youtube_url(self, url):
        """验证YouTube URL是否有效"""
        youtube_patterns = [
            r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'https?://youtu\.be/[\w-]+',
            r'https?://(?:www\.)?youtube\.com/embed/[\w-]+'
        ]
        for pattern in youtube_patterns:
            if re.match(pattern, url):
                return True
        return False
    
    def start_download(self):
        """开始下载过程"""
        url = self.url_var.get().strip()
        save_path = self.save_path_var.get().strip()
        quality = self.quality_var.get()
        yt_dlp_path = self.yt_dlp_path_var.get().strip()
        cookies_path = self.cookies_path_var.get().strip()
        output_format = self.format_var.get()
        
        # 验证输入
        if not url:
            messagebox.showerror("错误", "请输入视频URL")
            return
        
        if not self.is_valid_youtube_url(url):
            messagebox.showerror("错误", "请输入有效的YouTube URL")
            return
        
        if not save_path or not os.path.isdir(save_path):
            messagebox.showerror("错误", "请选择有效的保存路径")
            return
            
        if not yt_dlp_path or not os.path.isfile(yt_dlp_path):
            messagebox.showerror("错误", "请指定有效的yt-dlp.exe路径")
            return
            
        if not cookies_path or not os.path.isfile(cookies_path):
            messagebox.showerror("错误", "请指定有效的cookies文件路径")
            return
        
        # 重置进度条和日志
        self.progress_var.set(0)
        self.progress_label.config(text="0%")
        self.log_text.delete(1.0, tk.END)
        
        # 在新线程中开始下载，避免UI冻结
        threading.Thread(
            target=self.download_video, 
            args=(url, save_path, quality, yt_dlp_path, cookies_path, output_format), 
            daemon=True
        ).start()
    
    def download_video(self, url, save_path, quality, yt_dlp_path, cookies_path, output_format):
        """执行下载命令"""
        try:
            # 构建yt-dlp命令
            cmd = [
                yt_dlp_path,  # 使用指定路径的yt-dlp
                '--no-playlist',  # 只下载单个视频
                '-o', f'{save_path}/%(title)s.%(ext)s',  # 输出路径和文件名格式
            ]
            
            # 根据是否使用cookies来添加参数
            if not self.no_cookies_var.get():
                if os.path.isfile(cookies_path):
                    cmd.extend(['--cookies', cookies_path])  # 使用指定路径的cookies文件
                    self.update_status("信息: 使用Cookies文件进行身份验证")
                else:
                    self.update_status("警告: Cookies文件不存在，将尝试无Cookie下载")
                    cmd.extend(['--no-check-certificate'])  # 跳过证书检查
            else:
                self.update_status("信息: 已选择不使用Cookies下载")
                cmd.extend(['--no-check-certificate'])  # 跳过证书检查
            
            # 添加更好的播放器兼容性参数
            # 使用H.264视频编码和AAC音频编码，这是最广泛支持的格式
            cmd.extend(['--recode-video', 'mp4'])
            cmd.extend(['--postprocessor-args', '-c:v libx264 -c:a aac -strict experimental'])
            
            # 根据质量选择添加格式参数
            if quality == "最佳质量":
                # 使用兼容性更好的格式
                cmd.extend(['-f', 'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4][vcodec^=avc1]/best[ext=mp4]/best'])
            else:
                res = quality.replace('p', '')
                cmd.extend([
                    '-f', 
                    f'bestvideo[height<={res}][ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[height<={res}][ext=mp4][vcodec^=avc1]/best[height<={res}][ext=mp4]/best[height<={res}]'
                ])
            
            # 添加URL
            cmd.append(url)
            
            self.update_status(f"开始下载: {url}")
            self.update_status(f"保存路径: {save_path}")
            self.update_status(f"质量选择: {quality}")
            self.update_status(f"输出格式: {output_format}")
            self.update_status("信息: 使用H.264+AAC编码以提高播放器兼容性")
            
            # 如果不使用cookies，添加额外信息
            if self.no_cookies_var.get() or not os.path.isfile(cookies_path):
                self.update_status("注意: 不使用Cookies可能无法下载某些受限制的视频")
            
            # 执行命令并捕获输出
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # 处理输出，更新进度
            cookie_error_count = 0
            
            # 检查process.stdout是否有效
            if process.stdout is not None:
                for line in process.stdout:
                    self.log(line.strip())
                    
                    # 检查Cookie错误
                    if "The provided YouTube account cookies are no longer valid" in line or "Sign in to confirm you're not a bot" in line:
                        cookie_error_count += 1
                        if cookie_error_count == 1:  # 只显示一次提示
                            self.update_status("错误: YouTube Cookie已失效，请更新Cookie文件或选择不使用Cookie下载")
                    
                    # 尝试从输出中提取进度信息
                    progress_match = re.search(r'(\d+\.\d+)%', line)
                    if progress_match:
                        progress = float(progress_match.group(1))
                        self.update_progress(progress)
                    
                    # 检查是否下载完成
                    if 'has already been downloaded' in line:
                        self.update_progress(100)
                        self.update_status("视频已存在，无需重复下载")
                        break
                    
                    if '100%' in line:
                        self.update_progress(100)
            else:
                self.update_status("警告: 无法获取命令输出")
            
            # 等待进程完成
            process.wait()
            
            # 确保进度条显示100%
            self.update_progress(100)
            
            if process.returncode == 0:
                self.update_status("下载完成!")
                messagebox.showinfo("成功", f"视频已成功下载到:\n{save_path}")
            else:
                error_msg = f"下载失败，返回代码: {process.returncode}"
                self.update_status(error_msg)
                
                # 如果是Cookie错误，提供额外帮助
                if cookie_error_count > 0:
                    messagebox.showerror("失败", "下载过程中出现Cookie验证错误。\n\n请尝试以下解决方案：\n1. 更新Cookie文件\n2. 勾选'不使用Cookies下载'选项\n3. 点击'Cookie帮助'按钮获取更多信息")
                else:
                    messagebox.showerror("失败", "下载过程中出现错误，请查看日志了解详情")
                
        except Exception as e:
            error_msg = f"下载出错: {str(e)}"
            self.update_status(error_msg)
            messagebox.showerror("错误", error_msg)
    
    def check_ffmpeg_available(self):
        """检查系统是否安装了ffmpeg"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL,
                          check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def show_cookie_help(self):
        """显示关于Cookie问题的帮助信息"""
        help_text = """YouTube Cookie 问题解决方案:

1. Cookie失效是正常现象，因为YouTube会定期更新Cookie以提高安全性。

2. 解决方法：
   a. 使用浏览器扩展程序导出新的Cookie：
      - 安装 "Get cookies.txt" 扩展（Chrome/Edge/Firefox）
      - 登录YouTube账户
      - 使用扩展导出Cookie并保存为txt文件
      - 在本程序中选择该Cookie文件

   b. 不使用Cookie下载（适用于公开视频）：
      - 勾选"不使用Cookies下载"选项
      - 注意：某些视频可能需要登录才能下载

3. 如果仍然遇到问题：
   - 确保Cookie文件是最新的
   - 检查视频是否在您的地区可用
   - 尝试使用不同的网络连接

更多信息请参考：https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies
"""
        messagebox.showinfo("Cookie 帮助", help_text)

if __name__ == "__main__":
    # 确保中文显示正常
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()