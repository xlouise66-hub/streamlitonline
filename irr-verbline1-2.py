import streamlit as st
import random

# =========================
# 页面设置
# =========================
st.set_page_config(page_title="不规则动词过去式测试", layout="wide")
st.title("📚 不规则动词过去式双向测试（五选一）")

# =========================
# 题库：过去式 + 中文意思
# =========================
word_pairs = {
    "beat": "击打",
    "became": "成为",
    "began": "开始",
    "bit": "咬",
    "blew": "吹",
    "broke": "打破",
    "brought": "带来",
    "built": "建造",
    "bought": "买",
    "caught": "抓住",
    "chose": "选择",
    "came": "来",
    "cost": "花费",
    "cut": "切",
    "did": "做",
    "drew": "画",
    "drank": "喝",
    "drove": "驾驶",
    "ate": "吃",
    "fell": "掉下",
    "felt": "感觉",
    "fought": "战斗",
    "found": "找到",
    "flew": "飞",
    "forgot": "忘记",
    "got": "得到",
    "gave": "给",
    "went": "去",
    "grew": "生长",
    "hung": "悬挂",
    "had": "有",
    "heard": "听到",
    "hid": "隐藏",
    "hit": "击打",
    "held": "握住",
    "hurt": "伤害",
    "kept": "保持",
    "knew": "知道",
    "left": "离开",
    "lent": "借出"
}

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
        eng = [k for k, v in word_pairs.items() if v == meaning][0]
        st.session_state.questions.append({
            "type": "C2E",
            "question": f"'{meaning}' 的英文是什么？",
            "answer": eng
        })

    random.shuffle(st.session_state.questions)

# =========================
# 生成五选一选项，平均分布
# =========================
def insert_correct_answer(distractors, correct):
    # 插入正确答案到五选一随机位置
    opts = distractors.copy()
    pos = random.randint(0, 4)
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
# 用户界面
# =========================
user_answers = {}
with st.form("quiz_form"):
    st.subheader("👉 英译中 & 中译英 测试（40题）")
    for idx, q in enumerate(st.session_state.questions, start=1):
        user_answers[idx] = st.radio(
            f"{idx}. {q['question']}",
            st.session_state.options[idx],
            key=f"q{idx}"
        )
    submitted = st.form_submit_button("✅ 提交答案")

# =========================
# 评分与反馈
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
