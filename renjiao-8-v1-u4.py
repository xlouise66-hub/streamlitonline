import streamlit as st
import random

st.set_page_config(page_title="英语练习系统 - U4词汇", layout="wide")

# ================== U4词汇表 ==================
vocab = {
    "moss": "苔藓",
    "redwood": "红杉",
    "cheetah": "猎豹",
    "folding": "可折叠的",
    "folding fan": "折扇",
    "bamboo": "竹子",
    "yeah": "是的；好啊",
    "popular": "受欢迎的",
    "goodness": "天哪；善良",
    "tool": "工具",
    "actually": "实际上",
    "shoot": "发射；拍摄；射击",
    "appear": "出现",
    "feel free": "请随意",
    "land": "土地；降落",
    "African": "非洲的；非洲人",
    "rose": "玫瑰",
    "peony": "牡丹",
    "lotus": "莲花",
    "butterfly": "蝴蝶",
    "wing": "翅膀",
    "frog": "青蛙",
    "weigh": "称重；重达",
    "kg": "千克（缩写）",
    "kilogram": "千克",
    "ginkgo": "银杏",
    "province": "省份",
    "take a walk": "散步",
    "connect": "连接",
    "connected": "有关联的；连接的",
    "be connected with / to": "与……相连",
    "without": "没有；不带",
    "imagine": "想象",
    "honey": "蜂蜜；亲爱的",
    "disappointed": "失望的",
    "connection": "联系；连接",
    "pollination": "授粉",
    "pollen": "花粉",
    "action": "行动",
    "in fact": "事实上",
    "per cent": "百分比",
    "for this reason": "出于这个原因",
    "planet": "行星",
    "in order to": "为了……",
    "store": "储存；商店",
    "honeycomb": "蜂巢",
    "communicate": "交流；沟通",
    "play a part": "起作用；扮演角色",
    "ecosystem": "生态系统",
    "protect": "保护",
    "importance": "重要性",
    "title": "标题；头衔",
    "human": "人类的；人",
    "ant": "蚂蚁",
    "be home to sb / sth": "是……的栖息地",
    "happiness": "幸福",
    "disappoint": "使失望",
    "mushroom": "蘑菇",
    "ton": "吨",
    "role": "角色；作用",
    "play a role": "发挥作用",
    "pea": "豌豆",
    "climate": "气候",
    "ocean": "海洋",
    "except": "除了……之外",
    "tiny": "微小的",
    "live up to": "不辜负；符合",
    "likely": "可能的",
    "the Arctic Ocean": "北冰洋"
}

# ================== 拼写练习 ==================
spelling_exercises = [{"cn": cn, "en": en} for en, cn in vocab.items()]

# ================== 初始化随机题目 ==================
if "initialized" not in st.session_state:
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
