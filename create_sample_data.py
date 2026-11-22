# 4段階で共通して使う仮想データを作る準備用スクリプト。実企業の実績ではない。
# 1行は「1日・1商品」の合計。1年分・3商品を用意し、在庫制約と休業日はない想定。

from pathlib import Path  # 入力ファイルの保存先を指定する。
from random import Random  # 毎回同じ結果になる乱数を使う。
import math  # 季節の変動を作るsinとpiを使う。
import pandas as pd  # CSVとExcelのデータを作る。

BASE_DIR = Path(__file__).resolve().parent  # このファイルのある04 sales_analysisフォルダを取得する。
INPUT_DIR = BASE_DIR / "input"  # 共通入力フォルダを指定する。


def main():  # データ作成をまとめる。
    INPUT_DIR.mkdir(parents=True, exist_ok=True)  # 保存先を作る。
    if (INPUT_DIR / "sales.csv").exists() or (INPUT_DIR / "products.xlsx").exists():  # 自分で変更したデータを上書きしないよう確認する。
        raise FileExistsError("入力ファイルがすでにあります。再作成する場合は先に別の場所へ移してください。")  # 既存データがあれば停止する。
    rng = Random(42)  # 乱数の出発点を固定して、同じ練習データを再現できるようにする。
    products = pd.DataFrame({"商品番号": ["001", "002", "003"], "商品名": ["コーヒー", "サンドイッチ", "焼き菓子"], "カテゴリ": ["飲料", "食品", "食品"], "原価": [120, 230, 90]})  # 商品ごとの固定情報を表にする。原価は1個あたりの円額。
    rows = []  # 売上の日別データをためる空のリストを作る。
    for date in pd.date_range("2025-01-01", "2025-12-31"):  # 2025年の全日を順番に処理する。
        for product_id, normal_price, base_quantity in [("001", 350, 55), ("002", 600, 35), ("003", 280, 45)]:  # 商品番号・通常価格・基準販売数を1商品ずつ取り出す。
            promotion = int(rng.random() < 0.2)  # およそ20％の日をセール予定ありの1、それ以外を0にする。
            price = normal_price - 30 * promotion  # セールの日は価格を30円下げる。
            weekend = 12 if date.dayofweek >= 5 else 0  # 学習用に、土日は販売数が増える傾向を設定する。
            season = 5 * math.sin(2 * math.pi * date.dayofyear / 365)  # 季節による緩やかな変動を加える。
            quantity = max(0, round(base_quantity + weekend + 9 * promotion + season + rng.gauss(0, 5)))  # 傾向とランダムな変動を足し、0以上の整数にする。
            rows.append({"日付": date.strftime("%Y-%m-%d"), "商品番号": product_id, "数量": quantity, "販売単価": price, "セール": promotion})  # 1日・1商品分を辞書で記録する。
    rows.append(rows[12].copy())  # 完全重複の確認を練習できるよう、同じ行を1つ加える。
    missing_row = rows[20].copy()  # 欠損確認の練習用に、既存行を複製する。
    missing_row["数量"] = None  # 数量を空欄にした余分な行を作る。元の正常な行は残しておく。
    rows.append(missing_row)  # 欠損行を追加する。
    pd.DataFrame(rows).to_csv(INPUT_DIR / "sales.csv", index=False, encoding="utf-8-sig")  # Excelでも開きやすいUTF-8のCSVとして保存する。
    products.to_excel(INPUT_DIR / "products.xlsx", sheet_name="商品マスタ", index=False, engine="openpyxl")  # 商品マスタをExcel形式で保存する。
    print(f"仮想データを作成しました：{INPUT_DIR}")  # 保存先を表示する。
    print("売上CSV：1097行（正常1095行＋完全重複1行＋数量欠損1行）")  # ①で確認する件数を表示する。


if __name__ == "__main__":  # このファイルを直接実行したときだけ作成する。
    main()  # 練習データの作成を実行する。
