import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="Smart Sleep Robot",
    page_icon="🤖",
    layout="centered"
)

FILE_NAME = "sleep_log.csv"

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=[
        "日付",
        "歩数",
        "運動時間",
        "日光時間",
        "カフェイン",
        "スマホ時間",
        "ストレス",
        "ストレス原因",
        "学習時間",
        "睡眠スコア",
        "予測",
        "実際"
    ])
    df.to_csv(FILE_NAME, index=False)

st.title("😴 Smart Sleep Robot 🤖")
st.caption("日中の行動から今夜の睡眠を予測します")

st.markdown("---")

st.subheader("📝 今日の行動を入力")

steps = st.number_input(
    "🚶 今日の歩数",
    min_value=0,
    max_value=100000,
    value=8000,
    step=100
)

exercise = st.number_input(
    "🏃 運動時間（分）",
    min_value=0,
    max_value=300,
    value=30
)

sun_time = st.number_input(
    "☀ 日光を浴びた時間（分）",
    min_value=0,
    max_value=180,
    value=15
)

coffee = st.selectbox(
    "☕ カフェイン",
    [
        "飲んでない",
        "15時まで",
        "18時以降"
    ]
)

phone = st.number_input(
    "📱 夜のスマホ使用時間（分）",
    min_value=0,
    max_value=600,
    value=30
)

stress = st.slider(
    "😰 ストレス",
    1,
    5,
    3
)

stress_reason = st.text_area(
    "📝 ストレスの原因",
    placeholder="例：テスト・レポート・アルバイト・人間関係"
)

study = st.number_input(
    "📚 今日の学習時間（分）",
    min_value=0,
    max_value=1000,
    value=120
)

st.markdown("---")

if st.button("🤖 睡眠を分析する", use_container_width=True):

    score = 50
    advice = []

    # 歩数
    if steps >= 8000:
        score += 15
    elif steps >= 5000:
        score += 5
        advice.append("🚶 あと20〜30分散歩すると約3000歩増え、睡眠の質向上が期待できます。")
    else:
        score -= 10
        advice.append("🚶 歩数が少なめです。30分ほど散歩してみましょう。")

    # 運動
    if exercise >= 30:
        score += 15
    elif exercise >= 15:
        score += 5
        advice.append("🏃 あと15分運動するとさらに良くなります。")
    else:
        score -= 10
        advice.append("🏃 軽いウォーキングやストレッチを15〜30分行いましょう。")

    # 日光
    if sun_time >= 15:
        score += 10
    else:
        score -= 10
        advice.append("☀ 朝15分以上日光を浴びると体内時計が整います。")

    # カフェイン
    if coffee == "18時以降":
        score -= 15
        advice.append("☕ 18時以降のカフェインは避けましょう。")
    elif coffee == "15時まで":
        score += 5
    else:
        score += 10

    # スマホ
    if phone <= 30:
        score += 10
    elif phone <= 60:
        score += 0
        advice.append("📱 就寝1時間前からスマホを控えると睡眠の質が向上します。")
    else:
        score -= 20
        advice.append("📱 スマホ時間が長めです。今日は30分早く終了してみましょう。")

    # ストレス
    score -= (stress - 1) * 5

    if stress >= 4:
        advice.append("😌 寝る前に5分間の深呼吸やストレッチをおすすめします。")

    # ストレス原因分析
    if "テスト" in stress_reason:
        advice.append("📝 テスト期間ですね。25分勉強＋5分休憩（ポモドーロ法）がおすすめです。")

    if "レポート" in stress_reason:
        advice.append("📄 レポートは小さなタスクに分けて進めると負担が減ります。")

    if "アルバイト" in stress_reason:
        advice.append("💼 アルバイト後はぬるめのお風呂でリラックスしましょう。")

    if "人間関係" in stress_reason:
        advice.append("😊 信頼できる友人や家族と話す時間を作るのも効果的です。")

    score = max(0, min(score, 100))

    st.subheader("📊 分析結果")

    st.progress(score / 100)

    st.metric("😴 睡眠スコア", f"{score} 点")

    if score >= 80:
        robot = "🤖😊"
        prediction = "良い睡眠"
        st.success("今日は良い睡眠が期待できます！")
        st.balloons()

    elif score >= 60:
        robot = "🤖🙂"
        prediction = "普通"

    else:
        robot = "🤖😢"
        prediction = "睡眠不足の可能性"

    st.markdown(f"# {robot}")

    st.subheader("💡 AIアドバイス")

    if len(advice) == 0:
        st.success("今日はとても良い生活習慣です！この調子で23時までに就寝しましょう。")
    else:
        for a in advice:
            st.write("・", a)

    # データ保存
    # -----------------------------
    new_data = pd.DataFrame([{
        "日付": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "歩数": steps,
        "運動時間": exercise,
        "日光時間": sun_time,
        "カフェイン": coffee,
        "スマホ時間": phone,
        "ストレス": stress,
        "ストレス原因": stress_reason,
        "学習時間": study,
        "睡眠スコア": score,
        "予測": prediction,
        "実際": "未入力"
    }])

    history = pd.read_csv(FILE_NAME)
    history = pd.concat([history, new_data], ignore_index=True)
    history.to_csv(FILE_NAME, index=False)

