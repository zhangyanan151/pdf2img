#!/usr/bin/env python3
"""
PDF转长图 GUI工具 - 简化版本
提供图形界面的PDF转长图转换工具
"""

import os
# 设置环境变量来消除macOS Tkinter弃用警告
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from pdf_to_long_image import pdf_to_long_image


class PDFConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF转长图工具")
        self.root.geometry("700x600")
        self.root.minsize(600, 500)
        
        # 设置样式
        try:
            style = ttk.Style()
            style.theme_use('clam')
        except:
            pass  # 如果主题不可用，使用默认主题
        
        self.setup_ui()
        
    def setup_ui(self):
        # 创建主容器
        main_container = tk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题
        title_label = tk.Label(main_container, text="PDF转长图工具", 
                              font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # 文件选择区域
        file_frame = tk.LabelFrame(main_container, text="文件选择", padx=10, pady=10)
        file_frame.pack(fill='x', pady=(0, 15))
        
        # PDF文件选择
        pdf_frame = tk.Frame(file_frame)
        pdf_frame.pack(fill='x', pady=5)
        tk.Label(pdf_frame, text="PDF文件:", width=12, anchor='w').pack(side='left')
        self.pdf_path_var = tk.StringVar()
        self.pdf_entry = tk.Entry(pdf_frame, textvariable=self.pdf_path_var)
        self.pdf_entry.pack(side='left', fill='x', expand=True, padx=(5, 5))
        tk.Button(pdf_frame, text="浏览", command=self.browse_pdf).pack(side='right')
        
        # 输出文件选择
        output_frame = tk.Frame(file_frame)
        output_frame.pack(fill='x', pady=5)
        tk.Label(output_frame, text="输出文件:", width=12, anchor='w').pack(side='left')
        self.output_path_var = tk.StringVar()
        self.output_entry = tk.Entry(output_frame, textvariable=self.output_path_var)
        self.output_entry.pack(side='left', fill='x', expand=True, padx=(5, 5))
        tk.Button(output_frame, text="浏览", command=self.browse_output).pack(side='right')
        
        # 设置区域
        settings_frame = tk.LabelFrame(main_container, text="转换设置", padx=10, pady=10)
        settings_frame.pack(fill='x', pady=(0, 15))
        
        # 第一行设置
        settings_row1 = tk.Frame(settings_frame)
        settings_row1.pack(fill='x', pady=5)
        
        # DPI设置
        tk.Label(settings_row1, text="DPI:", width=8).pack(side='left')
        self.dpi_var = tk.IntVar(value=150)
        dpi_spin = tk.Spinbox(settings_row1, from_=50, to=600, textvariable=self.dpi_var, width=8)
        dpi_spin.pack(side='left', padx=(0, 20))
        
        # 质量设置
        tk.Label(settings_row1, text="JPEG质量:", width=10).pack(side='left')
        self.quality_var = tk.IntVar(value=95)
        quality_spin = tk.Spinbox(settings_row1, from_=1, to=100, textvariable=self.quality_var, width=8)
        quality_spin.pack(side='left')
        
        # 第二行设置
        settings_row2 = tk.Frame(settings_frame)
        settings_row2.pack(fill='x', pady=5)
        
        # 最大宽度设置
        tk.Label(settings_row2, text="最大宽度:", width=8).pack(side='left')
        self.max_width_var = tk.StringVar()
        width_entry = tk.Entry(settings_row2, textvariable=self.max_width_var, width=10)
        width_entry.pack(side='left', padx=(0, 10))
        tk.Label(settings_row2, text="(像素，留空不限制)").pack(side='left')
        
        # 转换按钮
        button_frame = tk.Frame(main_container)
        button_frame.pack(fill='x', pady=(0, 15))
        self.convert_button = tk.Button(button_frame, text="开始转换", 
                                       command=self.start_conversion,
                                       bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'),
                                       padx=20, pady=10)
        self.convert_button.pack()
        
        # 进度条
        self.progress = ttk.Progressbar(main_container, mode='indeterminate')
        self.progress.pack(fill='x', pady=(0, 10))
        
        # 状态标签
        self.status_var = tk.StringVar(value="请选择PDF文件开始转换")
        self.status_label = tk.Label(main_container, textvariable=self.status_var, 
                                    font=('Arial', 10))
        self.status_label.pack(pady=(0, 10))
        
        # 日志区域
        log_frame = tk.LabelFrame(main_container, text="转换日志", padx=10, pady=10)
        log_frame.pack(fill='both', expand=True)
        
        # 创建滚动文本框
        log_container = tk.Frame(log_frame)
        log_container.pack(fill='both', expand=True)
        
        self.log_text = tk.Text(log_container, height=8, wrap='word')
        scrollbar = tk.Scrollbar(log_container, orient='vertical', command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def browse_pdf(self):
        """浏览PDF文件"""
        filename = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if filename:
            self.pdf_path_var.set(filename)
            # 自动生成输出文件名
            if not self.output_path_var.get():
                base_name = os.path.splitext(os.path.basename(filename))[0]
                output_path = os.path.join(os.path.dirname(filename), f"{base_name}_长图.png")
                self.output_path_var.set(output_path)
    
    def browse_output(self):
        """浏览输出文件"""
        filename = filedialog.asksaveasfilename(
            title="保存长图文件",
            defaultextension=".png",
            filetypes=[("PNG文件", "*.png"), ("JPEG文件", "*.jpg"), ("所有文件", "*.*")]
        )
        if filename:
            self.output_path_var.set(filename)
    
    def log_message(self, message):
        """添加日志消息"""
        self.log_text.insert('end', message + "\n")
        self.log_text.see('end')
        self.root.update_idletasks()
    
    def start_conversion(self):
        """开始转换"""
        pdf_path = self.pdf_path_var.get().strip()
        if not pdf_path:
            messagebox.showerror("错误", "请选择PDF文件")
            return
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("错误", "PDF文件不存在")
            return
        
        output_path = self.output_path_var.get().strip()
        if not output_path:
            messagebox.showerror("错误", "请设置输出文件路径")
            return
        
        # 获取设置参数
        dpi = self.dpi_var.get()
        quality = self.quality_var.get()
        max_width = self.max_width_var.get().strip()
        max_width = int(max_width) if max_width else None
        
        # 清空日志
        self.log_text.delete(1.0, 'end')
        
        # 禁用转换按钮，启动进度条
        self.convert_button.configure(state='disabled')
        self.progress.start()
        self.status_var.set("正在转换中...")
        
        # 在新线程中执行转换
        thread = threading.Thread(
            target=self.convert_pdf,
            args=(pdf_path, output_path, dpi, quality, max_width)
        )
        thread.daemon = True
        thread.start()
    
    def convert_pdf(self, pdf_path, output_path, dpi, quality, max_width):
        """执行PDF转换"""
        try:
            # 重定向输出到日志
            import sys
            from io import StringIO
            
            old_stdout = sys.stdout
            
            class LogRedirector:
                def __init__(self, gui):
                    self.gui = gui
                
                def write(self, text):
                    if text.strip():
                        self.gui.root.after(0, lambda t=text.strip(): self.gui.log_message(t))
                
                def flush(self):
                    pass
            
            # 设置日志重定向
            log_redirector = LogRedirector(self)
            sys.stdout = log_redirector
            
            # 执行转换
            result_path = pdf_to_long_image(
                pdf_path=pdf_path,
                output_path=output_path,
                dpi=dpi,
                quality=quality,
                max_width=max_width
            )
            
            # 恢复标准输出
            sys.stdout = old_stdout
            
            # 转换成功
            self.root.after(0, lambda: self.conversion_completed(result_path))
            
        except Exception as e:
            # 恢复标准输出
            sys.stdout = old_stdout
            self.root.after(0, lambda: self.conversion_failed(str(e)))
    
    def conversion_completed(self, result_path):
        """转换完成"""
        self.progress.stop()
        self.convert_button.configure(state='normal')
        self.status_var.set("转换完成！")
        
        self.log_message(f"\n🎉 转换成功完成！")
        self.log_message(f"输出文件: {os.path.abspath(result_path)}")
        
        # 询问是否打开输出目录
        if messagebox.askyesno("转换完成", f"转换成功完成！\n\n输出文件: {result_path}\n\n是否打开文件所在目录？"):
            import subprocess
            import platform
            
            try:
                if platform.system() == "Windows":
                    subprocess.run(["explorer", "/select,", result_path])
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", "-R", result_path])
                else:  # Linux
                    subprocess.run(["xdg-open", os.path.dirname(result_path)])
            except Exception as e:
                self.log_message(f"无法打开目录: {str(e)}")
    
    def conversion_failed(self, error_message):
        """转换失败"""
        self.progress.stop()
        self.convert_button.configure(state='normal')
        self.status_var.set("转换失败")
        
        self.log_message(f"\n❌ 转换失败: {error_message}")
        messagebox.showerror("转换失败", f"转换过程中出现错误:\n\n{error_message}")


def main():
    root = tk.Tk()
    app = PDFConverterGUI(root)
    
    # 添加退出处理
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main() 