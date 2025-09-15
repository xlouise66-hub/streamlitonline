import streamlit as st
import random

st.set_page_config(page_title="英语练习系统 - Unit 3", layout="wide")

# ================== 词汇表 ==================
vocab = {
    "network": "网络",
    "flood": "洪水；水灾",
    "multimedia": "多媒体",
    "expert": "专家",
    "mobile": "可移动的",
    "payment": "付款；支付",
    "warn": "提醒注意；警告",
    "treatment": "治疗；疗法",
    "data": "数据",
    "company": "公司",
    "traffic": "路上行驶的车辆；交通",
    "flow": "（人或事物）涌流；流动",
    "smoothly": "平稳地；连续而流畅地",
    "laptop": "笔记本电脑",
    "screen": "屏幕",
    "weight": "重量",
    "digital": "数码的",
    "social": "社交的",
    "message": "（书面或口头的）信息",
    "interview": "采访",
    "positive": "正面的；积极的",
    "negative": "消极的",
    "effect": "影响",
    "opinion": "意见；看法",
    "novel": "（长篇）小说",
    "comment": "评论",
    "basis": "基础",
    "microprocessor": "微处理器",
    "microchip": "微芯片；芯片",
    "major": "主要的；重要的",
    "breakthrough": "突破；重大进展",
    "electronic": "电子的",
    "software": "软件",
    "app": "（application 的缩写）应用程序；应用软件",
    "era": "时代；纪元",
    "download": "下载",
    "tiny": "微小的",

    # 短语与表达
    "connect to": "连接",
    "bring big changes to": "给……带来重大变化",
    "mobile payment": "移动支付",
    "take ... for example": "以……为例",
    "rubbish bin": "垃圾箱",
    "social media": "社交媒体",
    "in person": "亲自；亲身",
    "the general public": "公众；大众"
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
