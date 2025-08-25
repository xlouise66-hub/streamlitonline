import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="高中必修一词组练习", layout="wide")

# ============ 高中必修一词组词汇表（共89个） ============
vocab = {
    "commit oneself to do": "承诺,保证做某事",
    "insist on": "坚决要求",
    "take up position": "担任,任职",
    "wear and tear": "(正常使用造成的)磨损",
    "come to power": "开始掌权",
    "sum up": "总结概括",
    "beyond control": "失控",
    "hang on": "不挂断；稍等；紧握",
    "due to": "由于",
    "lead to": "导致",
    "under construction": "建设中",
    "stand up to": "抵抗；经得起",
    "pass away": "去世；消失",
    "make great contributions to": "对…贡献巨大",
    "switch off/on": "关/开(电器)",
    "daily routine": "日常生活",
    "keep track of": "跟踪",
    "early on": "在初期",
    "prevent...from...": "阻止…做…",
    "catch fire": "着火",
    "in this sense": "从这种意义上",
    "keep in touch (with)": "(与…)保持联系",
    "smart homes": "智能家居",
    "keep us secure": "保障安全",
    "provide a comfortable environment": "提供舒适环境",
    "remote control": "遥控器",
    "advanced technology": "先进技术",
    "automatic control": "自动控制",
    "monitor your health": "监测健康",
    "send a warning": "发送警告",
    "artificial intelligence": "人工智能",
    "driverless cars": "无人驾驶汽车",
    "on the one hand...on the other hand...": "一方面…另一方面…",
    "on the move": "移动中",
    "set out": "出发；开始工作",
    "live off": "依赖…生活",
    "roller coaster": "过山车",
    "theme park": "主题公园",
    "appeal to": "吸引；呼吁",
    "up to": "达到；能胜任",
    "upside down": "颠倒",
    "on the edge of…": "在…边缘",
    "be blessed with…": "享有…",
    "ahead of…": "在…前面",
    "on display/show": "展出",
    "have an appetite for…": "喜欢…",
    "be home to …": "的栖息地",
    "at peace": "处于和平",
    "anything like": "与…相似",
    "by contrast": "相比之下",
    "by comparison": "相比较",
    "make inferences": "推理",
    "break down": "分解；打破",
    "straighten up": "整理；直起身",
    "in other words": "换句话说",
    "call on": "拜访；邀请",
    "at work": "起作用；工作中",
    "vary from culture to culture": "文化差异",
    "make eye contact": "眼神交流",
    "look into one's eyes": "注视眼睛",
    "shake one's head": "摇头",
    "kiss sb. on the cheek": "吻脸颊",
    "get through difficult situations": "摆脱困境",
    "feel down": "沮丧",
    "lean forward": "前倾",
    "have one's head lowered": "低头",
    "devote...to": "致力于…",
    "be comprised of": "由…组成",
    "deep down": "内心深处",
    "in turn": "相应地；轮流",
    "for instance": "例如",
    "work the land": "田间劳作",
    "pursue a career": "追求事业",
    "a serious shortage of food": "食物短缺",
    "tackle this crisis": "解决危机",
    "receive an education": "接受教育",
    "overcome technical difficulties": "克服技术困难",
    "receive numerous awards": "获奖无数",
    "a life of leisure": "悠闲生活",
    "far from the case": "远非如此",
    "care little for celebrity or money": "淡泊名利",
    "make large donations": "捐款支持",
    "fulfil one's dreams": "实现梦想",
    "be rich in nutrition": "营养丰富",
    "switch to organic farming": "转向有机农业",
    "turn to": "转向；求助",
    "focus on": "关注",
    "keep soil rich": "保持土壤肥沃",
    "nowhere near": "远不及"
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
        "He decided to ___ a new job after graduation.",
        "The building is still ___ and cannot be used yet.",
        "We must ___ technical difficulties to succeed.",
        "She promised to ___ the plan as soon as possible.",
        "The teacher asked students to ___ the passage.",
        "He likes to ___ the latest technology trends.",
        "The company will ___ more resources to R&D.",
        "They need to ___ this crisis immediately.",
        "Please ___ your health during the trip.",
        "The scientist tried to ___ the meaning of the data."
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
st.title("🎯 高中必修一词组练习")

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
            selected_label = st.session_state.part2_ans[i][0]  # 用户选项字母
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
