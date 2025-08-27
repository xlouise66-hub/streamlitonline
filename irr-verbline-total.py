import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="不规则动词练习", layout="wide")

# ============ 不规则动词数据库 ============
vocab_full = {
    "beat": ["beat", "beaten", "击打"],
    "become": ["became", "become", "变成"],
    "begin": ["began", "begun", "开始"],
    "bite": ["bit", "bitten", "咬"],
    "blow": ["blew", "blown", "吹"],
    "break": ["broke", "broken", "打破"],
    "bring": ["brought", "brought", "带来"],
    "build": ["built", "built", "建造"],
    "buy": ["bought", "bought", "买"],
    "catch": ["caught", "caught", "抓住"],
    "choose": ["chose", "chosen", "选择"],
    "come": ["came", "come", "来"],
    "cost": ["cost", "cost", "花费"],
    "cut": ["cut", "cut", "切割"],
    "do": ["did", "done", "做"],
    "draw": ["drew", "drawn", "画"],
    "drink": ["drank", "drunk", "喝"],
    "drive": ["drove", "driven", "驾驶"],
    "eat": ["ate", "eaten", "吃"],
    "fall": ["fell", "fallen", "掉落"],
    "feel": ["felt", "felt", "感觉"],
    "fight": ["fought", "fought", "打架"],
    "find": ["found", "found", "找到"],
    "fly": ["flew", "flown", "飞"],
    "forget": ["forgot", "forgotten", "忘记"],
    "get": ["got", "got", "得到"],
    "give": ["gave", "given", "给予"],
    "go": ["went", "gone", "去"],
    "grow": ["grew", "grown", "生长"],
    "hang": ["hung", "hung", "悬挂"],
    "have": ["had", "had", "有"],
    "hear": ["heard", "heard", "听见"],
    "hide": ["hid", "hidden", "隐藏"],
    "hit": ["hit", "hit", "击打"],
    "hold": ["held", "held", "握住"],
    "hurt": ["hurt", "hurt", "伤害"],
    "keep": ["kept", "kept", "保持"],
    "know": ["knew", "known", "知道"],
    "leave": ["left", "left", "离开"],
    "lend": ["lent", "lent", "借出"],
    "let": ["let", "let", "允许"],
    "lie": ["lay", "lain", "躺"],
    "light": ["lit", "lit", "点亮"],
    "lose": ["lost", "lost", "失去"],
    "make": ["made", "made", "制作"],
    "mean": ["meant", "meant", "意味着"],
    "meet": ["met", "met", "遇见"],
    "pay": ["paid", "paid", "支付"],
    "put": ["put", "put", "放置"],
    "read": ["read", "read", "阅读"],
    "ride": ["rode", "ridden", "骑"],
    "ring": ["rang", "rung", "响铃"],
    "rise": ["rose", "risen", "升起"],
    "run": ["ran", "run", "跑"],
    "say": ["said", "said", "说"],
    "see": ["saw", "seen", "看见"],
    "sell": ["sold", "sold", "卖"],
    "send": ["sent", "sent", "发送"],
    "shine": ["shone", "shone", "发光"],
    "shoot": ["shot", "shot", "射击"],
    "show": ["showed", "shown", "展示"],
    "shut": ["shut", "shut", "关闭"],
    "sing": ["sang", "sung", "唱歌"],
    "sit": ["sat", "sat", "坐"],
    "sleep": ["slept", "slept", "睡觉"],
    "speak": ["spoke", "spoken", "说话"],
    "spend": ["spent", "spent", "花费"],
    "stand": ["stood", "stood", "站立"],
    "steal": ["stole", "stolen", "偷"],
    "swim": ["swam", "swum", "游泳"],
    "take": ["took", "taken", "拿"],
    "teach": ["taught", "taught", "教"],
    "tear": ["tore", "torn", "撕裂"],
    "tell": ["told", "told", "告诉"],
    "think": ["thought", "thought", "思考"],
    "throw": ["threw", "thrown", "扔"],
    "understand": ["understood", "understood", "理解"],
    "wake": ["woke", "woken", "醒来"],
    "wear": ["wore", "worn", "穿"],
    "win": ["won", "won", "赢"],
    "write": ["wrote", "written", "写"]
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

# ============ 生成选择题 ============
def generate_choice_questions(num=30):
    items = list(vocab_full.items())
    questions = []
    for _ in range(num):
        word, forms = random.choice(items)
        meaning = forms[2]
        # 随机决定是中文提示英文选项，还是英文提示中文选项
        if random.choice([True, False]):
            question_text = f"‘{meaning}’ 用英语怎么说？"
            answer = word
            options = [word] + random.sample([w for w in vocab_full.keys() if w != word], 4)
        else:
            question_text = f"What is the meaning of '{word}'?"
            answer = meaning
            options = [meaning] + random.sample([v[2] for k,v in vocab_full.items() if k != word], 4)
        random.shuffle(options)
        questions.append({"question": question_text, "options": options, "answer": answer})
    return questions

# ============ 生成填空题（仅过去式+过去分词） ============
def generate_fill_questions(num=20):
    items = list(vocab_full.items())
    questions = []
    forms_idx = {"过去式":0,"过去分词":1}
    for _ in range(num):
        word, forms = random.choice(items)
        qtype = random.choice(["过去式","过去分词"])
        question_text = f"请写出'{word}'的{qtype}形式"
        answer = forms[forms_idx[qtype]]
        questions.append({"question": question_text, "answer": answer, "pronounce": answer})
    return questions

# ============ 页面结构 ============
st.title("🎯 不规则动词练习系统")

mode = st.radio("选择练习类型：", ["选择题 30题", "填空题 20题"])

# ================= 选择题 =================
if mode == "选择题 30题":
    if "choice_qs" not in st.session_state:
        st.session_state.choice_qs = generate_choice_questions(30)
        st.session_state.choice_ans = [""]*30

    for i, q in enumerate(st.session_state.choice_qs):
        st.subheader(f"Q{i+1}: {q['question']}")
        st.session_state.choice_ans[i] = st.radio("请选择答案：", q["options"], key=f"c_{i}_ans")

    if st.button("提交选择题答案"):
        score = sum(1 for i,q in enumerate(st.session_state.choice_qs) if st.session_state.choice_ans[i]==q["answer"])
        st.success(f"✅ 得分：{score*100/30:.1f} / 100")
        wrong = [(i+1, q['question'], st.session_state.choice_ans[i], q["answer"]) for i,q in enumerate(st.session_state.choice_qs) if st.session_state.choice_ans[i]!=q["answer"]]
        if wrong:
            st.error("❌ 错题回顾：")
            for w in wrong:
                st.write(f"{w[0]}. {w[1]}")
                st.write(f"你的答案：{w[2]} | 正确答案：{w[3]}")

# ================= 填空题（仅过去式和过去分词） =================
else:
    if "fill_qs" not in st.session_state:
        st.session_state.fill_qs = generate_fill_questions(20)
        st.session_state.fill_ans = [""]*20

    for i,q in enumerate(st.session_state.fill_qs):
        st.subheader(f"Q{i+1}: {q['question']}")
        st.session_state.fill_ans[i] = st.text_input("你的答案：", key=f"f_{i}_ans")

    if st.button("提交填空题答案"):
        score = sum(1 for i,q in enumerate(st.session_state.fill_qs) if st.session_state.fill_ans[i].strip().lower()==q["answer"].lower())
        st.success(f"✅ 得分：{score*5} / 100")
        wrong = [(i+1, q['question'], st.session_state.fill_ans[i], q["answer"], q["pronounce"]) for i,q in enumerate(st.session_state.fill_qs) if st.session_state.fill_ans[i].strip().lower()!=q["answer"].lower()]
        if wrong:
            st.error("❌ 错题回顾：")
            for w in wrong:
                st.write(f"{w[0]}. {w[1]}")
                st.write(f"你的答案：{w[2]} | 正确答案：{w[3]}")
                tts_button(w[4], f"wrong_{w[0]}")
