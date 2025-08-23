import streamlit as st
import streamlit.components.v1 as components
import random

# ============ 词汇表 ============
vocab = {
    "guitar": "吉他",
    "honest": "诚实的",
    "patient": "耐心的",
    "improve": "提高",
    "confident": "自信的",
    "courage": "勇气",
    "friendship": "友谊",
    "admiration": "钦佩",
    "respect": "尊重",
    "support": "支持",
    "trust": "信任",
    "survey": "调查",
    "personal": "个人的",
    "quality": "品质",
    "caring": "关心的",
    "describe": "描述",
    "appearance": "外貌",
    "straight": "直的",
    "dark": "黑暗的",
    "same": "相同的",
    "basic": "基本的",
    "thought": "思想",
    "however": "然而",
    "glad": "高兴的",
    "rise": "上升",
    "end": "结束",
    "heart": "心脏",
    "be good at": "擅长",
    "turn to somebody for help": "向某人求助",
    "after school": "放学后",
    "be willing to do something": "愿意做某事",
    "thanks to": "多亏",
    "count on": "依靠",
    "medium height": "中等身高",
    "modern dance": "现代舞",
    "take care of": "照顾",
    "watch over": "看护",
    "rise into": "升入",
    "cry out": "大声喊叫",
    "cry oneself to sleep": "哭着入睡",
    "wake up": "醒来",
    "come and go": "来来去去",
    "take somebody’s place": "取代某人",
    "come along": "一起来"
}

# 句子模板
sentences = [
    "He plays the ______ every weekend.",
    "She is very ______ and never lies.",
    "You need to ______ your English skills.",
    "True ______ is built on trust.",
    "Please ______ your best friend in one sentence.",
    "He is of ______ and wears glasses.",
    "I am ______ to see you today.",
    "They decided to ______ the injured animal.",
    "He showed great ______ when facing danger.",
    "You can always ______ me when you need help."
]

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

# ============ 题目生成函数 ============
def generate_vocab_questions(num=20):
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

def generate_fill_in_questions(num=10):
    selected = random.sample(sentences, num)
    questions = []
    for s in selected:
        correct = random.choice(list(vocab.keys()))
        questions.append({"sentence": s, "answer": correct, "pronounce": correct})
    return questions

# ============ 页面结构 ============
st.title("🎯 词汇练习 + 发音 + 拼写")

mode = st.radio("选择模式：", ["词汇选择题", "句子填空题", "拼写练习（听音写词）"])

# 词汇选择题
if mode == "词汇选择题":
    st.header("📌 词汇选择题（20题）")
    if "vocab_qs" not in st.session_state:
        st.session_state.vocab_qs = generate_vocab_questions(20)
        st.session_state.vocab_ans = [""] * 20

    for i, q in enumerate(st.session_state.vocab_qs):
        st.subheader(f"Question {i+1}: {q['question']}")
        tts_button(q['pronounce'], f"vocab{i}")
        st.session_state.vocab_ans[i] = st.radio(
            "请选择答案：", q["options"], key=f"vocab_{i}"
        )

    if st.button("提交答案"):
        score = sum(1 for i, q in enumerate(st.session_state.vocab_qs) if st.session_state.vocab_ans[i] == q["answer"])
        st.success(f"✅ 你的得分：{score * 5} / 100")
        st.write("正确答案：")
        for i, q in enumerate(st.session_state.vocab_qs):
            st.write(f"{i+1}. {q['question']} ✅ {q['answer']}")

# 句子填空题
elif mode == "句子填空题":
    st.header("📌 句子填空题（10题）")
    if "fill_qs" not in st.session_state:
        st.session_state.fill_qs = generate_fill_in_questions(10)
        st.session_state.fill_ans = [""] * 10

    for i, q in enumerate(st.session_state.fill_qs):
        st.subheader(f"Sentence {i+1}: {q['sentence']}")
        tts_button(q['pronounce'], f"fill{i}")
        st.session_state.fill_ans[i] = st.text_input("填空：", key=f"fill_{i}")

    if st.button("提交答案"):
        score = sum(1 for i, q in enumerate(st.session_state.fill_qs) if st.session_state.fill_ans[i].strip().lower() == q["answer"].lower())
        st.success(f"✅ 你的得分：{score * 10} / 100")
        st.write("正确答案：")
        for i, q in enumerate(st.session_state.fill_qs):
            st.write(f"{i+1}. {q['sentence']} ✅ {q['answer']}")

# 拼写练习模式
else:
    st.header("📌 拼写练习（听音写词）")
    if "spell_qs" not in st.session_state:
        st.session_state.spell_qs = random.sample(list(vocab.keys()), 10)
        st.session_state.spell_ans = [""] * 10

    for i, word in enumerate(st.session_state.spell_qs):
        st.subheader(f"Word {i+1}: 点击按钮听单词，输入拼写")
        tts_button(word, f"spell{i}")
        st.session_state.spell_ans[i] = st.text_input("请输入拼写：", key=f"spell_{i}")

    if st.button("提交答案"):
        score = sum(1 for i, word in enumerate(st.session_state.spell_qs) if st.session_state.spell_ans[i].strip().lower() == word.lower())
        st.success(f"✅ 你的得分：{score * 10} / 100")
        st.write("正确答案：")
        for i, word in enumerate(st.session_state.spell_qs):
            st.write(f"{i+1}. ✅ {word}")
