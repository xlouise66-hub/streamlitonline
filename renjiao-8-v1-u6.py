import streamlit as st
import random

st.set_page_config(page_title="U6 英语练习系统", layout="wide")

# ================== U6 词汇表 ==================
vocab = {
    "yourself": "你自己",
    "engineer": "工程师",
    "fashion": "时尚",
    "designer": "设计师",
    "director": "导演；主管",
    "musician": "音乐家",
    "fireman": "消防员",
    "AI": "人工智能",
    "essay": "短文；论文",
    "classic": "经典的；典型的",
    "keep on doing sth": "继续做某事",
    "make sure": "确保；弄清楚",
    "try one's best": "尽最大努力",
    "literature": "文学",
    "athlete": "运动员",
    "photographer": "摄影师",
    "painter": "画家",
    "businessman": "商人",
    "actress": "女演员",
    "lawyer": "律师",
    "law": "法律",
    "bath": "洗澡；浴缸",
    "miss": "想念；错过",
    "be tired of": "厌倦……",
    "able": "有能力的",
    "stick": "坚持；粘贴",
    "stick to sth": "坚持……",
    "resolution": "决心；决议",
    "have (...) to do with sb / sth": "与……有关",
    "mini-goal": "小目标",
    "achieve": "实现；达到",
    "physical": "身体的；物理的",
    "health": "健康",
    "healthily": "健康地",
    "take up": "开始从事；占据",
    "photography": "摄影",
    "self-improvement": "自我提升",
    "confident": "自信的",
    "organized": "有条理的",
    "wisely": "明智地",
    "possible": "可能的",
    "paragraph": "段落",
    "introduce": "介绍",
    "meaning": "意义",
    "fall": "落下；跌倒",
    "ahead": "向前；提前",
    "put out": "扑灭；熄灭",
    "design": "设计",
    "bridge": "桥",
    "final": "最后的；期末的",
    "confidence": "信心；自信",
    "draw to a close": "接近尾声",
    "form": "形成；表格",
    "relationship": "关系",
    "push-up": "俯卧撑",
    "energetic": "精力充沛的",
    "last but not least": "最后但同样重要的"
}

# ================== 拼写练习题准备 ==================
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
