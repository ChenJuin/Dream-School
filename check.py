def check_parentheses(input_str):
    stack = []  # 用于跟踪左括号的栈
    output = [' ' for _ in range(len(input_str))]  # 初始化输出字符串，用于标记

    for i, char in enumerate(input_str):
        if char == '(':
            stack.append(i)  # 将左括号的位置推入栈中
        elif char == ')':
            if stack:
                stack.pop()  # 如果栈不为空，弹出一个左括号
            else:
                output[i] = '?'  # 如果栈为空，标记一个问号

    # 遍历完字符串后，栈中仍有左括号，标记一个x
    for index in stack:
        output[index] = 'x'

    return ''.join(output)

# 样例输入
input_cases = [
    "bge)))))))))",
    "((IIII)))))",
    "()()()()(uuu",
    "))))UUUU((()"
]

# 输出结果
for case in input_cases:
    print(case)
    print(check_parentheses(case))
