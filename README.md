# Sales Analysis

架空の1年分の売上データで、欠損・重複の処理、売上と粗利益の集計、グラフ作成、販売数量の回帰分析を行います。

## 実行方法

リポジトリのルートで Python 3.10 以降を使います。

```bash
python -m pip install -r requirements.txt
python create_sample_data.py
python summarize.py
python visualize.py
python regression.py
```

集計表、グラフ、評価指標は `output/` 以下に保存します。グラフにはNoto Sans CJK JPなど、Matplotlibが認識する日本語フォントが必要です。回帰では時系列順に学習期間と評価期間を分け、学習期間の平均を使う予測とMAEを比較します。
