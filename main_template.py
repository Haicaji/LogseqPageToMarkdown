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
        "delete_properties": [True, None], # 删除Logseq属性
        "add_heading": [True, None],
        "change_image_link": [False, {"link_father": "https://myLogseq.github.io"}],
        "change_image_to_base64": [True, {"graphs_path": r"D:\\GraphsFile\\"}],
    }

    for tool_name, [use, arguments] in tool_dict.items():
        if use:
            content = use_tool(content, tool_name, arguments)

        write_file(output_md, content)

if __name__ == "__main__":
    main()