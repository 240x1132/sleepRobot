import streamlit as st

st.set_page_config(page_title="Smart Sleep Robot", page_icon="😴")

st.title("😴 Smart Sleep Robot")
st.write("日中の行動から今夜の睡眠スコアを予測します。")

steps = st.slider("🚶 今日の歩数", 0, 20000, 8000)
exercise = st.slider("🏃 運動時間（分）", 0, 120, 30)
sun = st.checkbox("☀ 朝日を浴びた")
coffee = st.selectbox(
    "☕ カフェイン",
    ["飲んでない", "15時まで", "18時以降"]
)
phone = st.slider("📱 夜のスマホ使用時間（分）", 0, 180, 30)

if st.button("睡眠スコアを計算"):
    score = 50

    if steps >= 8000:
        score += 15
    if exercise >= 30:
        score += 15
    if sun:
        score += 10
    if coffee == "18時以降":
        score -= 15
    if phone >= 60:
        score -= 20
    elif phone <= 30:
        score += 10

    score = max(0, min(score, 100))

    st.subheader(f"😴 睡眠スコア：{score}点")

    if score >= 80:
        st.success("😊 とても良い睡眠が期待できます！")
    elif score >= 60:
        st.warning("🙂 あと少し改善できます。")
    else:
        st.error("😢 睡眠の質が低下しそうです。")
