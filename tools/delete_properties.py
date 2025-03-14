import re

class delete_properties:
    def __init__(self, content, arguments):
        self.content = content
        self.content_new = []
        self.arguments = arguments

    def run(self):
        pattern_id = r'id::\s+[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        pattern_color = r'background-color::\s+(red|yellow|pink|green|blue|purple|gray)' # 背景颜色
        pattern_publish  = r'public::\s+(true|false)' # 公开
        pattern_collapsed = r'collapsed:: true' # 折叠
        pattern_list = [pattern_id, pattern_color, pattern_publish, pattern_collapsed]
        for line in self.content:
            flag = False
            for pattern in pattern_list:
                if re.search(pattern, line):
                    flag = True
                    break
            if flag:
                continue
            self.content_new.append(line)

    def output(self):
        return self.content_new