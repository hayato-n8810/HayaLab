import json
import os
import subprocess
import time

JSON_FILE = "./top100_javascript_repositories.json"
CLONE_DIR = "./clone_project"

# リポジトリのクローン
# JSONファイルを読み込む
# 2024-12-13時点
with open(JSON_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

for item in data:
    print("Cloning repository : " + item)
    # 各行のURLの末尾を取得しディレクトリ名を構成
    rep_split = item.split("/")
    clone_dir = rep_split[-2] + "_" + rep_split[-1]

    # クローン先のパスを作成
    clone_path = os.path.join(CLONE_DIR, clone_dir)

    try:
        subprocess.run(["git", "clone", item, clone_path], check=True)
    except subprocess.SubprocessError as e:
        print(f"Error while cloning repository: {e}")

    print(clone_dir + " clone finish")
    # 一応スリープ
    time.sleep(5)
