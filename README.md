# PDF转长图工具

一个高效的PDF转长图转换工具，支持将PDF文件的所有页面转换为一个垂直拼接的长图文件。python 需要3.12.x版本。找了半天没发现适合的软件所以才临时做了这个工具。

## 功能特性

- 🚀 高质量PDF页面转换
- 📏 可调节DPI和图片质量
- 🖼️ 支持PNG和JPEG输出格式
- 📐 支持最大宽度限制和自动缩放
- 🎨 提供命令行和GUI两种使用方式
- ⚡ 高效的内存管理和处理速度

## 安装依赖

```bash
pip install -r requirements_pdf.txt
```

或者手动安装：

```bash
pip install PyMuPDF>=1.23.0 Pillow>=10.0.0
```

## 使用方法

### 1. 命令行模式

#### 基本使用
```bash
python pdf_to_long_image.py document.pdf
```

#### 指定输出文件
```bash
python pdf_to_long_image.py document.pdf output.png
```

#### 调整参数
```bash
python pdf_to_long_image.py document.pdf output.jpg --dpi 200 --quality 90
```

#### 限制最大宽度
```bash
python pdf_to_long_image.py document.pdf --max-width 1200
```

#### 完整参数示例
```bash
python pdf_to_long_image.py document.pdf long_image.png --dpi 300 --quality 95 --max-width 1000
```

### 2. GUI界面模式

#### 方法1：使用启动脚本（推荐）
```bash
./run_gui.sh
```

#### 方法2：直接运行
```bash
python3 pdf_converter_gui.py
```

#### 方法3：设置环境变量（消除macOS警告）
```bash
export TK_SILENCE_DEPRECATION=1
python3 pdf_converter_gui.py
```

GUI界面提供：
- 文件选择对话框
- 参数设置界面
- 实时转换进度显示
- 转换日志查看
- 自动打开输出目录

## 参数说明

| 参数 | 说明 | 默认值 | 范围 |
|------|------|--------|------|
| `--dpi` | 图片分辨率DPI | 150 | 50-600 |
| `--quality` | JPEG质量 | 95 | 1-100 |
| `--max-width` | 最大宽度限制(像素) | 无限制 | 正整数 |

## 输出格式

- **PNG**: 无损压缩，适合需要高质量的场景
- **JPEG**: 有损压缩，文件较小，适合快速分享

## 性能优化建议

### DPI设置建议
- **预览/分享**: 150 DPI
- **打印/高质量**: 300 DPI
- **快速处理**: 100 DPI

### 内存优化
- 对于大型PDF，建议设置 `max-width` 参数限制宽度
- 系统内存较小时，可以降低DPI设置

### 文件大小控制
```bash
# 小文件（快速分享）
python pdf_to_long_image.py doc.pdf output.jpg --dpi 100 --quality 80 --max-width 800

# 中等质量（平衡大小和质量）
python pdf_to_long_image.py doc.pdf output.png --dpi 150 --max-width 1200

# 高质量（打印/存档）
python pdf_to_long_image.py doc.pdf output.png --dpi 300
```

## 使用示例

### 示例1：文档快速预览
```bash
python pdf_to_long_image.py report.pdf --dpi 120 --max-width 800
```

### 示例2：高质量存档
```bash
python pdf_to_long_image.py important_doc.pdf archive.png --dpi 300 --quality 100
```

### 示例3：批量处理脚本
```bash
#!/bin/bash
for file in *.pdf; do
    python pdf_to_long_image.py "$file" "${file%.pdf}_长图.png" --dpi 150 --max-width 1000
done
```

## 错误处理

### macOS Tkinter弃用警告
如果在macOS上看到以下警告：
```
DEPRECATION WARNING: The system version of Tk is deprecated and may be removed in a future release. Please don't rely on it. Set TK_SILENCE_DEPRECATION=1 to suppress this warning.
```

**解决方案**：
1. 使用提供的启动脚本：`./run_gui.sh`
2. 或设置环境变量：`export TK_SILENCE_DEPRECATION=1`

### 其他常见错误和解决方案：

### 1. 文件不存在
```
❌ 错误：PDF文件不存在: xxx.pdf
```
**解决**：检查文件路径是否正确

### 2. 内存不足
```
❌ 转换过程中出现错误: 内存不足
```
**解决**：降低DPI或设置max-width参数

### 3. 权限错误
```
❌ 转换过程中出现错误: 权限被拒绝
```
**解决**：检查输出目录的写入权限

### 4. PDF文件损坏
```
❌ 转换过程中出现错误: 无法打开PDF文件
```
**解决**：检查PDF文件是否完整或尝试修复

## 技术细节

### 核心技术栈
- **PyMuPDF (fitz)**: PDF解析和页面渲染
- **Pillow (PIL)**: 图像处理和拼接
- **tkinter**: GUI界面（可选）

### 处理流程
1. 解析PDF文件结构
2. 逐页渲染为高质量图像
3. 计算最优拼接尺寸
4. 垂直拼接所有页面
5. 优化并保存最终图像

### 内存管理
- 采用逐页处理避免内存溢出
- 自动释放临时图像数据
- 支持大型PDF文件处理

## 许可证

MIT License

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本PDF转长图功能
- 提供命令行和GUI界面
- 支持DPI、质量、宽度限制等参数调节 
