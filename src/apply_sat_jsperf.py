import json
import os
import subprocess
import tempfile

from const import path


def excute_sat(code_file, output_text_file):
    """SAT実行関数

    Args:
        code_file (json): {slow:~,fast:~}の形式のプログラム
        output_text_file (str): 出力テキストファイルパス
    """
    report_data = []
    error_occurred_globally = False

    for i, code in enumerate(code_file):
        entry_prefix_slow = f"--- Slow Program Entry {i + 1} ---\n"
        slow_code = code["slow"]
        current_report_data = [entry_prefix_slow, "Original Code:\n", slow_code, "\n\nComplexity Report:\n"]

        try:
            # 一時JavaScriptファイルを作成
            with tempfile.NamedTemporaryFile(mode="w+", suffix=".js", delete=False, encoding="utf-8") as tmp_js_file:
                tmp_js_file.write(slow_code)
                tmp_js_file_path = tmp_js_file.name

            # complexity-report を実行し標準出力にレポートをキャプチャ
            cmd = ["npx", "complexity-report", tmp_js_file_path]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",  # エンコーディングエラー時に置換文字を使用
            )
            stdout, stderr = process.communicate(timeout=60)  # タイムアウトを60秒に設定

            if process.returncode == 0:
                current_report_data.append(stdout)
            else:
                current_report_data.append("❌ Error running complexity-report:\n")
                if stdout:  # エラー時でも標準出力がある場合
                    current_report_data.append("Stdout:\n")
                    current_report_data.append(stdout)
                if stderr:
                    current_report_data.append("Stderr:\n")
                    current_report_data.append(stderr)

        except subprocess.TimeoutExpired:
            timeout_message = f"エラー: complexity-report実行タイムアウト（ファイル: {tmp_js_file_path}）。\n"
            print(timeout_message)
            current_report_data.append(timeout_message)
        except Exception as e:
            error_message = f"予期せぬエラーが発生しました（ファイル: {tmp_js_file_path}）: {e}\n"
            print(error_message)
            current_report_data.append(error_message)
        finally:
            # 一時ファイルを削除
            if tmp_js_file_path and os.path.exists(tmp_js_file_path):
                os.remove(tmp_js_file_path)

        report_data.append("".join(current_report_data))
        report_data.append("\n" + "=" * 60 + "\n\n")

    try:
        with open(output_text_file, "w", encoding="utf-8") as outfile:
            for report_entry in report_data:
                outfile.write(report_entry)
        if not error_occurred_globally:
            print(f"解析結果が '{output_text_file}' に出力されました。")
        else:
            print(f"⚠️  '{output_text_file}' に部分的な結果またはエラー情報が出力されました")

    except IOError as e:
        print(f"エラー: 出力ファイル '{output_text_file}' に書き込めませんでした: {e}")


if __name__ == "__main__":
    jsperf_data_path = f"{path.DATA}/jsperf/codes.json"
    output_text_file = f"{path.RESULTS}/sat/slow_code_sat.txt"

    with open(jsperf_data_path, "r") as f:
        jsperf_data = f.read()

    # json形式で読み込み
    jsperf_code = json.loads(jsperf_data)

    excute_sat(jsperf_code, output_text_file)