st.markdown("---")

st.subheader("📈 睡眠スコア履歴")

history = pd.read_csv(FILE_NAME)

if len(history) > 0:

    st.dataframe(history, use_container_width=True)

    chart = history[["日付", "睡眠スコア"]].copy()
    chart = chart.set_index("日付")

    st.line_chart(chart)

    st.metric(
        "平均睡眠スコア",
        round(history["睡眠スコア"].mean(),1)
    )

    st.metric(
        "最高睡眠スコア",
        int(history["睡眠スコア"].max())
    )

    st.metric(
        "最低睡眠スコア",
        int(history["睡眠スコア"].min())
    )

    st.markdown("---")
st.subheader("🌅 翌朝の睡眠評価")

actual = st.selectbox(
    "実際によく眠れましたか？",
    ["未入力", "はい", "いいえ"]
)

if st.button("💾 実際の結果を保存"):

    history = pd.read_csv(FILE_NAME)

    if len(history) > 0:
        history.loc[len(history)-1, "実際"] = actual
        history.to_csv(FILE_NAME, index=False)

        st.success("保存しました！")

st.markdown("---")
st.subheader("📊 AI予測精度")

history = pd.read_csv(FILE_NAME)

valid = history[history["実際"] != "未入力"]

if len(valid) > 0:

    TP = len(valid[(valid["予測"]=="良い睡眠") & (valid["実際"]=="はい")])
    FP = len(valid[(valid["予測"]=="良い睡眠") & (valid["実際"]=="いいえ")])
    FN = len(valid[(valid["予測"]!="良い睡眠") & (valid["実際"]=="はい")])
    TN = len(valid[(valid["予測"]!="良い睡眠") & (valid["実際"]=="いいえ")])

    accuracy = (TP+TN)/(TP+TN+FP+FN)

    precision = TP/(TP+FP) if (TP+FP)>0 else 0

    recall = TP/(TP+FN) if (TP+FN)>0 else 0

    if precision+recall==0:
        f1=0
    else:
        f1=2*precision*recall/(precision+recall)

    c1,c2 = st.columns(2)

    with c1:
        st.metric("Accuracy", f"{accuracy:.2f}")
        st.metric("Precision", f"{precision:.2f}")

    with c2:
        st.metric("Recall", f"{recall:.2f}")
        st.metric("F1 Score", f"{f1:.2f}")

    st.success("AI予測精度を更新しました。")

else:

    st.info("翌朝評価を入力するとAccuracy・Precision・Recall・F1 Scoreを表示します。")
