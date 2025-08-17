import streamlit as st
import random

st.title("📚 词汇测试（30题）")

# ----------------------------
# 题库（示例30题）
# ----------------------------
questions = [
    # 英译中（15题）
    {"question": "What does 'slow' mean?", "answer": "慢的"},
    {"question": "What does 'hurt' mean?", "answer": "伤害"},
    {"question": "What does 'smell' mean?", "answer": "气味"},
    {"question": "What does 'taste' mean?", "answer": "味道"},
    {"question": "What does 'sound' mean?", "answer": "声音"},
    {"question": "What does 'teenager' mean?", "answer": "青少年"},
    {"question": "What does 'club' mean?", "answer": "俱乐部"},
    {"question": "What does 'prize' mean?", "answer": "奖品"},
    {"question": "What does 'other' mean?", "answer": "其他"},
    {"question": "What does 'comedy' mean?", "answer": "喜剧"},
    {"question": "What does 'adventure' mean?", "answer": "冒险"},
    {"question": "What does 'future' mean?", "answer": "未来"},
    {"question": "What does 'best' mean?", "answer": "最好的"},
    {"question": "What does 'plan' mean?", "answer": "计划"},
    {"question": "What does 'since' mean?", "answer": "自从"},
    # 中译英（15题）
    {"question": "'move' 的意思是？", "answer": "移动"},
    {"question": "'until' 的意思是？", "answer": "直到"},
    {"question": "'join' 的意思是？", "answer": "参加"},
    {"question": "'competition' 的意思是？", "answer": "比赛"},
    {"question": "'sure' 的意思是？", "answer": "肯定的"},
    {"question": "'safe' 的意思是？", "answer": "安全的"},
    {"question": "'prize' 的意思是？", "answer": "奖品"},
    {"question": "'other' 的意思是？", "answer": "其他"},
    {"question": "'best' 的意思是？", "answer": "最好的"},
    {"question": "'future' 的意思是？", "answer": "未来"},
    {"question": "'club' 的意思是？", "answer": "俱乐部"},
    {"question": "'adventure' 的意思是？", "answer": "冒险"},
    {"question": "'comedy' 的意思是？", "answer": "喜剧"},
    {"question": "'teenager' 的意思是？", "answer": "青少年"},
    {"question": "'plan' 的意思是？", "answer": "计划"},
]

# ----------------------------
# 所有可能选项（保证答案出现且均分）
# ----------------------------
all_options = ["慢的","快的","聪明的","安全的","未来","伤害","移动","俱乐部","奖品","计划",
               "气味","味道","声音","青少年","喜剧","冒险","最好的","自从","参加","比赛","肯定的","其他"]

# ----------------------------
# 生成每题随机选项，并保存到 session_state 避免刷新跳动
# ----------------------------
if "options_dict" not in st.session_state:
    st.session_state.options_dict = {}

user_answers = {}

for idx, q in enumerate(questions, start=1):
    if idx not in st.session_state.options_dict:
        opts = [q["answer"]] + random.sample([x for x in all_options if x != q["answer"]], 4)
        random.shuffle(opts)
        st.session_state.options_dict[idx] = opts
    user_answers[idx] = st.radio(f"{idx}. {q['question']}", st.session_state.options_dict[idx], key=str(idx))

# ----------------------------
# 提交答案
# ----------------------------
if st.button("提交答案"):
    score = 0
    wrong_list = []
    for i, q in enumerate(questions, start=1):
        if user_answers.get(i) == q["answer"]:
            score += 1
        else:
            wrong_list.append(f"{i}. {q['question']} ➜ 正确答案: {q['answer']}")
    st.success(f"✅ 你的得分是 {score} / {len(questions)}")
    if wrong_list:
        st.write("❌ 错题及答案：")
        for w in wrong_list:
            st.write(w)
