import re
import base64
from os import path

class change_image_to_base64:
    def __init__(self, content, arguments):
        self.content = content
        self.content_new = []
        self.graphs_path = arguments['graphs_path']
        self.images_base64_content = []

    def run(self):
        for line in self.content:
            if re.search(r'(\!\[.*\]\()(\.\.)(\/assets\/.*\))', line):
                if re.search(r'\{:height \d+, :width \d+\}', line):
                    line = re.sub(r'\{:height \d+, :width \d+\}', '', line)

                pattern = r'!\[(.*?)\]\(\.\./(.*?)\)'
                def replacer(match):
                    alt_text = match.group(1)          # alt text
                    relative_path = match.group(2)     # 去掉 ../ 的路径
                    return f'![{alt_text}][{relative_path}]'
                line = re.sub(pattern, replacer, line)
                
                image_path = re.search(r'!\[.*?\]\[(.*?)\]', line).group(1)
                self.images_base64_content.append(self.imageToBase64(image_path))
            self.content_new.append(line)
        for image_base64 in self.images_base64_content:
            self.content_new.append(image_base64 + '\n')

    def output(self):
        return self.content_new
    
    def imageToBase64(self, image_path):
        with open(self.graphs_path + image_path, 'rb') as file:
            # 读取图片文件
            image_data = file.read()

            # base64 前面跟着的文件扩展名似乎对于 Markdown 渲染没有影响, 就不判断了, 默认png
            # suffix = self.get_suffix()
            head_txt = f"[{image_path}]:data:image/png;base64,"

            # 将图片数据编码为 Base64 字符串
            base64_str = base64.b64encode(image_data).decode('utf-8')
            
            return head_txt + base64_str
        
    def get_suffix(self):
        '''判断图片类型'''
        