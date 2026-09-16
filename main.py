import streamlit as st
import random
import time

# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="탈출! 거지키우기",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 게임 데이터
# =========================================================

STAGES = [
    {
        "name": "시골 탈출",
        "goal": 1_000_000,
        "background": "🌾",
        "description": "시골에서 벗어나 새로운 삶을 시작하자!"
    },
    {
        "name": "길거리 탈출",
        "goal": 5_000_000,
        "background": "🚶",
        "description": "길거리 생활을 끝내고 다음 단계로!"
    },
    {
        "name": "반지하 탈출",
        "goal": 50_000_000,
        "background": "🏠",
        "description": "반지하를 탈출하고 더 나은 집으로!"
    },
    {
        "name": "1층 탈출",
        "goal": 250_000_000,
        "background": "🏡",
        "description": "1층을 벗어나 더 넓은 세상으로!"
    },
    {
        "name": "지방도시 탈출",
        "goal": 1_250_000_000,
        "background": "🏙️",
        "description": "마지막 목표! 지방도시를 탈출하자!"
    }
]

# =========================================================
# 세션 상태 초기화
# =========================================================

defaults = {
    "money": 0,
    "stage": 0,
    "income_upgrade": 0,
    "click_upgrade": 0,
    "income_price": 1_000,
    "click_price": 1_000,
    "floating_texts": [],
    "cleared": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# 함수
# =========================================================

def format_money(value):
    return f"{value:,}원"


def click_income():
    income_per_click = 1_000 + st.session_state.income_upgrade * 1_000
    click_count = 1 + st.session_state.click_upgrade
    earned = income_per_click * click_count

    st.session_state.money += earned

    st.session_state.floating_texts.append(f"+{earned:,}원")
    if len(st.session_state.floating_texts) > 3:
        st.session_state.floating_texts.pop(0)

    if st.session_state.money >= STAGES[st.session_state.stage]["goal"]:
        st.session_state.cleared = True


def buy_income_upgrade():
    price = st.session_state.income_price

    if st.session_state.money >= price:
        st.session_state.money -= price
        st.session_state.income_upgrade += 1
        st.session_state.income_price = round(price * 1.5)


def buy_click_upgrade():
    price = st.session_state.click_price

    if st.session_state.money >= price:
        st.session_state.money -= price
        st.session_state.click_upgrade += 1
        st.session_state.click_price = round(price * 1.5)


def next_stage():
    if st.session_state.stage < len(STAGES) - 1:
        st.session_state.stage += 1
        st.session_state.cleared = False
        st.session_state.floating_texts = []


# =========================================================
# 현재 스테이지
# =========================================================

current_stage = STAGES[st.session_state.stage]

income_per_click = 1_000 + st.session_state.income_upgrade * 1_000
click_count = 1 + st.session_state.click_upgrade
actual_income = income_per_click * click_count

# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #f5f1e8;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    .game-title {
        text-align: center;
        font-size: 42px;
        font-weight: 900;
        margin-bottom: 5px;
    }

    .stage-title {
        text-align: center;
        font-size: 25px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .money-box {
        background: white;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }

    .money-label {
        font-size: 17px;
        color: #777;
    }

    .money-value {
        font-size: 38px;
        font-weight: 900;
    }

    .game-area {
        border: 5px solid #5b4636;
        border-radius: 25px;
        height: 430px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        overflow: hidden;
        box-shadow: inset 0px -30px 0px rgba(0,0,0,0.04);
    }

    .character {
        font-size: 130px;
        text-align: center;
        filter: drop-shadow(4px 5px 2px rgba(0,0,0,0.25));
        margin-bottom: 5px;
    }

    .character-name {
        background: rgba(255,255,255,0.85);
        padding: 7px 18px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 17px;
    }

    .click-guide {
        margin-top: 12px;
        text-align: center;
        font-size: 18px;
        font-weight: 700;
    }

    .floating {
        text-align: center;
        font-size: 24px;
        font-weight: 900;
        color: #ff9800;
        animation: fade 1.2s ease-out forwards;
    }

    @keyframes fade {
        0% {
            opacity: 1;
            transform: translateY(0px);
        }
        100% {
            opacity: 0;
            transform: translateY(-35px);
        }
    }

    .shop-title {
        text-align: center;
        font-size: 28px;
        font-weight: 900;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    .upgrade-card {
        background: white;
        border-radius: 18px;
        padding: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        min-height: 125px;
    }

    .upgrade-name {
        font-size: 20px;
        font-weight: 900;
    }

    .upgrade-info {
        color: #666;
        margin-top: 5px;
    }

    .goal-box {
        background: #fff8dc;
        border: 2px solid #e3c45c;
        border-radius: 15px;
        padding: 12px;
        text-align: center;
        margin: 10px 0 15px 0;
    }

    .goal-title {
        font-weight: 900;
        font-size: 18px;
    }

    .stButton > button {
        border-radius: 15px;
        font-weight: 800;
        min-height: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 제목
# =========================================================

st.markdown(
    '<div class="game-title">💰 탈출! 거지키우기</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="stage-title">STAGE {st.session_state.stage + 1} · '
    f'{current_stage["name"]}</div>',
    unsafe_allow_html=True
)

# =========================================================
# 돈
# =========================================================

st.markdown(
    f"""
    <div class="money-box">
        <div class="money-label">현재 보유 금액</div>
        <div class="money-value">💰 {format_money(st.session_state.money)}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 목표
# =========================================================

goal = current_stage["goal"]

st.markdown(
    f"""
    <div class="goal-box">
        <div class="goal-title">🎯 목표 금액: {goal:,}원</div>
        <div>{current_stage["description"]}</div>
    </div>
    """,
    unsafe_allow_html=True
)

progress = min(st.session_state.money / goal, 1.0)
st.progress(progress)

# =========================================================
# 스테이지별 배경
# =========================================================

backgrounds = [
    "linear-gradient(to bottom, #d9efff 0%, #eaf7ff 55%, #a8d08d 55%, #8dbb70 100%)",
    "linear-gradient(to bottom, #cfe8ff 0%, #edf6ff 55%, #c9c9c9 55%, #a9a9a9 100%)",
    "linear-gradient(to bottom, #686868 0%, #4f4f4f 55%, #353535 55%, #292929 100%)",
    "linear-gradient(to bottom, #bde2ff 0%, #e9f5ff 55%, #d7c4a8 55%, #c1a783 100%)",
    "linear-gradient(to bottom, #b5ddff 0%, #edf7ff 55%, #b6b6b6 55%, #8d8d8d 100%)"
]

stage_icons = ["🌾", "🚶", "🏠", "🏡", "🏙️"]

st.markdown(
    f"""
    <div class="game-area"
         style="background: {backgrounds[st.session_state.stage]};">
        <div style="font-size:45px;">{stage_icons[st.session_state.stage]}</div>
        <div class="character">🧑‍🦱</div>
        <div class="character-name">돈이 필요한 사람</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="click-guide">👆 아래 버튼을 눌러 돈을 벌어보세요!</div>',
    unsafe_allow_html=True
)

# =========================================================
# 돈 벌기
# =========================================================

if st.button("💰 돈 벌기!", key="earn_button", use_container_width=True):
    click_income()
    st.rerun()

# =========================================================
# +금액 효과
# =========================================================

if st.session_state.floating_texts:
    effects = "".join(
        f'<div class="floating">{text}</div>'
        for text in st.session_state.floating_texts[-3:]
    )
    st.markdown(effects, unsafe_allow_html=True)

# =========================================================
# 스테이지 클리어
# =========================================================

if st.session_state.cleared:
    st.success(
        f"🎉 STAGE {st.session_state.stage + 1} "
        f"'{current_stage['name']}' 클리어!"
    )

    if st.session_state.stage < len(STAGES) - 1:
        if st.button(
            "➡️ 다음 스테이지로",
            key="next_stage",
            use_container_width=True
        ):
            next_stage()
            st.rerun()
    else:
        st.balloons()
        st.success(
            "🏆 모든 스테이지를 클리어했습니다! "
            "당신은 드디어 탈출에 성공했습니다!"
        )

# =========================================================
# 상점
# =========================================================

st.markdown('<div class="shop-title">🛒 상점</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div class="upgrade-card">
            <div class="upgrade-name">💵 클릭 수익 증가</div>
            <div class="upgrade-info">클릭당 수익 +1,000원</div>
            <div class="upgrade-info">현재: {income_per_click:,}원 / 클릭</div>
            <div class="upgrade-info">
                업그레이드 횟수: {st.session_state.income_upgrade}회
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        f"구매하기 · {st.session_state.income_price:,}원",
        key="income_upgrade_button",
        use_container_width=True
    ):
        if st.session_state.money >= st.session_state.income_price:
            buy_income_upgrade()
            st.rerun()
        else:
            st.warning("💸 돈이 부족합니다!")

with col2:
    st.markdown(
        f"""
        <div class="upgrade-card">
            <div class="upgrade-name">👆 클릭 횟수 증가</div>
            <div class="upgrade-info">클릭 1번을 추가 클릭으로 계산</div>
            <div class="upgrade-info">현재: {click_count}회 클릭 취급</div>
            <div class="upgrade-info">
                업그레이드 횟수: {st.session_state.click_upgrade}회
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        f"구매하기 · {st.session_state.click_price:,}원",
        key="click_upgrade_button",
        use_container_width=True
    ):
        if st.session_state.money >= st.session_state.click_price:
            buy_click_upgrade()
            st.rerun()
        else:
            st.warning("💸 돈이 부족합니다!")

# =========================================================
# 현재 능력치
# =========================================================

st.markdown("---")

stat1, stat2, stat3 = st.columns(3)

with stat1:
    st.metric("💰 클릭당 수익", f"{income_per_click:,}원")

with stat2:
    st.metric("👆 클릭 취급 횟수", f"{click_count}회")

with stat3:
    st.metric("💸 실제 클릭 수익", f"{actual_income:,}원")

# =========================================================
# 스테이지 정보
# =========================================================

with st.expander("🗺️ 스테이지 정보"):
    for i, stage in enumerate(STAGES):
        if i < st.session_state.stage:
            status = "✅ 클리어"
        elif i == st.session_state.stage:
            status = "▶️ 현재"
        else:
            status = "🔒 잠김"

        st.write(
            f"**STAGE {i + 1} · {stage['name']}** "
            f"— 목표 {stage['goal']:,}원 — {status}"
        )
