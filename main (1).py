import streamlit as st

# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="탈출! 거지키우기",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =========================================================
# 게임 데이터
# =========================================================

STAGES = [
    {"name": "시골 탈출", "goal": 1_000_000, "icon": "🌾",
     "description": "시골에서 벗어나 새로운 삶을 시작하자!"},
    {"name": "길거리 탈출", "goal": 5_000_000, "icon": "🚶",
     "description": "길거리 생활을 끝내고 다음 단계로!"},
    {"name": "반지하 탈출", "goal": 50_000_000, "icon": "🏠",
     "description": "반지하를 탈출하고 더 나은 집으로!"},
    {"name": "1층 탈출", "goal": 250_000_000, "icon": "🏡",
     "description": "1층을 벗어나 더 넓은 세상으로!"},
    {"name": "지방도시 탈출", "goal": 1_250_000_000, "icon": "🏙️",
     "description": "마지막 목표! 지방도시를 탈출하자!"},
]

# =========================================================
# 세션 상태
# =========================================================

defaults = {
    "money": 0,
    "stage": 0,
    "income_upgrade": 0,
    "click_upgrade": 0,
    "income_price": 1_000,
    "click_price": 1_000,
    "last_earned": 0,
    "effect_id": 0,
    "cleared": False,
    "game_finished": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# 함수
# =========================================================

def money_text(value):
    return f"{value:,}원"


def earn_money():
    income = 1_000 + st.session_state.income_upgrade * 1_000
    clicks = 1 + st.session_state.click_upgrade
    earned = income * clicks

    st.session_state.money += earned
    st.session_state.last_earned = earned
    st.session_state.effect_id += 1

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
        st.session_state.last_earned = 0
    else:
        st.session_state.game_finished = True


# =========================================================
# 현재 정보
# =========================================================

stage = STAGES[st.session_state.stage]

income = 1_000 + st.session_state.income_upgrade * 1_000
click_count = 1 + st.session_state.click_upgrade
actual_income = income * click_count

# =========================================================
# 모바일 전용 CSS
# =========================================================

st.markdown(
    """
    <style>
    /* 전체 페이지를 휴대폰 폭에 맞춤 */
    .stApp {
        background: #f4efe5;
    }

    .block-container {
        width: 100%;
        max-width: 430px !important;
        padding: 12px 12px 30px 12px !important;
        margin: 0 auto !important;
    }

    /* Streamlit 기본 상단 여백 축소 */
    header {
        height: 0 !important;
    }

    /* 제목 */
    .game-title {
        text-align: center;
        font-size: 28px;
        font-weight: 900;
        margin: 2px 0 2px 0;
    }

    .stage-title {
        text-align: center;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    /* 돈 */
    .money-box {
        background: white;
        border-radius: 16px;
        padding: 10px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,.08);
    }

    .money-label {
        font-size: 13px;
        color: #777;
    }

    .money-value {
        font-size: 26px;
        font-weight: 900;
    }

    /* 목표 */
    .goal-box {
        background: #fff8dc;
        border: 2px solid #e3c45c;
        border-radius: 13px;
        padding: 9px;
        text-align: center;
        margin: 8px 0;
        font-size: 13px;
    }

    .goal-title {
        font-weight: 900;
        font-size: 15px;
    }

    /* 게임 클릭 영역 */
    div[data-testid="stButton"] > button.game-click {
        height: 350px !important;
    }

    /* 모든 버튼 기본 */
    .stButton > button {
        border-radius: 13px !important;
        font-weight: 800 !important;
        min-height: 46px;
    }

    /* 게임 버튼 */
    .game-button-wrapper .stButton > button {
        min-height: 350px !important;
        height: 350px !important;
        border: 5px solid #5b4636 !important;
        font-size: 65px !important;
        white-space: pre-wrap !important;
        line-height: 1.2 !important;
        box-shadow: inset 0 -80px 0 rgba(0,0,0,.04),
                    0 4px 12px rgba(0,0,0,.15) !important;
    }

    /* 획득 효과 */
    .earned {
        text-align: center;
        height: 32px;
        font-size: 22px;
        font-weight: 900;
        color: #f28c00;
        animation: earned-fade 1s ease-out forwards;
    }

    @keyframes earned-fade {
        0% { opacity: 1; transform: translateY(0); }
        100% { opacity: 0; transform: translateY(-18px); }
    }

    .shop-title {
        text-align: center;
        font-size: 23px;
        font-weight: 900;
        margin: 12px 0 7px;
    }

    .upgrade-card {
        background: white;
        border-radius: 14px;
        padding: 11px;
        min-height: 105px;
        box-shadow: 0 3px 10px rgba(0,0,0,.07);
        font-size: 12px;
    }

    .upgrade-name {
        font-size: 16px;
        font-weight: 900;
    }

    .upgrade-info {
        color: #666;
        margin-top: 3px;
    }

    /* 클리어 오버레이 */
    .clear-overlay {
        position: fixed;
        inset: 0;
        z-index: 999999;
        background: rgba(0,0,0,.72);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }

    .clear-box {
        width: min(390px, 90vw);
        background: white;
        border-radius: 25px;
        padding: 30px 20px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,.35);
    }

    .clear-emoji {
        font-size: 65px;
    }

    .clear-title {
        font-size: 30px;
        font-weight: 900;
        margin: 8px 0;
    }

    .clear-text {
        font-size: 15px;
        color: #555;
        margin-bottom: 15px;
    }

    /* 모바일에서 두 상점 카드를 세로 배치 */
    @media (max-width: 600px) {
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 화면
# =========================================================

st.markdown(
    '<div class="game-title">💰 탈출! 거지키우기</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="stage-title">STAGE {st.session_state.stage + 1} · {stage["name"]}</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="money-box">
        <div class="money-label">현재 보유 금액</div>
        <div class="money-value">💰 {money_text(st.session_state.money)}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="goal-box">
        <div class="goal-title">🎯 목표 {stage["goal"]:,}원</div>
        <div>{stage["description"]}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.progress(min(st.session_state.money / stage["goal"], 1.0))

# =========================================================
# 게임 클릭 영역
# =========================================================
# 상점 이외의 게임 영역 자체를 하나의 큰 버튼으로 사용한다.
# 따라서 캐릭터/배경 부분을 누르는 느낌으로 플레이할 수 있다.

backgrounds = [
    "linear-gradient(to bottom, #d9efff 0%, #eaf7ff 55%, #a8d08d 55%, #8dbb70 100%)",
    "linear-gradient(to bottom, #cfe8ff 0%, #edf6ff 55%, #c9c9c9 55%, #a9a9a9 100%)",
    "linear-gradient(to bottom, #686868 0%, #4f4f4f 55%, #353535 55%, #292929 100%)",
    "linear-gradient(to bottom, #bde2ff 0%, #e9f5ff 55%, #d7c4a8 55%, #c1a783 100%)",
    "linear-gradient(to bottom, #b5ddff 0%, #edf7ff 55%, #b6b6b6 55%, #8d8d8d 100%)",
]

st.markdown('<div class="game-button-wrapper">', unsafe_allow_html=True)

game_label = (
    f'{stage["icon"]}\n\n'
    f'🧑‍🦱\n\n'
    f'👆\n터치해서 돈 벌기\n\n'
    f'+{actual_income:,}원'
)

if not st.session_state.cleared and not st.session_state.game_finished:
    clicked = st.button(
        game_label,
        key="game_click",
        use_container_width=True,
    )

    if clicked:
        earn_money()
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# +금액 효과
# =========================================================

if st.session_state.last_earned > 0:
    st.markdown(
        f'<div class="earned" key="{st.session_state.effect_id}">'
        f'+{st.session_state.last_earned:,}원</div>',
        unsafe_allow_html=True,
    )

# =========================================================
# 스테이지 클리어 전체 화면
# =========================================================

if st.session_state.cleared:
    next_text = (
        "➡️ 다음 스테이지"
        if st.session_state.stage < len(STAGES) - 1
        else "🏆 게임 완료"
    )

    st.markdown(
        f"""
        <div class="clear-overlay">
            <div class="clear-box">
                <div class="clear-emoji">🎉</div>
                <div class="clear-title">STAGE CLEAR!</div>
                <div class="clear-text">
                    {stage["name"]}을(를) 탈출했습니다!<br>
                    <b>{stage["goal"]:,}원</b> 목표 달성!
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 오버레이 위 버튼처럼 보이게 만들기 위해 clear 영역 바로 뒤에 버튼을 배치.
    # 실제 클릭 시 다음 스테이지로 이동하며, 클리어 상태에서는 돈을 더 벌 수 없다.
    if st.button(next_text, key="clear_next", use_container_width=True):
        next_stage()
        st.rerun()

# =========================================================
# 최종 클리어
# =========================================================

if st.session_state.game_finished:
    st.balloons()
    st.success("🏆 모든 스테이지를 클리어했습니다!")

# =========================================================
# 상점
# =========================================================

st.markdown('<div class="shop-title">🛒 상점</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div class="upgrade-card">
            <div class="upgrade-name">💵 수익 증가</div>
            <div class="upgrade-info">클릭당 +1,000원</div>
            <div class="upgrade-info">현재 {income:,}원 / 클릭</div>
            <div class="upgrade-info">Lv.{st.session_state.income_upgrade}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        f"구매 · {st.session_state.income_price:,}원",
        key="income_upgrade",
        use_container_width=True,
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
            <div class="upgrade-info">클릭 1번을 추가 클릭 취급</div>
            <div class="upgrade-info">현재 {click_count}회 취급</div>
            <div class="upgrade-info">Lv.{st.session_state.click_upgrade}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        f"구매 · {st.session_state.click_price:,}원",
        key="click_upgrade",
        use_container_width=True,
    ):
        if st.session_state.money >= st.session_state.click_price:
            buy_click_upgrade()
            st.rerun()
        else:
            st.warning("💸 돈이 부족합니다!")

# =========================================================
# 능력치
# =========================================================

st.markdown("---")

s1, s2, s3 = st.columns(3)

with s1:
    st.metric("💰 클릭 수익", f"{income:,}원")

with s2:
    st.metric("👆 클릭 취급", f"{click_count}회")

with s3:
    st.metric("💸 실제 수익", f"{actual_income:,}원")

# =========================================================
# 스테이지 정보
# =========================================================

with st.expander("🗺️ 스테이지 정보"):
    for i, item in enumerate(STAGES):
        if i < st.session_state.stage:
            status = "✅ 클리어"
        elif i == st.session_state.stage:
            status = "▶️ 현재"
        else:
            status = "🔒 잠김"

        st.write(
            f"**STAGE {i + 1} · {item['name']}** "
            f"— {item['goal']:,}원 — {status}"
        )
