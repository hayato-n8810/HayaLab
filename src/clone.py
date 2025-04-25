import os
import subprocess
import time


def clone_repository(repo_url: str) -> None:
    """リポジトリクローン関数

    Args:
        repo_url (str): リポジトリURL
    """
    rep_split = repo_url.rstrip("/").split("/")
    clone_dir = f"{rep_split[-2]}_{rep_split[-1]}"
    target_path = f"./data/TestDynamicAnalysis/{clone_dir}"

    if not os.path.exists("./data/TestDynamicAnalysis"):
        os.makedirs("./data/TestDynamicAnalysis")

    if os.path.exists(target_path):
        print(f"{clone_dir} already cloned.")
    else:
        try:
            subprocess.run(["git", "clone", repo_url, target_path], check=True)
            print(f"Cloned {repo_url} into {target_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error cloning {repo_url}: {e}")
    time.sleep(1)  # アクセス制限回避


if __name__ == "__main__":
    # データセット取得：React
    repo = "https://github.com/facebook/react"

    print(repo)
    clone_repository(repo)
