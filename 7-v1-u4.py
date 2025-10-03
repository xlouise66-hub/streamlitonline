import streamlit as st
import random

st.set_page_config(page_title="英语练习系统", layout="wide")

# ================== 词汇表 ==================
vocab = {
    "system": "系统",
    "file": "文件",
    "amazing": "令人惊奇的",
    "planet": "行星",
    "billion": "十亿",
    "cover": "覆盖",
    "area": "区域；面积",
    "freezing": "极冷的",
    "north": "北方",
    "pole": "极点；顶端",
    "desert": "沙漠",
    "metre": "米",
    "reach": "到达；达到",
    "grain": "谷物；颗粒",
    "wide": "宽的；广阔的",
    "whale": "鲸",
    "butterfly": "蝴蝶",
    "provide": "提供",
    "explore": "探索",
    "disappear": "消失",
    "plastic": "塑料",
    "pollution": "污染",
    "protect": "保护",
    "chemical": "化学物质",
    "groundwater": "地下水",
    "burn": "燃烧",
    "oil": "石油；油",
    "gas": "天然气；气体",
    "harmful": "有害的",
    "website": "网站",
    "own": "自己的；拥有",
    "emperor": "皇帝",
    "hunt": "打猎；追捕",
    "war": "战争",
    "sandstorm": "沙尘暴",
    "solution": "解决方案",
    "blow": "吹",
    "generation": "一代；世代",
    "solar system": "太阳系",
    "fact file": "档案；资料文件",
    "be covered by": "被…覆盖",
    "as far as we know": "据我们所知",
    "sea level": "海平面",
    "what's more": "而且；更重要的是",
    "provide..with..": "为…提供…",
    "plastic pollution": "塑料污染",
    "cut down": "砍伐；削减",
    "hundreds of": "数百；许多",
    "blow away": "吹走"
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
