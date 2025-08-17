import streamlit as st
import random

st.set_page_config(page_title="不规则动词词汇测试", layout="wide")
st.title("📚 不规则动词词汇双向测试")

# =========================
# 题库（40题：英译中20，中译英20）
# =========================
word_pairs = {
    "beat": "打败",
    "become": "成为",
    "begin": "开始",
    "bite": "咬",
    "blow": "吹",
    "break": "打破",
    "bring": "带来",
    "build": "建造",
    "buy": "买",
    "catch": "抓住",
    "choose": "选择",
    "come": "来",
    "cost": "花费",
    "cut": "切",
    "do": "做",
    "draw": "画",
    "drink": "喝",
    "drive": "驾驶",
    "eat": "吃",
    "fall": "掉下",
    "feel": "感觉",
    "fight": "战斗",
    "find": "找到",
    "fly": "飞",
    "forget": "忘记",
    "get": "得到",
    "give": "给",
    "go": "去",
    "grow": "生长",
    "hang": "悬挂",
    "have": "有",
    "hear": "听到",
    "hide": "隐藏",
    "hit": "击打",
    "hold": "握住",
    "hurt": "伤害",
    "keep": "保持",
    "know": "知道",
    "leave": "离开",
    "lend": "借出"
}

# 拆分两个列表
english_words = list(word_pairs.keys())
chinese_words = list(word_pairs.values())

# =========================
# 生成题目（避免刷新跳动）
# =========================
if "questions" not in st.session_state:
    # 20 英译中
    eng_to_cn = random.sample(english_words, 20)
    # 20 中译英
    cn_to_eng = random.sample(chinese_words, 20)
    st.session_state.questions = []

    for word in eng_to_cn:
        st.session_state.questions.append({
            "type": "E2C",
            "question": f"What does '{word}' mean?",
            "answer": word_pairs[word]
        })
    for meaning in cn_to_eng:
        # 找到对应英文单词
        eng = [k for k, v in word_pairs.items() if v == meaning][0]
        st.session_state.questions.append({
            "type": "C2E",
            "question": f"'{meaning}' 的英文是什么？",
            "answer": eng
        })

    random.shuffle(st.session_state.questions)

# =========================
# 生成选项
# =========================
def insert_correct_answer(distractors, correct):
    positions = [0, 1, 2, 3, 4]
    weights = [1, 4, 1, 1, 4]  # 偏向B和E
    pos = random.choices(positions, weights=weights, k=1)[0]
    opts = distractors.copy()
    opts.insert(pos, correct)
    return opts

if "options" not in st.session_state:
    st.session_state.options = {}

    for idx, q in enumerate(st.session_state.questions, start=1):
        if q["type"] == "E2C":
            correct = q["answer"]
            distractors = random.sample([x for x in chinese_words if x != correct], 4)
        else:
            correct = q["answer"]
            distractors = random.sample([x for x in english_words if x != correct], 4)
        st.session_state.options[idx] = insert_correct_answer(distractors, correct)

# =========================
# UI 渲染
# =========================
user_answers = {}
with st.form("quiz_form"):
    st.subheader("👉 英译中 & 中译英 测试")
    for idx, q in enumerate(st.session_state.questions, start=1):
        user_answers[idx] = st.radio(
            f"{idx}. {q['question']}",
            st.session_state.options[idx],
            key=f"q{idx}"
        )
    submitted = st.form_submit_button("✅ 提交答案")

# =========================
# 评分
# =========================
if submitted:
    score = 0
    wrong_list = []
    for i, q in enumerate(st.session_state.questions, start=1):
        if user_answers.get(i) == q["answer"]:
            score += 1
        else:
            wrong_list.append(f"{i}. {q['question']} ➜ 正确答案: {q['answer']}")

    total = len(st.session_state.questions)
    percentage = round((score / total) * 100, 2)

    if percentage >= 90:
        level = "🌟 优秀"
    elif percentage >= 75:
        level = "👍 良好"
    elif percentage >= 60:
        level = "🙂 及格"
    else:
        level = "😢 不及格"

    st.success(f"✅ 你的得分是 {score} / {total} ({percentage}%) - {level}")

    if wrong_list:
        st.error("❌ 错题及正确答案：")
        for w in wrong_list:
            st.write(w)

    # 重新开始按钮
    if st.button("🔄 重新开始"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
