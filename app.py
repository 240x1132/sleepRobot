import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Smart Sleep Robot", page_icon="🤖", layout="centered")

FILE_NAME="sleep_log.csv"

if not os.path.exists(FILE_NAME):
    pd.DataFrame(columns=[
        "日付","歩数","運動時間","日光","カフェイン","スマホ","ストレス","睡眠スコア"
    ]).to_csv(FILE_NAME,index=False)

st.title("😴 Smart Sleep Robot 🤖")
st.caption("日中の行動から今夜の睡眠を予測します")

steps=st.slider("🚶 今日の歩数",0,20000,8000)
exercise=st.slider("🏃 運動時間（分）",0,120,30)
sun=st.checkbox("☀ 朝日を浴びた")
coffee=st.selectbox("☕ カフェイン",["飲んでない","15時まで","18時以降"])
phone=st.slider("📱 夜のスマホ使用時間（分）",0,180,30)
stress=st.slider("😰 今日のストレス",1,5,3)

if st.button("😴 睡眠スコアを計算",use_container_width=True):
    score=50
    if steps>=8000: score+=15
    if exercise>=30: score+=15
    if sun: score+=10
    if coffee=="18時以降": score-=15
    if phone>=60: score-=20
    elif phone<=30: score+=10
    score-=(stress-1)*5
    score=max(0,min(score,100))

    new_data=pd.DataFrame([{
        "日付":datetime.now().strftime("%Y-%m-%d %H:%M"),
        "歩数":steps,
        "運動時間":exercise,
        "日光":sun,
        "カフェイン":coffee,
        "スマホ":phone,
        "ストレス":stress,
        "睡眠スコア":score
    }])

    history=pd.read_csv(FILE_NAME)
    history=pd.concat([history,new_data],ignore_index=True)
    history.to_csv(FILE_NAME,index=False)

    st.subheader("📊 結果")
    st.progress(score/100)
    st.metric("😴 睡眠スコア",f"{score}点")

    if score>=80:
        robot="🤖😊"
        st.balloons()
        advice="今日はとても良い生活習慣でした！この調子で23時までに寝ましょう。"
    elif score>=60:
        robot="🤖🙂"
        advice="あと少し改善できます。スマホ時間を減らしてみましょう。"
    else:
        robot="🤖😢"
        advice="スマホ時間やカフェインを見直すと睡眠改善が期待できます。"

    st.markdown(f"# {robot}")
    st.info(advice)

st.markdown("---")
st.subheader("📈 睡眠スコア履歴")

history=pd.read_csv(FILE_NAME)
st.dataframe(history,use_container_width=True)

if not history.empty:
    chart=history[["日付","睡眠スコア"]].copy()
    chart=chart.set_index("日付")
    st.line_chart(chart)

