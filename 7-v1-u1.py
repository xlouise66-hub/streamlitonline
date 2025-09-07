import streamlit as st
import random

st.set_page_config(page_title="英语练习系统", layout="wide")

# ================== 词汇表 ==================
vocab = {
    "guitar": "吉他",
    "honest": "诚实的",
    "patient": "耐心的",
    "improve": "提高",
    "confident": "自信的",
    "courage": "勇气",
    "friendship": "友谊",
    "admiration": "钦佩",
    "respect": "尊重",
    "support": "支持",
    "trust": "信任",
    "survey": "调查",
    "personal": "个人的",
    "quality": "品质",
    "caring": "关心的",
    "describe": "描述",
    "appearance": "外貌",
    "straight": "直的",
    "dark": "黑暗的",
    "same": "相同的",
    "basic": "基本的",
    "thought": "思想",
    "however": "然而",
    "glad": "高兴的",
    "rise": "上升",
    "end": "结束",
    "heart": "心脏",
    "be good at": "擅长",
    "turn to somebody for help": "向某人求助",
    "after school": "放学后",
    "be willing to do something": "愿意做某事",
    "thanks to": "多亏",
    "count on": "依靠",
    "medium height": "中等身高",
    "modern dance": "现代舞",
    "take care of": "照顾",
    "watch over": "看护",
    "rise into": "升入",
    "cry out": "大声喊叫",
    "cry oneself to sleep": "哭着入睡",
    "wake up": "醒来",
    "come and go": "来来去去",
    "take somebody’s place": "取代某人",
    "come along": "一起来"
}

# ================== 拼写练习 ==================
spelling_exercises = [{"cn": cn, "en": en} for en, cn in vocab.items()]

# ================== 初始化随机题目 ==================
if "initialized" not in st.session_state:
    # 词汇选择题（中英互译）40题
    vocab_items = list(vocab.items())
    vocab_questions = []
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
    st.header("词汇选择题（40题）")
    for i, q in enumerate(st.session_state.vocab_questions, 1):
        st.write(f"Q{i}: {q['question']}")
        st.radio(f"选项Q{i}", q["options"], key=f"vocab_{i}")

# ================== 拼写练习 ==================
elif mode == "拼写练习（中英互译）":
    st.header("拼写练习（15题）")
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
