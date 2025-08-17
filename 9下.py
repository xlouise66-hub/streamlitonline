import streamlit as st
import random

st.set_page_config(page_title="词汇测试80题", layout="wide")
st.title("📚 六单元词汇双向测试（80题）")

# =========================
# 词汇题库（英-中）
# =========================
word_pairs = {
    # U1
    "voyage": "航行",
    "repetition": "重复",
    "American": "美国的",
    "continent": "大陆",
    "route": "路线",
    "discovery": "发现",
    "rise": "上升",
    "official": "官方的",
    "develop": "发展",
    "relation": "关系",
    "trade": "贸易",
    "foreign": "外国的",
    "fleet": "舰队",
    "Africa": "非洲",
    "nowhere": "无处",
    "silk": "丝绸",
    "giraffe": "长颈鹿",
    "besides": "此外",
    "development": "发展",
    "region": "地区",
    "pioneer": "先驱",
    "people": "人们",
    "wealth": "财富",
    "spread": "传播",
    "open up": "开放",
    "go on a trip": "去旅行",
    "set up": "建立",
    "set sail": "启航",
    "known as": "被称为",
    "as well as": "以及",
    "lead to": "导致",
    "compare with": "与……比较",
    # U2
    "culture shock": "文化冲击",
    "camp": "营地",
    "firework": "烟花",
    "turkey": "火鸡",
    "international": "国际的",
    "admit": "承认",
    "spare": "空闲的",
    "degree": "程度",
    "fail": "失败",
    "manage": "管理",
    "idiom": "习语",
    "everyday": "日常的",
    "uniform": "制服",
    "whatever": "无论什么",
    "pink": "粉红色",
    "purple": "紫色",
    "anyway": "无论如何",
    "especially": "特别地",
    "baseball": "棒球",
    "education": "教育",
    "state": "州",
    "national": "国家的",
    "president": "总统",
    "vacation": "假期",
    "schedule": "日程表",
    "set off": "出发",
    "take off": "起飞",
    "in one's spare time": "在空闲时间",
    "to a certain degree": "在某种程度上",
    "get used to": "习惯于",
    "under the weather": "身体不适",
    # U3
    "concern": "担忧",
    "atmosphere": "大气",
    "temperature": "温度",
    "consumer": "消费者",
    "guess": "猜测",
    "green": "绿色",
    "lifeless": "无生命的",
    "fuel": "燃料",
    "coal": "煤",
    "result": "结果",
    "increase": "增加",
    "sea level": "海平面",
    "destroy": "毁灭",
    "nature": "自然",
    "surface": "表面",
    "soil": "土壤",
    "flood": "洪水",
    "habit": "习惯",
    "proper": "适当的",
    "friendly": "友好的",
    "recycle": "回收",
    "purpose": "目的",
    "solution": "解决方案",
    "government": "政府",
    "role model": "榜样",
    "greenhouse effect": "温室效应",
    "in danger": "处于危险中",
    "as a result of": "由于",
    "take action": "采取行动",
    "make a difference": "有影响",
    "act as": "充当",
    # U4
    "asteroid": "小行星",
    "typhoon": "台风",
    "earthquake": "地震",
    "melt": "融化",
    "flood": "洪水",
    "badly": "严重地",
    "alive": "活着的",
    "pool": "水池",
    "object": "物体",
    "coach": "教练",
    "pass": "通过",
    "line": "线",
    "dead": "死的",
    "boss": "老板",
    "deaf": "聋的",
    "stare": "盯",
    "screen": "屏幕",
    "notice": "注意",
    "awake": "醒着的",
    "immediately": "立即",
    "missing": "失踪的",
    "fellow": "同伴",
    "natural disaster": "自然灾害",
    "pass by": "路过",
    "stick with": "坚持",
    "sit around": "闲坐",
    "have no time to do": "没有时间做",
    "fall on deaf ears": "充耳不闻",
    "stare at": "盯着",
    "in surprise": "惊讶地",
    "for now": "暂时",
    "survival kit": "生存装备",
    # U5
    "announcement": "公告",
    "passport": "护照",
    "the Pacific": "太平洋",
    "Canada": "加拿大",
    "resort": "度假胜地",
    "Canadian": "加拿大人",
    "slope": "斜坡",
    "opposite": "相反的",
    "glove": "手套",
    "couple": "夫妻",
    "gentle": "温和的",
    "honest": "诚实的",
    "rope": "绳子",
    "rapid": "快速的",
    "over": "在……之上",
    "shame": "羞愧",
    "fee": "费用",
    "enter": "进入",
    "semi-final": "半决赛",
    "final": "决赛",
    "badminton": "羽毛球",
    "stress": "压力",
    "be dying to": "渴望",
    "check in": "登记入住",
    "can't wait to do": "迫不及待做",
    "to be honest": "老实说",
    "fall over": "摔倒",
    "keep one's balance": "保持平衡",
    "build up": "积累",
    # U6
    "conduct": "行为",
    "lifestyle": "生活方式",
    "quarrel": "争吵",
    "focus": "集中",
    "peer": "同龄人",
    "pressure": "压力",
    "whether": "是否",
    "risk": "风险",
    "guard": "守卫",
    "positive": "积极的",
    "cancel": "取消",
    "bright": "明亮的",
    "force": "强迫",
    "concert": "音乐会",
    "private": "私人的",
    "silent": "安静的",
    "musical instrument": "乐器",
    "enemy": "敌人",
    "regular": "规律的",
    "cheer": "欢呼",
    "low": "低的",
    "eyesight": "视力",
    "dentist": "牙医",
    "recovery": "恢复",
    "deal with": "处理",
    "guard against": "防范",
    "cancel out": "抵消",
    "look on the bright side": "往好处想",
    "take up": "开始从事",
    "busy with": "忙于",
    "leave behind": "留下",
    "cheer up": "振作"
}

english_words = list(word_pairs.keys())
chinese_words = list(word_pairs.values())

# =========================
# 生成80题（40英译中 + 40中译英）
# =========================
if "questions" not in st.session_state:
    eng_to_cn = random.sample(english_words, 40)
    cn_to_eng = random.sample(chinese_words, 40)
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
    st.subheader("👉 英译中 & 中译英 测试（共80题）")
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
