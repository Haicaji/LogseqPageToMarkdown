import tools
import importlib

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(content)

def use_tool(content, tool_name, arguments):
    module = importlib.import_module(f"tools.{tool_name}")
    tool_class = getattr(module, tool_name)
    tool_instance = tool_class(content, arguments)
    tool_instance.run()
    # 返回处理后的内容
    return tool_instance.output()

def main():
    input_md = "input.md"
    output_md = "output.md"

    content = read_file(input_md)
    
    tool_dict = {
        "delete_properties": [True, None],
        "add_heading": [True, None],
        "delete_unuse_space": [True, None],
        "delete_alone_hyphen": [True, None],
    }

    for tool_name, [use, arguments] in tool_dict.items():
        if use:
            content = use_tool(content, tool_name, arguments)

    write_file(output_md, content)

if __name__ == "__main__":
    main()