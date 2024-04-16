from pprint import pprint
def parse_file_and_log(filename):
    # 用于存储符合条件的行的列表
    matched_lines = []
    
    # 打开文本文件以读取内容
    with open(filename, 'r') as file:
        # 打开 log 文件以写入符合条件的行
        with open('log.txt', 'w') as log_file:
            # 当前正在处理的行
            current_line = ''
            # 逐行读取文本文件内容
            for line in file:
                # 拼接当前行和下一行
                current_line += line.strip()
                # 如果当前行包含 'function' 字符串
                if line.strip().startswith('function') and ';' not in current_line:
                    # 如果当前行不完整，继续读取下一行直到找到完整的行
                    while '(' in current_line and '{' not in current_line:
                        next_line = next(file).strip()
                        current_line += ' '
                        current_line += next_line
                    # matched_lines.append(current_line.rstrip('{'))  
                    matched_lines.append(current_line.rstrip('{'))  
                # 重置当前行
                current_line = ''
    
    # 返回符合条件的行的列表
    return matched_lines


# 使用示例
filename = '/home/foxing/contract_database/foxing/bsc-contract-database/2024-04-16/0xFFa47257A7D682614Bd00061F1Af29e49eD18d28.sol'
matched_lines = parse_file_and_log(filename)
for i in matched_lines:
    print(i)    
