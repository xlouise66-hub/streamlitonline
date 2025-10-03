import streamlit as st
import random

st.set_page_config(page_title="英语练习系统 - U3词汇", layout="wide")

# ================== U3词汇表 ==================
vocab = {
    # 单词
    "compare": "比较",
    "shy": "害羞的",
    "lazy": "懒惰的",
    "loud": "大声的",
    "outgoing": "外向的",
    "hard-working": "勤奋的",
    "perform": "表演；执行",
    "solve": "解决",
    "flute": "长笛",
    "congratulation": "祝贺",
    "prize": "奖品；奖",
    "attend": "参加；出席",
    "spare": "备用的；多余的",
    "pleasure": "愉快；乐趣",
    "appearance": "外貌；外观",
    "personality": "个性；性格",
    "serious": "认真的；严肃的",
    "strength": "力量；优点",
    "fact": "事实",
    "slim": "苗条的",
    "population": "人口",
    "kilometer": "公里",
    "average": "平均的",
    "rainfall": "降雨量",
    "per": "每；每一",
    "millimeter": "毫米",
    "pleasant": "令人愉快的",
    "alike": "相似的",
    "mirror": "镜子",
    "interest": "兴趣",
    "novel": "小说",
    "difference": "差异；不同",
    "sense": "感觉；意识",
    "humour": "幽默",
    "less": "更少的",
    "straightforward": "直率的；简单的",
    "opinion": "观点；看法",
    "honest": "诚实的",
    "direct": "直接的",
    "similarity": "相似性",
    "friendship": "友谊",
    "metre": "米",
    "prince": "王子",
    "character": "性格；人物",
    "pauper": "穷人",
    "exchange": "交换",
    "accident": "事故",
    "expect": "期望；预计",
    "silver": "银；银色",
    "situation": "情况",
    "touch": "触碰",
    "lend a hand": "帮忙",
    "care about": "关心",
    "reach": "达到；伸手",

    # 短语与表达
    "as ... as ...": "和……一样",
    "besides": "此外；而且",
    "spare time": "空闲时间",
    "have sth in common": "有共同之处",
    "thanks to": "多亏；由于",
    "make a mistake": "犯错误",
    "by accident": "偶然；意外",
    "reach for": "伸手去拿",
    "silver lining": "好的一面"
}

# ================== 拼写练习 ==================
spelling_exercises = [{"cn": cn, "en": en} for en, cn in vocab.items()]

# ================== 初始化随机题目 ==================
if "initialized" not in st.session_state:
    # 词汇选择题 30题（根据词汇数量可适当调整）
    vocab_items = list(vocab.items())
    vocab_questions = []
    for _ in range(min(30, len(vocab_items))):
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
    st.header("词汇选择题（30题）")
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

    total = 30 if mode == "词汇选择题（中英互译）" else 15
    st.success(f"得分：{score} / {total}")

    if wrong:
        st.error("以下是错题：")
        for i, question, user_ans, correct in wrong:
            st.write(f"Q{i}: {question} 你的答案：{user_ans} ✅ 正确答案：{correct}")
