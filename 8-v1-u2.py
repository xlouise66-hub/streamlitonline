import streamlit as st
import random

st.set_page_config(page_title="英语练习系统 - Unit 2", layout="wide")

# ================== 词汇表 ==================
vocab = {
    "flight": "（尤指乘飞机的）航程",
    "schedule": "日程安排",
    "everywhere": "到处；各个地方",
    "challenge": "向（某人）挑战",
    "prize": "奖赏；奖励",
    "promise": "承诺；保证",
    "chessboard": "国际象棋棋盘",
    "silver": "银",
    "reply": "回复；答复",
    "hesitation": "犹豫",
    "wonder": "想知道；琢磨",
    "agree": "同意；赞成",
    "per cent": "百分之……",
    "currently": "目前；当前",
    "check": "检查；核查",
    "budget": "预算",
    "province": "省份",
    "sharply": "急剧地；突然大幅度地",
    "count": "计算（或清点）总数",
    "system": "系统",
    "symbol": "符号；记号",
    "represent": "代表",
    "exactly": "准确地；确切地",

    # 短语与表达
    "flight schedule": "航班时刻表",
    "price tag": "价格标签",
    "for a moment": "片刻；一会儿",
    "without hesitation": "毫不犹豫",
    "go up": "上升",
    "go down": "下降",
    "write down": "写下；记下",
    "instead of": "代替；作为……的替换"
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
