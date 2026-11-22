from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "output" / "summary"
OUTPUT_DIR = BASE_DIR / "output" / "charts"

def main():
    available_fonts = {font.name for font in font_manager.fontManager.ttflist}
    for font_name in ["Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", "Noto Sans CJK JP", "IPAexGothic"]:
        if font_name in available_fonts:
            plt.rcParams["font.family"] = font_name
            break
    else:
        raise RuntimeError("日本語フォントが見つかりません。Noto Sans CJK JPなどを用意してください。")

    monthly = pd.read_csv(INPUT_DIR / "monthly_summary.csv", encoding="utf-8-sig")
    products = pd.read_csv(INPUT_DIR / "product_summary.csv", dtype={"商品番号": str}, encoding="utf-8-sig")
    weekdays = pd.read_csv(INPUT_DIR / "weekday_summary.csv", encoding="utf-8-sig")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly["月"], monthly["売上"], marker="o", label="売上")
    ax.plot(monthly["月"], monthly["粗利益"], marker="o", label="粗利益")
    ax.set(title="月別の売上と粗利益(仮想データ)", xlabel="月", ylabel="金額（円）")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "monthly.png", dpi=160)
    plt.close(fig)

    ranked = products.sort_values("粗利益", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(ranked["商品名"], ranked["粗利益"])
    ax.set(title="商品別の粗利益", xlabel="商品", ylabel="粗利益(円)")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "product_profit.png", dpi=160)
    plt.close(fig)

    weekdays = weekdays.sort_values("曜日番号")
    weekday_names = weekdays["曜日番号"].map({0:"月", 1:"火",2: "水", 3: "木", 4: "金", 5: "土", 6: "日"})
    fig, ax = plt.subplots(figsize=(8,5))
    ax.bar(weekday_names, weekdays["平均販売数"])
    ax.set(title="曜日別の平均販売数（仮想データ）", xlabel="曜日", ylabel="平均販売数（個／日・商品）") 
    fig.tight_layout() 
    fig.savefig(OUTPUT_DIR / "weekday.png", dpi=160)
    plt.close(fig)

if __name__ =="__main__":
    main()
