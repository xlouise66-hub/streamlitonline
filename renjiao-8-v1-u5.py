import streamlit as st
import random

st.set_page_config(page_title="U5 英语练习系统", layout="wide")

# ================== U5 词汇表 ==================
vocab = {
    "pepper": "胡椒；辣椒",
    "cut up": "切碎",
    "mix": "混合；搅拌",
    "bake": "烘烤",
    "oven": "烤箱",
    "pour sth into sth": "把……倒入……",
    "flour": "面粉",
    "boil": "煮沸；烧开",
    "butter": "黄油",
    "cheese": "奶酪",
    "cut sth in / into sth": "把……切成……",
    "tablespoon": "汤匙；大勺",
    "mash": "捣碎",
    "mashed potatoes": "土豆泥",
    "stir-fry": "翻炒",
    "do with": "处理；对付",
    "bowl": "碗",
    "heat": "加热；热量",
    "oil": "油",
    "pan": "平底锅；锅子",
    "put sth back": "放回去",
    "mix...with...": "把……和……混合",
    "simple": "简单的",
    "ingredient": "成分；食材",
    "instruction": "说明；指导",
    "steamed fish": "清蒸鱼",
    "hot and sour soup": "酸辣汤",
    "mess": "混乱；凌乱",
    "pretty": "相当；漂亮的",
    "Christmas": "圣诞节",
    "pancake": "薄煎饼",
    "dream": "梦想；梦",
    "university": "大学",
    "go boating": "划船；泛舟",
    "memory": "记忆；回忆",
    "visible": "可见的",
    "along with sb / sth": "连同……；和……一起",
    "pumpkin": "南瓜",
    "pie": "馅饼",
    "warm up": "加热；热身",
    "cinnamon": "肉桂",
    "fill...with...": "把……装满……",
    "sweetness": "甜味；温柔",
    "college": "学院；大学",
    "host": "主人；主持人",
    "hostess": "女主人；女主持人",
    "recipe": "食谱",
    "cream": "奶油",
    "crust": "外壳；硬皮",
    "mixture": "混合物",
    "least": "最少；最小",
    "at least": "至少",
    "secret": "秘密",
    "according to": "根据；按照",
    "whenever": "无论何时",
    "item": "物品；项目",
    "spaghetti": "意大利面",
    "spoon": "勺子",
    "slice": "切片；薄片",
    "couple": "一对；夫妻",
    "island": "岛屿",
    "wife": "妻子",
    "separate": "分开；单独的",
    "born": "出生的",
    "one by one": "一个接一个",
    "Thanksgiving": "感恩节"
}

# ================== 拼写练习题准备 ==================
spelling_exercises = [{"cn": cn, "en": en} for en, cn in vocab.items()]

# ================== 初始化随机题目 ==================
if "initialized" not in st.session_state:
    vocab_items = list(vocab.items())
    vocab_questions = []

    # 词汇选择题（中英互译）40题
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
    st.header("U5 词汇选择题（40题）")
    for i, q in enumerate(st.session_state.vocab_questions, 1):
        st.write(f"Q{i}: {q['question']}")
        st.radio(f"选项Q{i}", q["options"], key=f"vocab_{i}")

# ================== 拼写练习 ==================
elif mode == "拼写练习（中英互译）":
    st.header("U5 拼写练习（15题）")
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
            ans = st.sessio
