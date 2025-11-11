import streamlit as st
import random

st.set_page_config(page_title="U6 英语练习系统", layout="wide")

# ================== U6 词汇表 ==================
vocab = {
    "guide": "导游；指南",
    "east": "东；东方",
    "west": "西；西方",
    "mix": "混合",
    "western": "西方的",
    "style": "风格",
    "popular": "受欢迎的",
    "site": "地点；场所",
    "across": "横过；在……对面",
    "adult": "成年人",
    "senior": "年长的；高级的",
    "customer": "顾客",
    "design": "设计",
    "else": "其他的",
    "suggestion": "建议",
    "tip": "提示；小建议",
    "historic": "有历史意义的",
    "list": "清单；列出",
    "landscape": "风景；景观",
    "memory": "记忆；回忆",
    "general": "普遍的；一般的",
    "sight": "景象；名胜",
    "natural": "自然的",
    "almost": "几乎",
    "become": "成为",
    "gateway": "入口；门户",
    "influence": "影响",
    "artwork": "艺术品",
    "painting": "绘画；画作",
    "scene": "场景；风景",
    "wife": "妻子",
    "stone": "石头",
    "reflection": "倒影；反思",
    "tourist spot": "旅游景点",
    "light up": "点亮；照亮",
    "in the center of": "在……中心",
    "be interested in": "对……感兴趣",
    "historic site": "历史遗迹",
    "in memory of": "纪念……"
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
    st.header("U6 词汇选择题（40题）")
    for i, q in enumerate(st.session_state.vocab_questions, 1):
        st.write(f"Q{i}: {q['question']}")
        st.radio(f"选项Q{i}", q["options"], key=f"vocab_{i}")

# ================== 拼写练习 ==================
elif mode == "拼写练习（中英互译）":
    st.header("U6 拼写练习（15题）")
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
