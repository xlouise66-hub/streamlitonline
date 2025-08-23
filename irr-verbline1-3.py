import streamlit as st
import random

# -----------------------
# 词汇表（英文 -> 中文）
# -----------------------
vocab = {
    "been": "已经",
    "beaten": "被打",
    "become": "变成",
    "begun": "开始了",
    "bitten": "被咬",
    "blown": "吹过",
    "broken": "打破",
    "brought": "带来",
    "built": "建造",
    "bought": "买了",
    "caught": "抓住",
    "chosen": "选择",
    "come": "来",
    "cost": "花费",
    "cut": "切",
    "done": "做完",
    "drawn": "画过",
    "drunk": "喝过",
    "driven": "驾驶",
    "eaten": "吃过",
    "fallen": "掉落",
    "felt": "感觉",
    "fought": "打过仗",
    "found": "找到",
    "flown": "飞过",
    "forgotten": "忘记",
    "got": "得到",
    "given": "给过",
    "gone": "去过",
    "grown": "成长",
    "hung": "悬挂",
    "had": "拥有",
    "heard": "听到",
    "hidden": "隐藏",
    "hit": "击打",
    "held": "握住",
    "hurt": "伤害",
    "kept": "保持",
    "known": "知道",
    "left": "离开",
    "lent": "借出"
}

# -----------------------
# 初始化题目（每个词只出现一次）
# -----------------------
if 'questions' not in st.session_state:
    words = list(vocab.items())
    random.shuffle(words)
    questions = []
    
    for word, meaning in words:
        # 随机决定题型：True=英译中，False=中译英
        if random.choice([True, False]):
            question_text = f"What is the meaning of '{word}'?"
            correct_answer = meaning
            wrong_options = random.sample([m for k, m in words if m != meaning], 4)
        else:
            question_text = f"哪个英文单词的意思是：'{meaning}'?"
            correct_answer = word
            wrong_options = random.sample([k for k, m in words if k != word], 4)

        # 插入正确答案到随机位置
        options = wrong_options.copy()
        correct_index = random.randint(0, 4)
        options.insert(correct_index, correct_answer)

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
st.title("不规则动词第三列测试（满分100分）")
questions = st.session_state.questions
user_answers = st.session_state.user_answers

for i, q in enumerate(questions):
    st.subheader(f"Question {i+1}: {q['question']}")
    user_answers[i] = st.radio(
        "选择答案：", 
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
            score += 100 / len(questions)  # 自动按题数算分
    st.success(f"你的总分是：{round(score)} / 100 分")

    st.subheader("所有正确答案：")
    option_labels = ['A', 'B', 'C', 'D', 'E']
    for i, q in enumerate(questions):
        st.write(f"Question {i+1}: {q['question']}")
        for idx, opt in enumerate(q['options']):
            mark = " ✅" if opt == q["answer"] else ""
            st.write(f"{option_labels[idx]}. {opt} {mark}")
