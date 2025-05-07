import json


def extract_variable_names(ast_json: dict) -> dict:
    """抽象構文木から変数名を抽出する関数

    Args:
        ast_json (dict): json形式の抽象構文木

    Returns:
        dict: 変数名の置換辞書
    """
    variable_names = {}
    function_names = {}
    var_count = 1
    function_count = 1

    # rootノードのchildrenを取得
    root_children = ast_json.get("root", {}).get("children", [])

    # 各式文を処理
    for node in root_children:
        # 変数宣言ノードを探す
        if node.get("type") == "expression_statement" or node.get("type") == "lexical_declaration":
            for child in node.get("children", []):
                # 代入・変数宣言ノードを探す
                if child.get("type") == "assignment_expression" or child.get("type") == "variable_declarator":
                    # identifierノードを探す（変数名）
                    for elem in child.get("children", []):
                        if elem.get("type") == "identifier":
                            if elem.get("label") not in variable_names:
                                variable_names[elem.get("label")] = "VAR_" + str(var_count)
                                var_count += 1
                # 関数呼び出しを探す
                elif child.get("type") == "call_expression":
                    # 引数ノードを探す
                    for elem in child.get("children", []):
                        if elem.get("type") == "arguments":
                            # identifierノードを探す（変数名）
                            for elemchild in elem.get("children", []):
                                if elemchild.get("type") == "identifier":
                                    if elemchild.get("label") not in variable_names:
                                        variable_names[elemchild.get("label")] = "VAR_" + str(var_count)
                                        var_count += 1
                # 関数宣言を探す
                elif child.get("type") == "function_declaration":
                    for elem in child.get("children", []):
                        # 関数名を取得
                        if elem.get("type") == "identifier":
                            if elem.get("label") not in function_names:
                                function_names[elem.get("label")] = "FUNCTION_" + str(function_count)
                                function_count += 1
                        # 仮引数名を取得
                        if elem.get("type") == "fomal_parameters":
                            if elem.get("label") not in function_names:
                                for elemchild in elem.get("children", []):
                                    if elemchild.get("type") == "identifier":
                                        if elemchild.get("label") not in variable_names:
                                            variable_names[elemchild.get("label")] = "VAR_" + str(var_count)
                                            var_count += 1

    return variable_names


# ファイルからJSONを読み込む
with open("test_abs2.json", "r") as f:
    ast_json = json.load(f)

# 変数名を抽出して表示
variable_names = extract_variable_names(ast_json)
print(variable_names)
