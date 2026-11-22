from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output" / "summary"

def main():
    sales = pd.read_csv(INPUT_DIR / "sales.csv", dtype={"商品番号":str}, encoding="utf-8-sig", parse_dates=["日付"])
    products = pd.read_excel(INPUT_DIR / "products.xlsx", sheet_name="商品マスタ", dtype={"商品番号":str}, engine="openpyxl")
    print(sales.head())
    sales.info()
    print(sales.isna().sum())
    print(f"完全に同じ行の重複：{sales.duplicated().sum()}件")

    sales["数量"] = pd.to_numeric(sales["数量"], errors="coerce")
    sales["販売単価"] = pd.to_numeric(sales["販売単価"], errors="coerce")
    missing = sales[["日付", "商品番号", "数量", "販売単価", "セール"]].isna().any(axis=1)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sales.loc[missing].to_csv(OUTPUT_DIR / "excluded_rows.csv", index=False, encoding="utf-8-sig")
    print(f"欠損で除外：{missing.sum()}行")
    sales = sales.loc[~missing].drop_duplicates().copy()
    if sales.duplicated(["日付","商品番号"]).any():
        raise ValueError("同じ日付・商品番号で異なる行があります。入力を確認してください。")
    if (sales[["数量", "販売単価"]] < 0).any().any():  
        raise ValueError("負の数量または単価があります。今回は返品データを扱いません。")
    
    sales = sales.merge(products, on="商品番号", how="left", validate="many_to_one")
    if sales[["商品名", "原価"]].isna().any().any():  
        raise ValueError("商品マスタに商品名・原価がないデータがあります。")  
    sales["売上"] = sales["数量"]*sales["販売単価"]
    sales["粗利益"] = sales["数量"]*(sales["販売単価"]-sales["原価"])
    sales["月"]= sales["日付"].dt.strftime("%Y-%m")
    sales["曜日番号"] = sales["日付"].dt.dayofweek
    selected = sales.loc[(sales["商品番号"]=="001")&(sales["月"]=="2025-01"), ["日付", "商品名", "数量", "売上"]]
    print(selected.head())

    product_summary = sales.groupby(["商品番号", "商品名"], as_index=False).agg(販売数=("数量","sum"), 売上=("売上","sum"), 粗利益=("粗利益","sum"))
    product_summary["粗利益率"] = product_summary["粗利益"].div(product_summary["売上"].replace(0, float("nan")))
    product_summary = product_summary.sort_values("粗利益", ascending=False)
    monthly_summary = sales.groupby("月", as_index=False)[["売上", "粗利益"]].sum()
    weekday_summary = sales.groupby("曜日番号", as_index=False).agg(平均販売数=("数量", "mean")) 
    sales = sales.sort_values(["日付", "商品番号"])
    sales.to_csv(OUTPUT_DIR /"sales_clean.csv", index=False, encoding="utf-8-sig")
    product_summary.to_csv(OUTPUT_DIR / "product_summary.csv", index=False, encoding="utf-8-sig")  
    monthly_summary.to_csv(OUTPUT_DIR / "monthly_summary.csv", index=False, encoding="utf-8-sig")  
    weekday_summary.to_csv(OUTPUT_DIR / "weekday_summary.csv", index=False, encoding="utf-8-sig") 
    print(product_summary.to_string(index=False))  
    print(f"保存先：{OUTPUT_DIR}") 


if __name__ == "__main__":
    main()
