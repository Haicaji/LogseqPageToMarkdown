import re

class change_image_link:
    def __init__(self, content, arguments):
        self.content = content
        self.content_new = []
        self.link_father = arguments['link_father']

    def run(self):
        for line in self.content:
            if re.search(r'(\!\[.*\]\()(\.\.)(\/assets\/.*\))', line):
                if re.search(r'\{:height \d+, :width \d+\}', line):
                    line = re.sub(r'\{:height \d+, :width \d+\}', '', line)
                line = re.sub(r'(\!\[.*\]\()(\.\.)(\/assets\/.*\))', r'\1' + self.link_father + r'\3', line)
            self.content_new.append(line)

    def output(self):
        return self.content_new