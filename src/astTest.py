import re
import subprocess


def generate_abstract_map(ast_lines):
    """変数・関数名を抽出する"""
    var_map = {}
    func_map = {}
    var_counter = 1
    func_counter = 1

    parent_stack = []

    for line in ast_lines:
        indent_level = len(line) - len(line.lstrip(" "))
        line_stripped = line.strip()

        # スタック調整
        while len(parent_stack) > indent_level // 4:
            parent_stack.pop()

        # ノード名取得
        m_node = re.match(r"^([a-z_]+)(?:\s|\[)", line_stripped)
        if m_node:
            parent_stack.append(m_node.group(1))

        parent_type = parent_stack[-1] if parent_stack else None

        # identifier の抽出と分類
        if "identifier:" in line_stripped:
            name = line_stripped.split("identifier:")[1].strip().split()[0]

            if parent_type == "variable_declarator":
                if name not in var_map:
                    var_map[name] = f"VAR_{var_counter}"
                    var_counter += 1
            elif parent_type == "formal_parameters":
                if name not in var_map:
                    var_map[name] = f"VAR_{var_counter}"
                    var_counter += 1
            elif parent_type == "function_declaration":
                if name not in func_map:
                    func_map[name] = f"FUNCTION_{func_counter}"
                    func_counter += 1

    return var_map, func_map


def apply_abstract_map(js_code, var_map, func_map):
    """識別子の長さが長い順に置換（衝突回避）"""
    for original, abstracted in sorted(var_map.items(), key=lambda x: -len(x[0])):
        js_code = re.sub(rf"\b{re.escape(original)}\b", abstracted, js_code)

    for original, abstracted in sorted(func_map.items(), key=lambda x: -len(x[0])):
        js_code = re.sub(rf"\b{re.escape(original)}\b", abstracted, js_code)

    return js_code


# JavaScriptコード（入力）
with open("test.js", "r") as f:
    js = f.read()

js_code = js.strip().split("\n")

# gumtree parse 出力（テキストAST形式、手動サンプル）
result = subprocess.run(["gumtree", "parse", "test.js"], capture_output=True, text=True)
ast_text = result.stdout.splitlines()
# 抽象化マップ生成
var_map, func_map = generate_abstract_map(ast_text)

# 抽象化実行
abstracted_code = apply_abstract_map(js_code, var_map, func_map)

# 出力
print("✅ 抽象化されたコード:")
print(abstracted_code)
