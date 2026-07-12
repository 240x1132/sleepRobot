import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="Smart Sleep Robot",
    page_icon="🤖",
    layout="centered"
)

st.title("😴 Smart Sleep Robot 🤖")
st.caption("日中の行動から今夜の睡眠を予測します")

st.markdown("---")

st.subheader("📝 今日の行動")

steps = st.slider("🚶 今日の歩数", 0, 20000, 8000)

exercise = st.slider("🏃 運動時間（分）", 0, 120, 30)

sun = st.checkbox("☀ 朝日を浴びた")

coffee = st.selectbox(
    "☕ カフェイン",
    ["飲んでない", "15時まで", "18時以降"]
)

phone = st.slider("📱 夜のスマホ使用時間（分）", 0, 180, 30)

stress = st.slider("😰 今日のストレス",1,5,3)

st.markdown("---")

if st.button("😴 睡眠スコアを計算",use_container_width=True):

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

    score -= (stress-1)*5

    score=max(0,min(score,100))

    st.markdown("## 📊 結果")

    st.progress(score/100)

    st.metric("😴 睡眠スコア",f"{score}点")

    if score>=80:

        robot="🤖😊"

        advice="""
### 💡 AIアドバイス

今日はとても良い生活習慣でした！

この調子で23時までに寝ると、
さらに質の良い睡眠が期待できます。
"""

        st.balloons()

    elif score>=60:

        robot="🤖🙂"

        advice="""
### 💡 AIアドバイス

あと少し改善できます！

・スマホ時間を減らす
・軽い運動をする
"""

    else:

        robot="🤖😢"

        advice="""
### 💡 AIアドバイス

睡眠の質が低下する可能性があります。

・スマホは30分早く終了
・夕方以降のカフェインを控える
・朝日を浴びましょう
"""

    st.markdown(f"# {robot}")

    st.write(advice)
