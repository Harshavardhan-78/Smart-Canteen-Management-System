def encode_inputs(weather, exams, region):
    weather_map = {"Sunny": 0, "Rainy": 1, "Cloudy": 2}
    exams_map = {"None": 0, "Midterms": 1, "Finals": 2}
    region_map = {"Urban": 0, "Rural": 1}

    return [
        weather_map[weather],
        exams_map[exams],
        region_map[region]
    ]

def generate_historical_insights(df):
    insights = []

    if df.empty:
        return ["Not enough historical data"]

    avg_qty = df["quantity"].mean()

    weather_trend = df.groupby(["weather", "item"])["quantity"].mean()
    for (w, item), qty in weather_trend.items():
        if qty > avg_qty:
            insights.append(f"📈 {item} sells more during {w} weather")

    exam_trend = df.groupby(["exams", "item"])["quantity"].mean()
    for (e, item), qty in exam_trend.items():
        if e != "None" and qty > avg_qty:
            insights.append(f"📚 During {e}, demand for {item} increases")

    low_items = (
        df.groupby("item")["quantity"]
        .mean()
        .sort_values()
        .head(3)
        .index
    )

    for item in low_items:
        insights.append(f"⚠️ Reduce or replace {item} (low demand historically)")

    return list(set(insights))

def recommend_tomorrow_menu(df, weather, exams):
    if df.empty:
        return ["Insufficient data"]

    filtered = df[
        (df["weather"] == weather) &
        (df["exams"] == exams)
    ]

    if filtered.empty:
        filtered = df

    return (
        filtered.groupby("item")["quantity"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .index
        .tolist()
    )
