import streamlit as st
import random

# -----------------------
# 不规则动词过去式词汇表
# -----------------------
vocab = {
    "let": "让", "lay": "躺下", "lit": "点燃", "lost": "丢失", "made": "制作",
    "meant": "意味着", "met": "遇见", "paid": "支付", "put": "放置", "read": "阅读",
    "rode": "骑", "rang": "响铃", "rose": "上升", "ran": "跑", "said": "说",
    "saw": "看见", "sold": "卖", "sent": "发送", "shone": "照耀", "shot": "射击",
    "showed": "展示", "shut": "关闭", "sang": "唱歌", "sat": "坐", "slept": "睡觉",
    "spoke": "说话", "spent": "花费", "stood": "站立", "stole": "偷", "swam": "游泳",
    "took": "拿", "taught": "教", "tore": "撕裂", "told": "告诉", "thought": "思考",
    "threw": "扔", "understood": "理解", "woke": "醒来", "wore": "穿", "won": "赢",
    "wrote": "写"
}

# -----------------------
# 初始化题目，只执行一次
# -----------------------
if 'questions' not in st.session_state:
    words = list(vocab.items())
    questions = []

    while len(questions) < 40:
        word, meaning = random.choice(words)

        # 随机决定题型：英译中 或 中译英
        question_type = random.choice(["en_to_cn", "cn_to_en"])

        if question_type == "en_to_cn":
            question_text = f"What is the meaning of '{word}'?"
            correct_answer = meaning
            wrong_options = random.sample([m for k, m in words if m != meaning], 4)
            options = wrong_options
            options.insert(random.randint(0, 4), correct_answer)

        else:  # cn_to_en
            question_text = f"Which word means '{meaning}' in past tense?"
            correct_answer = word
            wrong_options = random.sample([k for k, m in words if k != word], 4)
            options = wrong_options
            options.insert(random.randint(0, 4), correct_answer)

        questions.append({
            "question": question_text,
            "options": options,
            "answer": correct_answer
        })

    st.session_state.questions = questions
    st.session_state.user_answers = [""] * len(questions)

# -----------------------
# Streamlit界面
# -----------------------
st.title("不规则动词测试（40题，满分100分）")
questions = st.session_state.questions
user_answers = st.session_state.user_answers

for i, q in enumerate(questions):
    st.subheader(f"Question {i+1}: {q['question']}")
    # 固定选项顺序，绑定session_state
    user_answers[i] = st.radio(
        "Select an answer:",
        q["options"],
        key=f"q{i}",
        index=q["options"].index(user_answers[i]) if user_answers[i] else 0
    )

# -----------------------
# 提交按钮
# -----------------------
if st.button("提交答案"):
    score = 0
    for ua, q in zip(user_answers, questions):
        if ua == q["answer"]:
            score += 2.5  # 每题2.5分
    st.success(f"你的总分是：{score} / 100 分")

    st.subheader("所有正确答案：")
    option_labels = ['A', 'B', 'C', 'D', 'E']
    for i, q in enumerate(questions):
        st.write(f"Question {i+1}: {q['question']}")
        for idx, opt in enumerate(q['options']):
            mark = "(正确答案)" if opt == q["answer"] else ""
            st.write(f"{option_labels[idx]}. {opt} {mark}")
