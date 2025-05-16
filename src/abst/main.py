import json
import os
import subprocess

from code_abstract import CodeAbstract
from parser import Parser


def execute_abstraction(js_file_path):
    """抽象化実行関数

    Args:
        js_file_path (str): 対象ファイルのパス

    Returns:
        str: 抽象化後のファイル
    """
    # プロセスIDを使用してをユニークな一時ファイルを生成
    thread_id = os.getpid()
    parser = Parser(thread_id)
    target_js = f"./parser_{thread_id}.js"

    # JavaScriptコードを読み込み
    with open(js_file_path, "r") as f:
        code = f.read()

    # 改行コードの標準化・コメント除去・フォーマッタの適応
    code = code.replace("\r\n", "\n")
    # code = parser.remove_comment(code)
    code = parser.prettier(code)

    # 整形後コードが空の場合は終了
    if len(code) == 0:
        return None

    # AST生成
    ast_str = subprocess.run(
        ["node", "jsparser.js", target_js],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ).stdout

    # ASTが存在しない場合は終了
    if len(ast_str) == 0:
        return None

    # json形式で読み込み
    ast = json.loads(ast_str)

    # 弱抽象化の実施
    abstcode = CodeAbstract(code, ast)
    abstcode.weak_abstract_code()

    # 一時ファイルの削除
    os.remove(f"parser_{thread_id}.js")

    # 抽象化結果を返す
    return abstcode.abstract_code


if __name__ == "__main__":
    result = execute_abstraction("test.js")
    with open("test_abs.js", "w") as f:
        f.write(result)
