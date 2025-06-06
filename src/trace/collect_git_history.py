import json
import os
from pathlib import Path

from git import Repo

from const import path


def read_target_files(json_path):
    """パスの書かれたjsonファイル読み込み"""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("slow_apply_files", []) + data.get("fast_call_files", [])


def find_git_root(path):
    """指定ファイルの所属するgitリポジトリのルートを探す"""
    current = Path(path).resolve()
    for parent in current.parents:
        if (parent / ".git").exists():
            return str(parent)
    raise FileNotFoundError(f"{path} に .git リポジトリが見つかりません")


def get_file_commit_history(repo, file_path):
    """コミット履歴取得"""
    commits = list(repo.iter_commits(paths=file_path))
    commits.reverse()  # oldest first
    return commits


def get_commit_diff(repo, file_path, commits):
    """ファイル変更差分取得"""
    results = []
    for i, commit in enumerate(commits):
        commit_id = commit.hexsha
        message = commit.message.strip()
        diff_pairs = []

        if i == 0:
            try:
                content = commit.tree[file_path].data_stream.read().decode("utf-8").splitlines()
                diff_pairs = [{"removed": "", "added": line} for line in content]
            except Exception:
                pass
        else:
            prev_commit = commits[i - 1]
            diff_index = prev_commit.diff(commit, paths=file_path, create_patch=True)
            diff_text = ""
            for diff_item in diff_index:
                if diff_item.a_path == file_path or diff_item.b_path == file_path:
                    try:
                        diff_text = diff_item.diff.decode("utf-8")
                    except Exception:
                        diff_text = ""
                    break

            for line in diff_text.splitlines():
                if line.startswith("-") and not line.startswith("---"):
                    removed = line[1:].strip()
                    diff_pairs.append({"removed": removed, "added": ""})
                elif line.startswith("+") and not line.startswith("+++"):
                    added = line[1:].strip()
                    if diff_pairs and diff_pairs[-1]["added"] == "":
                        last = diff_pairs.pop()
                        diff_pairs.append({"removed": last["removed"], "added": added})
                    else:
                        diff_pairs.append({"removed": "", "added": added})

        results.append({"file": file_path, "commit": commit_id, "message": message, "diff": diff_pairs})
    return results


def main():
    """メイン"""
    # trace_codeで作成したjsonファイルからリポジトリ名とファイル数の項目消したやつ
    # json_path = f"{path.RESULTS}/trace/propaty_files.json"
    json_path = f"{path.RESULTS}/trace/addArray_files.json"
    # output_path = f"{path.RESULTS}/trace/all_commit_diffs_propaty.json"
    output_path = f"{path.RESULTS}/trace/all_commit_diffs_addArray.json"

    target_files = read_target_files(json_path)
    all_results = []

    for abs_file_path in target_files:
        if not os.path.exists(abs_file_path):
            print(f"[WARN] ファイルが見つかりません: {abs_file_path}")
            continue

        try:
            git_root = find_git_root(abs_file_path)
            rel_path = os.path.relpath(abs_file_path, git_root)
            repo = Repo(git_root)

            commits = get_file_commit_history(repo, rel_path)
            diffs = get_commit_diff(repo, rel_path, commits)
            all_results.extend(diffs)

        except Exception as e:
            print(f"[ERROR] {abs_file_path} の処理中にエラー発生: {e}")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"✅ 全コミット差分を {output_path} に出力しました。")


if __name__ == "__main__":
    main()
