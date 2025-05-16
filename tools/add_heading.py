import re

class add_heading:
    def __init__(self, content, arguments):
        self.content = content
        self.content_new = []
        self.arguments = arguments

    def run(self):
        # 将一个块合并为一行
        temp_content = []
        for line in self.content:
            if line.replace('\t', '').startswith("-"):
                temp_content.append(line)
            else:
                if len(temp_content) > 0:
                    temp_content[-1] = temp_content[-1] + line
                else:
                    temp_content.append(line)
                    Exception("Error: The first line is not start with `-`")
        # 删除空白行
        self.content = []
        for line in temp_content:
            if '-' not in line:
                continue
            else:
                self.content.append(line)
        # 处理标题
        for i in range(self.content.__len__()):
            line = self.content[i]
            self.content[i] = self.deal_heading(line, self.count_indent(line))
        # 块级缩进处理
        delete_indent_count = -1
        for i in range(self.content.__len__()):
            if self.content[i][0] == '#':
                delete_indent_count = -1
            else:
                if delete_indent_count == -1:
                    delete_indent_count = self.count_indent(self.content[i])
                    self.content[i] = self.content[i].replace('\t', '', delete_indent_count)
                else:
                    if delete_indent_count <= self.count_indent(self.content[i]):
                        self.content[i] = self.content[i].replace('\t', '', delete_indent_count)
                    else:
                        delete_indent_count = self.count_indent(self.content[i])
                        self.content[i] = '\n---\n\n' + self.content[i].replace('\t', '', delete_indent_count)
        # 块间处理
        for i in range(self.content.__len__()):
            if self.content[i].replace('\t', '').startswith('-'):
                indent = self.count_indent(self.content[i])
                text = self.content[i].split('\n')
                for j in range(text.__len__()):
                    text[j] = '\t'*indent + text[j].lstrip('\t')+'\n'
                if text[0].replace('\n', '').replace('\t', '') == '-':
                    text[0] = text[0][:-1]
                    text[1] = text[1].lstrip('\t')[1:]
                self.content[i] = ''
                for t in text:
                    self.content[i] += t

        for line in self.content:
            self.content_new.append(line)
    
    def deal_heading(self, text, indent_count):
        if "heading:: true" in text:
            text = text.split("\n")[:-1]
            if "heading:: true" not in text[-1].replace('\t', ''):
                raise Exception("Error: The last line is not `heading:: true`")
            text = text[0]+'\n'
            text = re.sub(r'^\t+', '', text)
            text = re.sub(r'\-', '#'*(indent_count+1), text, 1)
            return text+'\n'
        else:
            return text

    # 获取 `-` 前 `\t` 数量
    def count_indent(self, line):
        count = 0
        for s in line:
            if s == '\t':

                count += 1
            elif s == '-':
                break
            else:
                raise Exception("Error: The line is not start with `-`")
        return count

    def output(self):
        return self.content_new
    
if __name__ == "__main__":
    input_md = "input.md"
    output_md = "output.md"

    with open(input_md, 'r') as file:
        content = file.readlines()

    tool_instance = add_heading(content, None)
    tool_instance.run()
    content_new = tool_instance.output()

    with open(output_md, 'w', encoding='utf-8') as file:
        file.writelines(content_new)
