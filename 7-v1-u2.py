import streamlit as st
import random

st.set_page_config(page_title="英语练习系统", layout="wide")

# ================== 词汇表 ==================
vocab = {
    "geography": "地理",
    "corner": "角落",
    "activity": "活动",
    "club": "俱乐部",
    "practice": "练习",
    "solve": "解决",
    "develop": "发展",
    "skill": "技能",
    "teen": "青少年",
    "magazine": "杂志",
    "teenager": "青少年",
    "greeting": "问候",
    "grade": "年级",
    "energy": "精力",
    "drama": "戏剧",
    "sincerely": "真诚地",
    "diary": "日记",
    "project": "项目",
    "poster": "海报",
    "realize": "意识到",
    "luckily": "幸运地",
    "just": "刚刚/只是",
    "presentation": "展示/演讲",
    "mood": "心情",
    "mind": "介意/心思",
    "pack": "打包",
    "celebrate": "庆祝",
    "success": "成功",
    "rocky": "多岩石的",
    "do the dishes": "洗碗",
    "junior high school": "初中",
    "take part in": "参加",
    "look forward to": "期待",
    "daily life": "日常生活",
    "go to bed": "上床睡觉",
    "get up": "起床",
    "on foot": "步行",
    "full of energy": "精力充沛",
    "get ready for": "为…做好准备",
    "put on": "穿上",
    "clean up": "打扫",
    "pick up": "捡起/接人"
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
