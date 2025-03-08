class delete_alone_hyphen:
    def __init__(self, content, arguments):
        self.content = content
        self.content_new = []
        self.arguments = arguments

    def run(self):
        for line in self.content:
            stripped_line = line.strip()
            if stripped_line != "-":
                self.content_new.append(line)

    def output(self):
        return self.content_new