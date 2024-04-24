import mysql.connector

# 连接到数据库
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            # Your own database
        )
        # print("Connected to MySQL database")
        return connection
    except mysql.connector.Error as error:
        # print("Failed to connect to MySQL database:", error)
        return None

def parse_file_and_log(filename):
    # 用于存储符合条件的行的列表
    matched_lines = []
    
    # 打开文本文件以读取内容
    with open(filename, 'r') as file:
        # 打开 log 文件以写入符合条件的行
        with open('logzzzzz.txt', 'w') as log_file:
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

def extract_function_content(line):
    # 找到第一个空格的索引
    space_index = line.find(' ')
    if space_index == -1:
        return None  # 如果没有找到空格，则返回 None
    # 找到第一个左括号的索引
    parenthesis_index = line.find('(', space_index)
    if parenthesis_index == -1:
        return None  # 如果没有找到左括号，则返回 None
    # 提取空格和左括号之间的内容
    content = line[space_index + 1:parenthesis_index]
    return content

def extract_para_content(line):
    # 找到第一个左括号的索引
    start_index = line.find('(')
    if start_index == -1:
        return None  # 如果没有找到左括号，则返回 None
    # 找到第一个右括号的索引
    end_index = line.find(')', start_index)
    if end_index == -1:
        return None  # 如果没有找到右括号，则返回 None
    # 提取左括号和右括号之间的内容
    content = line[start_index + 1:end_index]
    return content.strip()  # 去除内容两边的空格

def extract_visable_content(line):
    # 查找是否存在'returns'单词
    returns_index = line.find('returns')
    # print(f'returns_inde-{returns_index}')
    # 如果存在'returns'单词
    if returns_index != -1:
        # 找到第一个右括号的索引
        end_index = line.find(')')
        if end_index == -1:
            return None  # 如果没有找到右括号，则返回 None
        # 提取右括号到'returns'之间的内容
        # print(f'end_index-{end_index}')
        content = line[end_index + 1:returns_index]
        # print(f'content-{content}')
        return content.strip()  # 去除内容两边的空格
    else:
        # 找到第一个右括号的索引
        end_index = line.find(')')
        if end_index == -1:
            return None  # 如果没有找到右括号，则返回 None
        # 提取右括号到行末尾的内容
        content = line[end_index + 1:]
        return content.strip()  # 去除内容两边的空格
    
def extract_returns_content(line):
    # 统计左括号的出现次数
    left_parentheses_count = line.count('(')
    # 如果左括号出现次数超过2次
    if left_parentheses_count > 2:
        # 找到最后一个左括号的索引
        last_left_parentheses_index = line.rfind('(')
        # 找到最后一个右括号的索引
        last_right_parentheses_index = line.rfind(')')
        # 提取最后一个括号中的内容
        content = line[last_left_parentheses_index + 1:last_right_parentheses_index]
        return content.strip()  # 去除内容两边的空格
    else:
        return None


def try_to_decode(file):
    try:
        # print(f'正在分析{file}')
        # 连接到数据库
        connection = connect_to_database()

        # 如果连接成功，则执行插入操作
        if connection:
            cursor = connection.cursor()

            # 读取文件，假设文件名为 'your_script.py'
            matched_lines = parse_file_and_log(file)
            for line in matched_lines:
                # 解析函数内容
                function_content = extract_function_content(line)
                if function_content is None:
                    function_content = ""
                # 解析参数内容
                para_content = extract_para_content(line)
                if para_content is None:
                    para_content = ""
                # 解析可见性内容
                visible_content = extract_visable_content(line)
                if visible_content is None:
                    visible_content = ""
                # 解析返回内容
                returns_content = extract_returns_content(line)
                if returns_content is None:
                    returns_content = ""

                # 检查条目是否存在
                select_query = "SELECT * FROM contract_functions WHERE function_name = %s AND parameter = %s AND visible = %s AND returns = %s"
                cursor.execute(select_query, (function_content, para_content, visible_content, returns_content))
                existing_entry = cursor.fetchone()
                if existing_entry:
                    # 如果条目存在，将 times 字段加 1
                    update_query = "UPDATE contract_functions SET times = times + 1 WHERE function_name = %s AND parameter = %s AND visible = %s AND returns = %s"
                    cursor.execute(update_query, (function_content, para_content, visible_content, returns_content))
                else:
                    # 如果条目不存在，插入新的条目
                    insert_query = "INSERT INTO contract_functions (function_name, parameter, visible, returns, times) VALUES (%s, %s, %s, %s, %s)"
                    values = (function_content, para_content, visible_content, returns_content, 1)  # 这里假设 times 默认为 1
                    cursor.execute(insert_query, values)

                connection.commit()

            # 关闭数据库连接
            cursor.close()
            connection.close()
    except Exception as e:
        # print(f'Error occured {e}')
        pass
