import json
import re
from collections import defaultdict

from const import path

# 正規表現パターン
r"""
TARGET_REGEX1 = re.compile(r"\w+\.hasOwnProperty\(")
TARGET_REGEX2 = re.compile(r"Object\.prototype\.hasOwnProperty\.call\(")

TARGET_REGEX1 = re.compile(r".+\.apply\(")
TARGET_REGEX2 = re.compile(r".+\.call\(")
"""

TARGET_REGEX1 = re.compile(r"\w+\.push")
TARGET_REGEX2 = re.compile(r"\w+\.concat")


def match_target(diff_text):
    """正規表現のパターンが含まれるかどうか判定"""
    return bool(TARGET_REGEX1.search(diff_text) or TARGET_REGEX2.search(diff_text))


def filter_and_group_nested(input_path, output_path):
    """ファイルごとに正規表現のパターンを含む変更履歴を収集しまとめる"""
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    grouped_results = defaultdict(list)

    for entry in data:
        file_path = entry["file"]
        commit = entry["commit"]
        message = entry["message"]
        diffs = entry.get("diff", [])

        matched_diffs = [d for d in diffs if match_target(d.get("added", "")) or match_target(d.get("removed", ""))]

        if matched_diffs:
            grouped_results[file_path].append({"commit": commit, "message": message, "diff": matched_diffs})

    # 整形して出力データを作成
    output_data = [{"file": file_path, "commits": commits} for file_path, commits in grouped_results.items()]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"✅ 出力完了: {output_path} （{len(output_data)} ファイル）")


if __name__ == "__main__":
    """メイン"""
    filter_and_group_nested(
        f"{path.RESULTS}/trace/all_commit_diffs_propaty.json", f"{path.RESULTS}/trace/filtered_by_addArray.json"
    )
