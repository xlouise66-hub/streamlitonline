import streamlit as st
import random

# =========================
# 不规则动词过去分词（第三列）词汇
# =========================
vocab = {
    "let": "让", "lain": "躺下", "lit": "点燃", "lost": "丢失", "made": "制作",
    "meant": "意味着", "met": "遇见", "paid": "支付", "put": "放置", "read": "阅读",
    "ridden": "骑", "rung": "响铃", "risen": "升起", "run": "跑", "said": "说",
    "seen": "看见", "sold": "卖", "sent": "发送", "shone": "发光", "shot": "射击",
    "shown": "展示", "shut": "关闭", "sung": "唱歌", "sat": "坐", "slept": "睡觉",
    "spoken": "说话", "spent": "花费", "stood": "站立", "stolen": "偷", "swum": "游泳",
    "taken": "拿", "taught": "教", "torn": "撕裂", "told": "告诉", "thought": "思考",
    "thrown": "扔", "understood": "理解", "woken": "醒来", "worn": "穿", "won": "赢",
    "written": "写"
}

# =========================
# 初始化题目
# =========================
if 'questions' not in st.session_state:
    words = list(vocab.items())
    random.shuffle(words)  # 打乱顺序
    questions = []

    for word, meaning in words:
        question_type = random.choice(["en_to_cn", "cn_to_en"])
        if question_type == "en_to_cn":
            # 英译中
            wrong_options = random.sample([m for _, m in words if m != meaning], 4)
            correct_index = random.randint(0, 4)
            options = wrong_options
            options.insert(correct_index, meaning)
            questions.append({
                "question": f"'{word}' 的中文意思是？",
                "options": options,
                "answer": meaning
            })
        else:
            # 中译英
            wrong_options = random.sample([w for w, _ in words if w != word], 4)
            correct_index = random.randint(0, 4)
            options = wrong_options
            options.insert(correct_index, word)
            questions.append({
                "question": f"“{meaning}” 对应的英文是？",
                "options": options,
                "answer": word
            })

    st.session_state.questions = questions
    st.session_state.user_answers = [""] * len(questions)

# =========================
# Streamlit UI
# =========================
st.title("不规则动词过去分词测试（满分100分）")
questions = st.session_state.questions
user_answers = st.session_state.user_answers

option_labels = ['A', 'B', 'C', 'D', 'E']

for i, q in enumerate(questions):
    st.subheader(f"第 {i+1} 题: {q['question']}")
    user_answers[i] = st.radio(
        "请选择一个答案：",
        q["options"],
        index=q["options"].index(user_answers[i]) if user_answers[i] else 0,
        key=f"q{i}"
    )

# =========================
# 提交按钮
# =========================
if st.button("提交答案"):
    score = 0
    for ua, q in zip(user_answers, questions):
        if ua == q["answer"]:
            score += 100 / len(questions)

    st.success(f"你的总分是：{round(score)} / 100 分")

    st.subheader("正确答案：")
    for i, q in enumerate(questions):
        st.write(f"第 {i+1} 题: {q['question']}")
        for idx, opt in enumerate(q['options']):
            mark = "(✔ 正确答案)" if opt == q["answer"] else ""
            st.write(f"{option_labels[idx]}. {opt} {mark}")
