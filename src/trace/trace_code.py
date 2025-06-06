import json
import os
import re

from const import path

# グローバル変数でエラーを収集
error_log = []


def find_pattern_files(target_directory, patterns):
    """指定した正規表現のパターンが出現するファイルのパスを返す

    Args:
        target_directory (str): 走査対象フォルダ（プロジェクト）
        patterns (dict): 正規表現パターン

    Returns:
        dict: 見つけたファイルパス
    """
    slow_files = []  # slowが見つかったファイルパス
    fast_files = []  # fastが見つかったファイルパス

    clone_path = os.path.join("./", target_directory)
    print(f"Processing directory: {clone_path}")

    for root, dirs, files in os.walk(clone_path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for file in files:
            if file.endswith(".js"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()

                        # .apply()パターンをチェック
                        if patterns["slow"].search(content):
                            slow_files.append(file_path)

                        # .call()パターンをチェック
                        if patterns["fast"].search(content):
                            fast_files.append(file_path)

                except Exception as e:
                    error_message = f"Error reading file {file_path}: {e}"
                    print(error_message)
                    error_log.append(error_message)

    print(f"Finished processing directory: {target_directory}")
    return {
        "repository": target_directory,
        "slow_apply_files": slow_files,
        "fast_call_files": fast_files,
        "slow_count": len(slow_files),
        "fast_count": len(fast_files),
    }


def process_pattern_files(target_directory, patterns, output_file):
    """実行関数とファイル出力

    Args:
        target_directory (str): 走査対象フォルダ（プロジェクト）
        patterns (dict): 検出対象正規表現パターン
        output_file (str): 出力ファイル
    """
    try:
        # 単一のディレクトリを処理
        result = find_pattern_files(target_directory, patterns)

        # 結果をファイルに書き込む処理のエラー処理
        try:
            with open(output_file, "w", encoding="utf-8") as json_file:
                json.dump(result, json_file, ensure_ascii=False, indent=4)
            print(f"結果が {output_file} に出力されました。")
        except Exception as e:
            error_message = f"Error writing to file {output_file}: {e}"
            print(error_message)
            error_log.append(error_message)

    except Exception as e:
        error_message = f"Unexpected error in process_pattern_files: {e}"
        print(error_message)
        error_log.append(error_message)
    finally:
        print("Process finished")


if __name__ == "__main__":
    """メイン"""
    try:
        DATA_DIR = f"{path.DATA}/repository"

        # 対象フォルダを指定（例: 最初のプロジェクト）
        projects = os.listdir(DATA_DIR)
        if not projects:
            print("No projects found in clone_project directory")
            exit(1)

        target_project = f"{path.DATA}/repository/{projects[0]}"  # プロジェクトを選択
        print(f"Target project: {target_project}")

        # Pattern
        patterns1 = {"slow": re.compile(r".+\.apply\("), "fast": re.compile(r".+\.call\(")}

        patterns2 = {
            "slow": re.compile(r"Object\.prototype\.hasOwnProperty\.call\("),
            "fast": re.compile(r"\w+\.hasOwnProperty\("),
        }

        patterns3 = {
            "slow": re.compile(r"\w+\.push"),
            "fast": re.compile(r"\w+\.concat"),
        }

        process_pattern_files(target_project, patterns3, f"{path.RESULTS}/trace/addArray_files.json")

    except Exception as e:
        error_message = f"Unexpected error in main: {e}"
        print(error_message)
        error_log.append(error_message)

    finally:
        # エラー内容をファイルに書き出す
        if error_log:
            error_file = "errors.log"
            with open(error_file, "w", encoding="utf-8") as f:
                f.write("\n".join(error_log))
            print(f"Errors have been logged to {error_file}")
