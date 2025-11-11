import streamlit as st
import random

st.set_page_config(page_title="U8 英语练习系统", layout="wide")

# ================== U8 词汇表 ==================
vocab = {
    "ring": "戒指；铃声",
    "collection": "收藏；收集品",
    "own": "拥有；自己的",
    "valuable": "贵重的；有价值的",
    "handle": "把手；处理",
    "glove": "手套",
    "add": "添加；增加",
    "envelope": "信封",
    "absolutely": "绝对地；完全地",
    "seem": "似乎；看起来",
    "impossible": "不可能的",
    "single": "单个的；单身的",
    "nail": "钉子；指甲",
    "explain": "解释；说明",
    "bit": "一点；少量",
    "similar": "相似的",
    "coin": "硬币",
    "soft": "柔软的；轻柔的",
    "sticker": "贴纸",
    "waste": "浪费",
    "item": "物品；项目",
    "result": "结果",
    "wrapper": "包装纸",
    "bar": "条；棒；酒吧",
    "include": "包括；包含",
    "size": "尺寸；大小",
    "pattern": "图案；模式",
    "produce": "生产；制造",
    "attract": "吸引",
    "insect": "昆虫",
    "object": "物体；目标",
    "flat": "平的；公寓",
    "language": "语言",
    "treasure": "珍宝；财富",
    "unlock": "打开；解锁",
    "real": "真实的",
    "add to": "增加；添加到",
    "soft drink": "软饮料；汽水",
    "a waste of time": "浪费时间",
    "pocket money": "零花钱",
    "all over the world": "全世界各地"
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
    st.header("U8 词汇选择题（40题）")
    for i, q in enumerate(st.session_state.vocab_questions, 1):
        st.write(f"Q{i}: {q['question']}")
        st.radio(f"选项Q{i}", q["options"], key=f"vocab_{i}")

# ================== 拼写练习 ==================
elif mode == "拼写练习（中英互译）":
    st.header("U8 拼写练习（15题）")
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
