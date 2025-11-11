import streamlit as st
import random

st.set_page_config(page_title="U5 英语练习系统", layout="wide")

# ================== U5 词汇表 ==================
vocab = {
    "spacesuit": "宇航服",
    "collect": "收集",
    "leave": "离开",
    "kilometre": "千米",
    "weak": "虚弱的",
    "tie": "系；绑",
    "low": "低的",
    "weigh": "称重；重量为",
    "breathe": "呼吸",
    "facility": "设施",
    "adventure": "冒险",
    "pass": "经过；通过",
    "experiment": "实验",
    "prepare": "准备",
    "dream": "梦想；梦",
    "chance": "机会",
    "send": "发送；派遣",
    "introduction": "介绍",
    "view": "景色；看法",
    "someday": "将来某一天",
    "experience": "经历；经验",
    "lander": "着陆器",
    "island": "岛屿",
    "ancient": "古代的",
    "poem": "诗",
    "express": "表达",
    "determination": "决心",
    "universe": "宇宙",
    "already": "已经",
    "century": "世纪",
    "neighbor": "邻居",
    "circle": "圆；环绕",
    "surface": "表面",
    "release": "释放；发表",
    "kilogram": "千克",
    "programme": "节目；计划",
    "space station": "空间站",
    "do exercise": "做运动",
    "take photos": "拍照",
    "get into orbit": "进入轨道",
    "thousands of": "成千上万的"
}

# ================== 拼写练习 ==================
spelling_exercises = [{"cn": cn, "en": en} for en, cn in vocab.items()]

# ================== 初始化随机题目 ==================
if "initialized" not in st.session_state:
    vocab_items = list(vocab.items())
    vocab_questions = []

    # 词汇选择题（中英互译）40题
    for _ in range(40):
        word, meaning = random.choice(vocab_items)
        if random.choice([True, False]):  # 英文题目
            question = f"What is the meaning of '{word}'?"
            answer = meaning
            options = [answer] + random.sample([m for _, m in vocab_items if m != meaning], 4)
        else:  # 中文题目
            question = f"‘{meaning}’ 用英语怎么说？"
            answer = word
            options = [answer] + random.sample([w for w, _ in vocab_items if w != word], 4)
        random.shuffle(options)
        vocab_questions.append({"question": question, "options": options, "answer": answer})
    st.session_state.vocab_questions = vocab_questions

    # 拼写练习 15题
    st.session_state.spelling = random.sample(spelling_exercises, min(15, len(spelling_exercises)))

    st.session_state.initialized = True

# ================== 页面结构 ==================
mode = st.radio("选择练习模式", ["词汇选择题（中英互译）", "拼写练习（中英互译）"])

# ================== 词汇选择题 ==================
if mode == "词汇选择题（中英互译）":
    st.header("U5 词汇选择题（40题）")
    for i, q in enumerate(st.session_state.vocab_questions, 1):
        st.write(f"Q{i}: {q['question']}")
        st.radio(f"选项Q{i}", q["options"], key=f"vocab_{i}")

# ================== 拼写练习 ==================
elif mode == "拼写练习（中英互译）":
    st.header("U5 拼写练习（15题）")
    for i, q in enumerate(st.session_state.spelling, 1):
        st.write(f"Q{i}: 请写出“{q['cn']}”的英文拼写")
        st.text_input(f"答案Q{i}", key=f"spell_{i}")

# ================== 提交答案 ==================
if st.button("提交答案"):
    score = 0
    wrong = []

    if mode == "词汇选择题（中英互译）":
        for i, q in enumerate(st.session_state.vocab_questions, 1):
            ans = st.session_state.get(f"vocab_{i}")
            if ans == q["answer"]:
                score += 1
            else:
                wrong.append((i, q["question"], ans, q["answer"]))

    elif mode == "拼写练习（中英互译）":
        for i, q in enumerate(st.session_state.spelling, 1):
            ans = st.session_state.get(f"spell_{i}", "").strip().lower()
            if ans == q["en"].lower():
                score += 1
            else:
                wrong.append((i, q["cn"], ans, q["en"]))

    total = 40 if mode == "词汇选择题（中英互译）" else 15
    st.success(f"得分：{score} / {total}")

    if wrong:
        st.error("以下是错题：")
        for i, question, user_ans, correct in wrong:
            st.write(f"Q{i}: {question} 你的答案：{user_ans} ✅ 正确答案：{correct}")
