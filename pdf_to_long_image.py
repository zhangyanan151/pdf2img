#!/usr/bin/env python3
"""
PDF转长图工具
支持将PDF文件转换为一个垂直拼接的长图文件

使用方法:
python pdf_to_long_image.py input.pdf [output.png] [--dpi 150] [--quality 95]
"""

import fitz  # PyMuPDF
import argparse
import os
from PIL import Image
import sys


def pdf_to_long_image(pdf_path, output_path=None, dpi=150, quality=95, max_width=None):
    """
    将PDF文件转换为长图
    
    Args:
        pdf_path (str): PDF文件路径
        output_path (str): 输出图片路径，如果为None则自动生成
        dpi (int): 图片DPI，默认150
        quality (int): JPEG质量，默认95
        max_width (int): 最大宽度限制，如果设置则会按比例缩放
    
    Returns:
        str: 输出文件路径
    """
    
    # 检查输入文件是否存在
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
    
    # 生成输出文件名
    if output_path is None:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = f"{base_name}_长图.png"
    
    print(f"正在处理PDF文件: {pdf_path}")
    print(f"输出路径: {output_path}")
    print(f"DPI设置: {dpi}")
    
    try:
        # 打开PDF文件
        pdf_document = fitz.open(pdf_path)
        total_pages = len(pdf_document)
        print(f"PDF总页数: {total_pages}")
        
        # 存储所有页面的图片
        page_images = []
        
        # 计算缩放因子 (DPI/72，因为PDF默认72DPI)
        zoom_factor = dpi / 72.0
        matrix = fitz.Matrix(zoom_factor, zoom_factor)
        
        # 逐页转换
        for page_num in range(total_pages):
            print(f"正在处理第 {page_num + 1}/{total_pages} 页...")
            
            page = pdf_document[page_num]
            
            # 将页面转换为图片
            pix = page.get_pixmap(matrix=matrix)
            img_data = pix.tobytes("png")
            
            # 转换为PIL Image
            img = Image.open(fitz.io.BytesIO(img_data))
            
            # 如果设置了最大宽度限制，则按比例缩放
            if max_width and img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                print(f"  页面已缩放至: {max_width}x{new_height}")
            
            page_images.append(img)
        
        pdf_document.close()
        
        # 计算长图的总尺寸
        if not page_images:
            raise ValueError("没有成功转换任何页面")
        
        # 使用第一页的宽度作为基准宽度
        base_width = page_images[0].width
        total_height = sum(img.height for img in page_images)
        
        print(f"长图尺寸: {base_width}x{total_height}")
        
        # 创建长图画布
        long_image = Image.new('RGB', (base_width, total_height), 'white')
        
        # 拼接所有页面
        current_y = 0
        for i, img in enumerate(page_images):
            print(f"正在拼接第 {i + 1} 页...")
            
            # 如果页面宽度不一致，居中放置
            if img.width != base_width:
                x_offset = (base_width - img.width) // 2
            else:
                x_offset = 0
            
            long_image.paste(img, (x_offset, current_y))
            current_y += img.height
        
        # 保存长图
        print("正在保存长图...")
        
        # 根据文件扩展名选择保存格式
        file_ext = os.path.splitext(output_path)[1].lower()
        
        if file_ext in ['.jpg', '.jpeg']:
            long_image.save(output_path, 'JPEG', quality=quality, optimize=True)
        elif file_ext == '.png':
            long_image.save(output_path, 'PNG', optimize=True)
        else:
            # 默认保存为PNG
            output_path = os.path.splitext(output_path)[0] + '.png'
            long_image.save(output_path, 'PNG', optimize=True)
        
        print(f"✅ 转换完成！")
        print(f"输出文件: {output_path}")
        print(f"文件大小: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
        
        return output_path
        
    except Exception as e:
        print(f"❌ 转换过程中出现错误: {str(e)}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="将PDF文件转换为垂直拼接的长图",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python pdf_to_long_image.py document.pdf
  python pdf_to_long_image.py document.pdf output.png --dpi 200
  python pdf_to_long_image.py document.pdf --max-width 1200 --quality 90
        """
    )
    
    parser.add_argument('pdf_path', help='PDF文件路径')
    parser.add_argument('output_path', nargs='?', help='输出图片路径（可选，默认自动生成）')
    parser.add_argument('--dpi', type=int, default=150, help='图片DPI（默认: 150）')
    parser.add_argument('--quality', type=int, default=95, help='JPEG质量 1-100（默认: 95）')
    parser.add_argument('--max-width', type=int, help='最大宽度限制（像素）')
    
    args = parser.parse_args()
    
    # 验证参数
    if args.quality < 1 or args.quality > 100:
        print("❌ 错误：质量参数必须在1-100之间")
        sys.exit(1)
    
    if args.dpi < 50 or args.dpi > 600:
        print("❌ 错误：DPI参数建议在50-600之间")
        sys.exit(1)
    
    try:
        output_file = pdf_to_long_image(
            pdf_path=args.pdf_path,
            output_path=args.output_path,
            dpi=args.dpi,
            quality=args.quality,
            max_width=args.max_width
        )
        
        print(f"\n🎉 转换成功完成！")
        print(f"输出文件: {os.path.abspath(output_file)}")
        
    except Exception as e:
        print(f"\n❌ 转换失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 