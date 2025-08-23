import streamlit as st
import random

# =========================
# 不规则动词三列词汇
# 英文原形: [过去式, 过去分词, 中文意思]
# =========================
vocab_full = {
    "let": ["let", "let", "让"],
    "lie": ["lay", "lain", "躺下"],
    "light": ["lit", "lit", "点燃"],
    "lose": ["lost", "lost", "丢失"],
    "make": ["made", "made", "制作"],
    "mean": ["meant", "meant", "意味着"],
    "meet": ["met", "met", "遇见"],
    "pay": ["paid", "paid", "支付"],
    "put": ["put", "put", "放置"],
    "read": ["read", "read", "阅读"],
    "ride": ["rode", "ridden", "骑"],
    "ring": ["rang", "rung", "响铃"],
    "rise": ["rose", "risen", "升起"],
    "run": ["ran", "run", "跑"],
    "say": ["said", "said", "说"],
    "see": ["saw", "seen", "看见"],
    "sell": ["sold", "sold", "卖"],
    "send": ["sent", "sent", "发送"],
    "shine": ["shone", "shone", "发光"],
    "shoot": ["shot", "shot", "射击"],
    "show": ["showed", "shown", "展示"],
    "shut": ["shut", "shut", "关闭"],
    "sing": ["sang", "sung", "唱歌"],
    "sit": ["sat", "sat", "坐"],
    "sleep": ["slept", "slept", "睡觉"],
    "speak": ["spoke", "spoken", "说话"],
    "spend": ["spent", "spent", "花费"],
    "stand": ["stood", "stood", "站立"],
    "steal": ["stole", "stolen", "偷"],
    "swim": ["swam", "swum", "游泳"],
    "take": ["took", "taken", "拿"],
    "teach": ["taught", "taught", "教"],
    "tear": ["tore", "torn", "撕裂"],
    "tell": ["told", "told", "告诉"],
    "think": ["thought", "thought", "思考"],
    "throw": ["threw", "thrown", "扔"],
    "understand": ["understood", "understood", "理解"],
    "wake": ["woke", "woken", "醒来"],
    "wear": ["wore", "worn", "穿"],
    "win": ["won", "won", "赢"],
    "write": ["wrote", "written", "写"]
}

# ------------------------
# 构建题目列表（60题）
# ------------------------
if 'questions' not in st.session_state:
    # 将三列拆开成可考的形式
    all_words = []
    for base, forms in vocab_full.items():
        en_base, en_past, en_pp, cn = forms[0], forms[1], forms[2], forms[2] if len(forms)==3 else forms[2]
        all_words.append((en_base, cn))
        all_words.append((en_past, cn))
        all_words.append((en_pp, cn))
    # 去重
    all_words = list(set(all_words))
    
    # 随机抽取 40 题
    questions_sample = random.sample(all_words, 40)
    questions = []

    for word, meaning in questions_sample:
        # 随机决定题型 True=英译中，False=中译英
        if random.choice([True, False]):
            question_text = f"'{word}' 的中文意思是？"
            correct_answer = meaning
            wrong_options = random.sample([m for w, m in all_words if m != meaning], 4)
        else:
            question_text = f"“{meaning}” 对应的英文是？"
            correct_answer = word
            wrong_options = random.sample([w for w, m in all_words if w != word], 4)

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

# ------------------------
# Streamlit 界面
# ------------------------
st.title("不规则动词综合测试（原形/过去式/过去分词）40题，满分100")
questions = st.session_state.questions
user_answers = st.session_state.user_answers
option_labels = ['A', 'B', 'C', 'D', 'E']

for i, q in enumerate(questions):
    st.subheader(f"第 {i+1} 题: {q['question']}")
    user_answers[i] = st.radio(
        "请选择答案：",
        q["options"],
        index=q["options"].index(user_answers[i]) if user_answers[i] else 0,
        key=f"q{i}"
    )

# ------------------------
# 提交按钮
# ------------------------
if st.button("提交答案"):
    score = 0
    for ua, q in zip(user_answers, questions):
        if ua == q["answer"]:
            score += 100 / len(questions)
    st.success(f"你的总分是：{round(score)} / 100 分")

    st.subheader("所有正确答案：")
    for i, q in enumerate(questions):
        st.write(f"第 {i+1} 题: {q['question']}")
        for idx, opt in enumerate(q['options']):
            mark = " ✅" if opt == q["answer"] else ""
            st.write(f"{option_labels[idx]}. {opt} {mark}")
