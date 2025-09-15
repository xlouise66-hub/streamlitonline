import streamlit as st
import random

st.set_page_config(page_title="英语练习系统 - Unit 2", layout="wide")

# ================== 词汇表 ==================
vocab = {
    "pack": "打包",
    "pack up": "收拾行李；打包",
    "bathroom": "浴室；洗手间",
    "sort": "种类；分类",
    "bedroom": "卧室",
    "balcony": "阳台",
    "hang up": "挂起；挂断电话",
    "invite": "邀请",
    "living room": "客厅",
    "arrival": "到达",
    "yet": "尚；还；已经",
    "add": "增加；添加",
    "add sth to sth": "把某物添加到某物中",
    "go shopping": "去购物",
    "biscuit": "饼干",
    "borrow": "借入",
    "plan": "计划",
    "treasure": "财富；珍宝",
    "hunt": "寻找；打猎",
    "treasure hunt": "寻宝游戏",
    "lift": "电梯；举起",
    "give sb. a lift": "让某人搭便车",
    "until": "直到……为止",
    "be careful with": "小心对待",
    "movie": "电影",
    "the movies": "电影院",
    "dead": "死的；无生命的",
    "note": "笔记；便条",
    "take notes": "做笔记",
    "clean up": "打扫干净",
    "community": "社区",
    "rubbish": "垃圾",
    "almost": "几乎；差不多",
    "journey": "旅行",
    "pull": "拉；拖",
    "luggage": "行李",
    "share sth with sb": "与某人分享某物",
    "familiar": "熟悉的",
    "joke": "笑话",
    "several": "几个；数个",
    "nod": "点头",
    "writer": "作家",
    "text": "文本；短信",
    "describe": "描述",
    "wherever": "无论在哪里",
    "matter": "要紧；事情",
    "no matter": "不论；无论",
    "perhaps": "可能；也许",
    "plate": "盘子",
    "freshly": "新鲜地",
    "smell": "闻；气味",
    "joy": "快乐；喜悦",
    "apartment": "公寓",
    "block": "街区；大楼",
    "decorate": "装饰",
    "cover": "覆盖",
    "poster": "海报",
    "scissors": "剪刀",
    "glue": "胶水",
    "paper cutting": "剪纸",
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
