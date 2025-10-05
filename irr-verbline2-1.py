import streamlit as st
import random

# -----------------------
# 词汇表（英语动词 -> 中文）
# -----------------------
vocab = {
    "let": "让", "lie": "躺", "light": "点燃", "lose": "丢失", "make": "制造",
    "mean": "意味着", "meet": "遇见", "pay": "支付", "put": "放", "read": "阅读",
    "ride": "骑", "ring": "响", "rise": "升起", "run": "跑", "say": "说",
    "see": "看见", "sell": "卖", "send": "发送", "shine": "发光", "shoot": "射击",
    "show": "展示", "shut": "关闭", "sing": "唱", "sit": "坐", "sleep": "睡觉",
    "speak": "说话", "spend": "花费", "stand": "站立", "steal": "偷", "swim": "游泳",
    "take": "拿", "teach": "教", "tear": "撕", "tell": "告诉", "think": "思考",
    "throw": "扔", "understand": "理解", "wake": "醒来", "wear": "穿", "win": "赢",
    "write": "写"
}

# -----------------------
# 初始化题目，只执行一次
# -----------------------
if 'questions' not in st.session_state:
    words = list(vocab.items())
    random.shuffle(words)  # 打乱顺序
    questions = []

    used_words = set()  # 避免重复题目

    while len(questions) < 40 and len(used_words) < len(words):
        word, meaning = random.choice(words)
        if word in used_words:
            continue  # 避免重复题目
        used_words.add(word)

        # 随机题型：True=英译中，False=中译英
        is_eng_to_ch = random.choice([True, False])
        if is_eng_to_ch:
            question_text = f"What is the meaning of '{word}'?"
            correct_answer = meaning
            wrong_options = random.sample([m for k, m in words if m != meaning], 4)
        else:
            question_text = f"'{meaning}' 的英文是？"
            correct_answer = word
            wrong_options = random.sample([k for k, m in words if k != word], 4)

        # 插入正确答案到随机位置
        correct_index = random.randint(0, 4)
        options = wrong_options.copy()
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
st.title("40题英语动词测试（中英混合题型）")
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
    wrong_list = []

    for idx, (ua, q) in enumerate(zip(user_answers, questions)):
        if ua == q["answer"]:
            score += 2.5  # 每题2.5分
        else:
            wrong_list.append((idx + 1, q['question'], ua, q['answer']))

    st.success(f"你的总分是：{score} / 100 分")

    if wrong_list:
        st.subheader("错题回顾：")
        for i, q_text, user_ans, correct_ans in wrong_list:
            st.write(f"Question {i}: {q_text}")
            st.write(f"❌ 你的答案: {user_ans}")
            st.write(f"✅ 正确答案: {correct_ans}")
            st.write("---")
    else:
        st.balloons()
        st.success("太棒啦！全部答对 🎉")
