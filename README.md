# hayaLab
研究の痕跡

## ディレクトリ構成
```
/
├── data/                  ← データセット（ignore）
├── src/                   ← 研究プログラムセット
├── results/               ← 結果
├── archive/               ← 研究トピックごとのディレクトリアーカイブ
│   └── [topic]/
│       ├── visualize/     ← 可視化用
│       ├── src/           ← 研究プログラム一式
│       └── results/       ← このトピックに関する結果
└── config/                ← 実験設定
```
## 研究トピック
- Omori:大森研究に関するもの
- Zenkoku:全国までのもの

## python 実行方法
- ファイル実行
```
uv run python {ファイル名}
```

- pip install
```
uv add {ライブラリ名}
```
