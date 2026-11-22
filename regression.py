from pathlib import Path
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

BASE_DIR = Path(__file__).resolve().parent  
INPUT_PATH = BASE_DIR / "output" / "summary" / "sales_clean.csv"  
OUTPUT_DIR = BASE_DIR / "output" / "regression" 

def main():
    sales = pd.read_csv(INPUT_PATH, dtype={"商品番号":str}, parse_dates=["日付"], encoding="utf-8-sig")
    daily = sales.loc[sales["商品番号"]=="001"].sort_values("日付").copy()
    if len(daily)<30:
        raise ValueError("商品001の日別データを30日分以上用意してください。")

    split_index = int(len(daily) * 0.8)
    train = daily.iloc[:split_index].copy()
    test = daily.iloc[split_index:].copy()
    X_train = train[["販売単価"]]
    y_train = train["数量"]
    X_test = test[["販売単価"]]
    y_test = test["数量"]

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test).clip(min=0)
    baseline = [y_train.mean()] * len(test)
    model_mae = mean_absolute_error(y_test, predictions)
    baseline_mae = mean_absolute_error(y_test, baseline)

    print(f"学習期間：{train['日付'].min():%Y-%m-%d}～{train['日付'].max():%Y-%m-%d}")
    print(f"評価期間：{test['日付'].min():%Y-%m-%d}～{test['日付'].max():%Y-%m-%d}")

    print(f"予測式：販売数 = {model.coef_[0]:.4f} × 販売単価 + {model.intercept_:.2f}") 
    print(f"平均値の予測 MAE：{baseline_mae:.2f}個／線形回帰 MAE：{model_mae:.2f}個") 

    result = test[["日付", "商品名", "販売単価", "数量"]].copy()
    result["予測販売数"] = predictions 
    result["平均値予測"] = baseline 
    result["絶対誤差"] = (result["数量"] - result["予測販売数"]).abs()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_DIR / "predictions.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame({"方法": ["平均値", "単回帰"], "MAE": [baseline_mae, model_mae]}).to_csv(OUTPUT_DIR / "metrics.csv", index=False, encoding="utf-8-sig")

if __name__ =="__main__":
    main()
