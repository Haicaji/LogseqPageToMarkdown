import re

class add_heading:
    def __init__(self, content, arguments):
        self.content = content
        self.content_new = []
        self.arguments = arguments

    def run(self):
        pattern_heading = r'heading::\s+(true|false)'
        for i in range(len(self.content)):
            if re.search(pattern_heading, self.content[i]):
                temp = self.content_new[-1].replace("\t", "")
                temp_ = re.sub(r"^\-", "#", temp, count=1)
                self.content_new[-1] = self.content_new[-1].replace(temp, temp_)
            else:
                self.content_new.append(self.content[i])

        self.content = self.content_new
        self.content_new = []

        beforce_title_count = 0
        for i in range(len(self.content)):
            indent_count = self.count_indent(self.content[i])
            if re.search(r'^#', self.content[i].replace("\t", "")):
                beforce_title_count += 1
                self.content[i] = self.content[i].replace(indent_count*"\t"+"#", "#"*(indent_count+1))
                self.content_new.append(self.content[i])
                self.content_new.append("\n")
            else:
                if beforce_title_count > indent_count:
                    beforce_title_count -= 1
                self.content[i] = self.content[i].replace(beforce_title_count*"\t", "", 1)
                self.content_new.append(self.content[i])
    
    # 判断缩进数量
    def count_indent(self, line):
        count = 0
        for char in line:
            if char == "\t":
                count += 1
            else:
                break
        return count

    def output(self):
        return self.content_new