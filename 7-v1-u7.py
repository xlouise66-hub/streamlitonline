import streamlit as st
import random

st.set_page_config(page_title="U7 英语练习系统", layout="wide")

# ================== U7 词汇表 ==================
vocab = {
    "literature": "文学",
    "act": "表演；行动",
    "appreciate": "欣赏；感激",
    "join": "加入；参加",
    "definitely": "当然；明确地",
    "fair": "展览会；公平的",
    "rocket": "火箭",
    "launch": "发射；推出",
    "shout": "喊叫",
    "power": "力量；能源",
    "moment": "时刻；瞬间",
    "member": "成员",
    "shape": "形状；塑造",
    "hike": "远足；徒步旅行",
    "recently": "最近",
    "attend": "出席；参加",
    "charity": "慈善",
    "sale": "销售；拍卖",
    "snack": "零食；点心",
    "decorate": "装饰",
    "difference": "差异；不同",
    "compete": "竞争；比赛",
    "event": "事件；活动",
    "spoon": "勺子",
    "annual": "每年的",
    "fantastic": "极好的；奇妙的",
    "dollar": "美元",
    "pie": "馅饼",
    "equipment": "设备；装备",
    "clubs fair": "社团展",
    "solar power": "太阳能",
    "of course": "当然",
    "remote control": "遥控器",
    "turn around": "转身；好转",
    "make a difference": "产生影响",
    "primary school": "小学",
    "fall off": "跌落；减少"
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
    st.header("U7 词汇选择题（40题）")
    for i, q in enumerate(st.session_state.vocab_questions, 1):
        st.write(f"Q{i}: {q['question']}")
        st.radio(f"选项Q{i}", q["options"], key=f"vocab_{i}")

# ================== 拼写练习 ==================
elif mode == "拼写练习（中英互译）":
    st.header("U7 拼写练习（15题）")
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
