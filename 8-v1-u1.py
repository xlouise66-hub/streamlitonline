import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="沪教版八上U1词汇练习", layout="wide")

# ============ 八上U1词汇表 ============ 
vocab = {
    "dinosaur": "恐龙",
    "intelligent": "有才智的；聪明的",
    "talented": "有才能的；天才的",
    "artistic": "有艺术天赋的；（尤指）有美术才能的",
    "perhaps": "可能；大概；也许",
    "notebook": "笔记本",
    "vehicle": "交通工具；车辆",
    "prehistoric": "史前的",
    "completely": "完全地；彻底地",
    "original": "原来的；起初的",
    "birth": "出生",
    "suffering": "苦难；疼痛",
    "artist": "艺术家；（尤指）画家",
    "death": "死；死亡",
    "whole": "全部的；所有的",
    "piece": "一首，一篇（作品）",
    "editor": "（书籍的）编辑",
    "organize": "安排；组织",
    "order": "顺序",
    "record": "记录",
    "general education": "通识教育",
    "go back a long way": "历史悠久",
    "be similar to": "与……相似",
    "alphabetical order": "字母顺序",
    "play an important role": "起到重要作用"
}

# ============ 发音按钮 ============
def tts_button(word, key):
    components.html(f"""
    <button onclick="speak_{key}()">🔊 发音</button>
    <script>
    function speak_{key}() {{
        var msg = new SpeechSynthesisUtterance("{word}");
        msg.lang = 'en-US';
        window.speechSynthesis.speak(msg);
    }}
    </script>
    """, height=40)

# ============ 生成 Part1 词汇选择题 ============
def generate_part1(num=20):
    words = list(vocab.items())
    questions = []
    for _ in range(num):
        word, meaning = random.choice(words)
        if random.choice([True, False]):
            question = f"What is the meaning of '{word}'?"
            answer = meaning
            options = [answer] + random.sample([m for _, m in words if m != meaning], 4)
        else:
            question = f"‘{meaning}’ 用英语怎么说？"
            answer = word
            options = [answer] + random.sample([w for w, _ in words if w != word], 4)
        random.shuffle(options)
        questions.append({"question": question, "options": options, "answer": answer, "pronounce": word})
    return questions

# ============ 生成 Part2 五选一句子填空 ============
def generate_part2(num=20):
    words = list(vocab.items())
    templates = [
        "He decided to ___ a meeting next week.",
        "The book was arranged in ___ on the shelf.",
        "She wants to be an ___ when she grows up.",
        "The company plans to ___ the event tomorrow.",
        "The teacher asked us to keep a ___ of new words.",
        "He bought a new ___ to write his ideas.",
        "Dinosaurs are ___ animals that lived millions of years ago.",
        "He is a very ___ boy with great ideas.",
        "She played an important ___ in the play.",
        "He is a very ___ artist with many talents."
    ]
    questions = []
    for _ in range(num):
        sentence = random.choice(templates)
        correct_word, _ = random.choice(words)
        options = [correct_word] + random.sample([w for w, _ in words if w != correct_word], 4)
        random.shuffle(options)
        labels = ["A", "B", "C", "D", "E"]
        labeled_options = {label: opt for label, opt in zip(labels, options)}
        for label, opt in labeled_options.items():
            if opt == correct_word:
                answer_label = label
                break
        questions.append({"sentence": sentence, "options": labeled_options, "answer": answer_label})
    return questions

# ============ 生成 Part3 听音拼写题 ============
def generate_part3(num=20):
    words = list(vocab.items())
    selected = random.sample(words, num)
    questions = []
    for word, meaning in selected:
        questions.append({"word": word, "meaning": meaning})
    return questions

# ============ 页面结构 ============
st.title("🎯 沪教版八上U1词汇练习")

mode = st.radio("选择练习类型：", ["Part 1 词汇选择题", "Part 2 短文选词填空", "Part 3 听音拼写"])

# ================= Part1 词汇选择题 =================
if mode == "Part 1 词汇选择题":
    st.header("📌 Part 1：词汇选择题（20题）")
    if "part1_qs" not in st.session_state:
        st.session_state.part1_qs = generate_part1(20)
        st.session_state.part1_ans = [""] * 20

    for i, q in enumerate(st.session_state.part1_qs):
        st.subheader(f"Question {i+1}: {q['question']}")
        tts_button(q['pronounce'], f"p1_{i}")
        st.session_state.part1_ans[i] = st.radio("请选择答案：", q["options"], key=f"p1_{i}_ans")

    if st.button("提交答案", key="submit_p1"):
        score = sum(1 for i, q in enumerate(st.session_state.part1_qs) if st.session_state.part1_ans[i] == q["answer"])
        st.success(f"✅ 你的得分：{score * 5} / 100")
        st.write("正确答案：")
        for i, q in enumerate(st.session_state.part1_qs):
            st.write(f"{i+1}. {q['question']} ✅ {q['answer']}")

# ================= Part2 短文选词填空 =================
elif mode == "Part 2 短文选词填空":
    st.header("📌 Part 2：五选一句子填空（20题）")
    if "part2_qs" not in st.session_state:
        st.session_state.part2_qs = generate_part2(20)
        st.session_state.part2_ans = [""] * 20

    for i, q in enumerate(st.session_state.part2_qs):
        st.subheader(f"Sentence {i+1}: {q['sentence']}")
        options_display = [f"{label}. {word}" for label, word in q["options"].items()]
        st.session_state.part2_ans[i] = st.radio("请选择答案：", options_display, key=f"p2_{i}_ans")

    if st.button("提交答案", key="submit_p2"):
        score = 0
        wrong = []
        for i, q in enumerate(st.session_state.part2_qs):
            selected_label = st.session_state.part2_ans[i][0]
            if selected_label == q["answer"]:
                score += 1
            else:
                wrong.append((q['sentence'], st.session_state.part2_ans[i], q['options'][q['answer']]))
        st.success(f"✅ 你的得分：{score}/{len(st.session_state.part2_qs)}")
        if wrong:
            st.error("❌ 错题回顾：")
            for idx, (ques, ans, correct) in enumerate(wrong, 1):
                st.write(f"{idx}. {ques}")
                st.write(f"你的答案：{ans} | 正确答案：{correct}")

# ================= Part3 听音拼写 =================
else:
    st.header("📌 Part 3：听音拼写（20题）")
    if "part3_qs" not in st.session_state:
        st.session_state.part3_qs = generate_part3(20)
        st.session_state.part3_ans = [""] * 20

    for i, q in enumerate(st.session_state.part3_qs):
        st.subheader(f"Word {i+1}: {q['meaning']}")
        tts_button(q['word'], f"p3_{i}")
        st.session_state.part3_ans[i] = st.text_input("请输入拼写：", key=f"p3_{i}_ans")

    if st.button("提交答案", key="submit_p3"):
        score = 0
        wrong = []
        for i, q in enumerate(st.session_state.part3_qs):
            if st.session_state.part3_ans[i].strip().lower() == q["word"].lower():
                score += 1
            else:
                wrong.append((q['meaning'], st.session_state.part3_ans[i], q["word"]))
        st.success(f"✅ 你的得分：{score}/{len(st.session_state.part3_qs)}")
        if wrong:
            st.error("❌ 错题回顾：")
            for idx, (meaning, ans, correct) in enumerate(wrong, 1):
                st.write(f"{idx}. {meaning}")
                st.write(f"你的答案：{ans} | 正确答案：{correct}")
