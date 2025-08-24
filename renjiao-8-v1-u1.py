import streamlit as st
import streamlit.components.v1 as components
import random

# ============ 词汇表（已更新） ============
vocab = {
    "ancient": "古老的",
    "camp": "营地",
    "landscape": "风景",
    "strange": "奇怪的",
    "vacation": "假期",
    "fantastic": "极好的",
    "town": "城镇",
    "breath": "呼吸",
    "take sb’s breath away": "令人惊叹",
    "especially": "尤其",
    "steamed chicken soup": "清炖鸡汤",
    "anywhere": "任何地方",
    "nothing": "没有东西",
    "scenery": "景色",
    "silk": "丝绸",
    "scarf": "围巾",
    "nothing but": "只不过",
    "hotel": "酒店",
    "comfortable": "舒服的",
    "ready": "准备好的",
    "ready to do sth.": "准备做某事",
    "somewhere": "某个地方",
    "sky": "天空",
    "bored": "无聊的",
    "stand up": "站起来",
    "towards": "朝向",
    "rainbow": "彩虹",
    "square": "广场",
    "during": "在……期间",
    "victory": "胜利",
    "Russian": "俄罗斯的",
    "fight": "战斗",
    "against": "反对",
    "fight against sb / sth.": "与某人/某事作斗争",
    "guide": "导游",
    "artwork": "艺术品",
    "thousands of": "成千上万",
    "tear": "眼泪",
    "remind": "提醒",
    "peace": "和平",
    "easily": "容易地",
    "forget": "忘记",
    "noon": "中午",
    "sick": "生病的",
    "station": "车站",
    "palace": "宫殿",
    "accordion": "手风琴",
    "get together": "聚会",
    "in the sun": "在阳光下",
    "tower": "塔",
    "might": "可能",
    "budget": "预算",
    "passport": "护照",
    "forgetful": "健忘的",
    "faraway": "遥远的",
    "regular": "常规的",
    "countryside": "乡村",
    "turn around": "转身",
    "surprised": "惊讶的",
    "deer": "鹿",
    "probably": "大概",
    "look for": "寻找"
}

# 句子模板（保持通用）
sentences = [
    "The ______ temple is full of history.",
    "We stayed in a ______ during our trip.",
    "He was ______ when he saw the rainbow.",
    "I need a ______ to travel abroad.",
    "They are going to ______ in the countryside.",
    "The ______ was very beautiful after the rain.",
    "She bought a silk ______ in the shop.",
    "Don’t forget to take your ______ before leaving.",
    "He was ______ because he had nothing to do.",
    "This guide will ______ you of the trip schedule."
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
st.title("🎯 人教版8上词汇练习 + 发音 + 拼写")

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
