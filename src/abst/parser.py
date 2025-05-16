import subprocess


class Parser:
    """javascript実行に関するクラス"""

    def __init__(self, i):
        self.filename = f"./parser_{i}.js"

    def save_file(self, code):
        """入力プログラムの保存

        Args:
            code (str): プログラム文字列
        """
        with open(self.filename, "w") as f:
            f.write(code)

    def read_file(self):
        """入力ファイルの中身を取得

        Returns:
            str: ファイルの中身
        """
        with open(self.filename) as f:
            return f.read()

    def node(self, command, code):
        """jsファイル実行

        Args:
            command (str): 実行コマンド
            code (str): 実行ファイル名

        Returns:
            ???: コマンド実行結果の標準出力
        """
        self.save_file(code)
        return subprocess.run(
            command + [f"./{self.filename}"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        ).stdout

    # def remove_comment(self, code):
    #   return self.node(["node", "comment_remover.js"], code)

    def prettier(self, code):
        """フォーマッターの適応

        Args:
            code (str): 対象プログラム

        Returns:
            str: フォーマッター適応後プログラム
        """
        self.node(["npx", "prettier", "--write"], code)
        return self.read_file()
