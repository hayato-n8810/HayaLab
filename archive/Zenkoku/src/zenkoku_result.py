# 全国の結果を出すプログラム
# clone_projectから5パターンの正規表現の数を並列計算で取得

import json
import os
from multiprocessing import Pool, cpu_count

# グローバル変数でエラーを収集
error_log = []


def pattern_num(args):
    directory, patterns = args
    fast_count = 0
    slow_count = 0

    clone_path = os.path.join("./", directory)
    print(f"Processing directory: {clone_path}")

    for root, dirs, files in os.walk(clone_path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for file in files:
            if file.endswith(".js"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                        fast_count += len(patterns["fast"].findall(content))
                        slow_count += len(patterns["slow"].findall(content))
                except Exception as e:
                    error_message = f"Error reading file {file_path}: {e}"
                    print(error_message)
                    error_log.append(error_message)

    print(f"Finished processing directory: {directory}")
    return {"repository": directory, "fast": fast_count, "slow": slow_count}


def process_patterns(projects, patterns, output_file):
    try:
        args = [(dir, patterns) for dir in projects]

        # 並列処理のエラー処理
        try:
            with Pool(cpu_count() - 1) as pool:
                results = pool.map(pattern_num, args)
        except Exception as e:
            error_message = f"Error during parallel processing: {e}"
            print(error_message)
            error_log.append(error_message)
            results = []

        # 結果をファイルに書き込む処理のエラー処理
        try:
            with open(output_file, "w", encoding="utf-8") as json_file:
                json.dump(results, json_file, ensure_ascii=False, indent=4)
            print(f"結果が {output_file} に出力されました。")
        except Exception as e:
            error_message = f"Error writing to file {output_file}: {e}"
            print(error_message)
            error_log.append(error_message)

    except Exception as e:
        error_message = f"Unexpected error in process_patterns: {e}"
        print(error_message)
        error_log.append(error_message)
    finally:
        print("Process finished")


if __name__ == "__main__":
    try:
        CLONE_DIR = "./clone_project"
        project = os.listdir(CLONE_DIR)

        os.chdir("clone_project")

        """
        # Pattern 1
        patterns1 = {
            'slow': re.compile(r'.*new String\\('),
            'fast': re.compile(r".*=\\s*(\\".*?\\"|'.*?')")
        }
        process_patterns(project, patterns1, '../string.json')

        # Pattern 2
        patterns2 = {
            'slow': re.compile(r".+\\.fill\\(0\\)", re.DOTALL),
            'fast': re.compile(r".*new\\s*(?:Int(?:8|16|32|64)|Uint(?:8|16|32|64)|Float(?:32|64)|Big(?:Int|Uint)64)Array\\s*\\(.*\\)")
        }
        process_patterns(project, patterns2, '../array0.json')
        
        # Pattern 3
        patterns3 = {
            'slow': re.compile(r".+\\.apply\\("),
            'fast': re.compile(r".+\\.call\\(")
        }
        process_patterns(project, patterns3, '../func.json')

        # Pattern 4
        patterns4 = {
            'slow_date': re.compile(r"new Date\\(\\)\\.getTime\\(\\)"), # new Date().getTime()に一致
            'fast_date': re.compile(r"Date\\.now\\(\\)"), # Date.now()に一致
        }
        process_patterns(project, patterns4, '../date.json')

        # Pattern 5
        patterns5 = {
            'slow_propaty':re.compile(r"Object\\.prototype\\.hasOwnProperty\\.call\\((.*)\\)"), # Object.prototype.hasOwnProperty.call(***)に一致,
            'fast_propaty':re.compile(r"\\.hasOwnProperty\\((.*)\\)"), #　.hasOwnProperty(***)に一致,
        }
        process_patterns(project, patterns5, '../propaty.json')
        """

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
