import re

class delete_unuse_space:
    def __init__(self, content, arguments):
        self.content = content
        self.content_new = []
        self.arguments = arguments

    def run(self):
        for i in range(len(self.content)):
            if not re.search(r"^\-", self.content[i]):
                temp = self.content[i].replace("\t", "")
                temp = self.content[i].replace(temp, "")
                self.content[i] = self.content[i].replace("\t", "")
                while re.search(r"^ ", self.content[i]):
                    self.content[i] = re.sub(r"^\W", "", self.content[i], count=1)
                self.content_new.append(temp + self.content[i])
            else:
                self.content_new.append(self.content[i])

    def output(self):
        return self.content_new