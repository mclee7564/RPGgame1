import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="탈출 키우기",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family: Arial, "Noto Sans KR", sans-serif;
    background: #f3efe7;
}

body {
    display: flex;
    justify-content: center;
    align-items: center;
}

#game {
    width: min(100vw, 430px);
    height: 100dvh;
    max-height: 100dvh;
    position: relative;
    overflow: hidden;
    background: #d9c29c;
}

/* ---------- 배경 ---------- */
.stage1 {
    background:
        linear-gradient(to bottom, rgba(255,255,255,.12), rgba(0,0,0,.05)),
        linear-gradient(to bottom, #8ed0ff 0 48%, #8bc36b 48% 72%, #d6b277 72% 100%);
}
.stage2 {
    background:
        linear-gradient(to bottom, #b9ddff 0 42%, #777 42% 74%, #444 74% 100%);
}
.stage3 {
    background:
        linear-gradient(to bottom, #696969 0 55%, #393939 55% 100%);
}
.stage4 {
    background:
        linear-gradient(to bottom, #b9dfff 0 43%, #d9d9d9 43% 100%);
}
.stage5 {
    background:
        linear-gradient(to bottom, #8cc8f5 0 48%, #c4c4c4 48% 100%);
}

.game-area {
    position: absolute;
    inset: 0;
    cursor: pointer;
    user-select: none;
    touch-action: manipulation;
}

/* 배경 장식 */
.sun {
    position: absolute;
    width: 65px;
    height: 65px;
    border-radius: 50%;
    background: #ffe477;
    top: 75px;
    right: 28px;
    opacity: .9;
}

.cloud {
    position: absolute;
    font-size: 46px;
    opacity: .75;
}

.house {
    position: absolute;
    bottom: 25%;
    left: 12%;
    font-size: 95px;
}

.tree {
    position: absolute;
    bottom: 24%;
    right: 8%;
    font-size: 90px;
}

.car {
    position: absolute;
    bottom: 23%;
    right: 15%;
    font-size: 65px;
}

.door {
    position: absolute;
    bottom: 25%;
    left: 50%;
    transform: translateX(-50%);
    font-size: 120px;
}

.building {
    position: absolute;
    bottom: 21%;
    left: 50%;
    transform: translateX(-50%);
    font-size: 190px;
}

.street-line {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 24%;
    border-top: 5px dashed rgba(255,255,255,.55);
}

/* ---------- 상단 UI ---------- */
.top-ui {
    position: absolute;
    top: 10px;
    left: 10px;
    right: 10px;
    z-index: 20;
    pointer-events: none;
}

.stage-name {
    display: inline-block;
    background: rgba(255,255,255,.9);
    border-radius: 14px;
    padding: 7px 11px;
    font-size: 14px;
    font-weight: 800;
    box-shadow: 0 2px 8px rgba(0,0,0,.12);
}

.money {
    margin-top: 7px;
    display: inline-block;
    background: rgba(255,255,255,.94);
    border-radius: 14px;
    padding: 8px 12px;
    font-size: 19px;
    font-weight: 900;
    box-shadow: 0 2px 8px rgba(0,0,0,.12);
}

.progress-wrap {
    margin-top: 7px;
    width: 100%;
    height: 13px;
    border-radius: 10px;
    background: rgba(255,255,255,.65);
    overflow: hidden;
    box-shadow: inset 0 1px 3px rgba(0,0,0,.15);
}

.progress {
    height: 100%;
    width: 0%;
    background: #ffca3a;
    border-radius: 10px;
    transition: width .15s;
}

/* ---------- 상점 ---------- */
.shop-open {
    position: absolute;
    top: 10px;
    left: 10px;
    z-index: 30;
    margin-top: 118px;
    border: 0;
    border-radius: 14px;
    padding: 9px 13px;
    background: #ffffff;
    box-shadow: 0 3px 10px rgba(0,0,0,.18);
    font-size: 15px;
    font-weight: 900;
    cursor: pointer;
    touch-action: manipulation;
}

.shop-overlay {
    display: none;
    position: absolute;
    inset: 0;
    z-index: 100;
    background: rgba(0,0,0,.55);
    align-items: center;
    justify-content: center;
    padding: 18px;
}

.shop-panel {
    width: 100%;
    max-width: 370px;
    background: #fffdf8;
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0 10px 35px rgba(0,0,0,.28);
}

.shop-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 13px;
}

.shop-title {
    font-size: 24px;
    font-weight: 900;
}

.close-shop {
    border: 0;
    background: #eeeeee;
    border-radius: 12px;
    padding: 8px 12px;
    font-weight: 800;
    cursor: pointer;
}

.upgrade {
    width: 100%;
    border: 0;
    border-radius: 16px;
    background: #f1eadc;
    padding: 14px;
    margin-top: 10px;
    text-align: left;
    cursor: pointer;
}

.upgrade:active {
    transform: scale(.98);
}

.upgrade-title {
    font-size: 16px;
    font-weight: 900;
}

.upgrade-info {
    margin-top: 5px;
    font-size: 13px;
    color: #555;
}

.upgrade-price {
    margin-top: 8px;
    font-size: 15px;
    font-weight: 900;
}

.upgrade.disabled {
    opacity: .45;
    cursor: not-allowed;
}

/* ---------- 클릭 효과 ---------- */
.float-money {
    position: absolute;
    z-index: 50;
    pointer-events: none;
    font-size: 21px;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 2px 4px rgba(0,0,0,.6);
    animation: floatUp .7s ease-out forwards;
}

@keyframes floatUp {
    0% {
        transform: translateY(0) scale(1);
        opacity: 1;
    }
    100% {
        transform: translateY(-75px) scale(1.12);
        opacity: 0;
    }
}

.tap-guide {
    position: absolute;
    left: 50%;
    bottom: 8%;
    transform: translateX(-50%);
    z-index: 10;
    background: rgba(0,0,0,.4);
    color: white;
    padding: 8px 14px;
    border-radius: 20px;
    font-size: 13px;
    pointer-events: none;
}

/* ---------- 클리어 ---------- */
.clear-overlay {
    display: none;
    position: absolute;
    inset: 0;
    z-index: 200;
    background: rgba(0,0,0,.72);
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 25px;
}

.clear-box {
    width: 100%;
    max-width: 350px;
    background: #fffdf8;
    border-radius: 24px;
    padding: 28px 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,.35);
}

.clear-title {
    font-size: 31px;
    font-weight: 1000;
    margin-bottom: 8px;
}

.clear-desc {
    font-size: 15px;
    color: #555;
    line-height: 1.5;
    margin-bottom: 18px;
}

.next-stage {
    width: 100%;
    border: 0;
    border-radius: 15px;
    background: #ffca3a;
    padding: 13px;
    font-size: 17px;
    font-weight: 900;
    cursor: pointer;
}

.final {
    background: #ffca3a;
}
</style>
</head>

<body>
<div id="game">

    <div id="gameArea" class="game-area">
        <div class="sun"></div>
        <div class="cloud" style="top:80px;left:35px;">☁️</div>
        <div class="cloud" style="top:145px;left:190px;font-size:35px;">☁️</div>
        <div id="decor"></div>
        <div class="tap-guide">화면을 터치해서 돈을 벌어보세요!</div>
    </div>

    <div class="top-ui">
        <div id="stageName" class="stage-name"></div><br>
        <div id="money" class="money">💰 ₩1,000</div>
        <div class="progress-wrap">
            <div id="progress" class="progress"></div>
        </div>
    </div>

    <button id="shopOpen" class="shop-open">🛒 상점</button>

    <div id="shopOverlay" class="shop-overlay">
        <div class="shop-panel">
            <div class="shop-header">
                <div class="shop-title">🛒 상점</div>
                <button id="shopClose" class="close-shop">닫기 ✕</button>
            </div>

            <button id="incomeUpgrade" class="upgrade">
                <div class="upgrade-title">💵 클릭 수익 증가</div>
                <div class="upgrade-info" id="incomeInfo">클릭할 때마다 +₩1,000</div>
                <div class="upgrade-price" id="incomePrice">구매: ₩1,000</div>
            </button>

            <button id="countUpgrade" class="upgrade">
                <div class="upgrade-title">👆 클릭 횟수 증가</div>
                <div class="upgrade-info" id="countInfo">한 번 터치하면 1번 클릭</div>
                <div class="upgrade-price" id="countPrice">구매: ₩1,000</div>
            </button>
        </div>
    </div>

    <div id="clearOverlay" class="clear-overlay">
        <div class="clear-box">
            <div id="clearTitle" class="clear-title">🎉 스테이지 클리어!</div>
            <div id="clearDesc" class="clear-desc"></div>
            <button id="nextStage" class="next-stage">다음 스테이지로 ➜</button>
        </div>
    </div>
</div>

<script>
const stages = [
    { name: "1단계 · 시골 탈출", goal: 1000000, className: "stage1" },
    { name: "2단계 · 길거리 탈출", goal: 5000000, className: "stage2" },
    { name: "3단계 · 반지하 탈출", goal: 50000000, className: "stage3" },
    { name: "4단계 · 1층 탈출", goal: 250000000, className: "stage4" },
    { name: "5단계 · 지방도시 탈출", goal: 1250000000, className: "stage5" }
];

let stage = 0;
let money = 0;
let incomeLevel = 0;
let countLevel = 0;
let incomePrice = 1000;
let countPrice = 1000;
let cleared = false;
let shopOpen = false;

const game = document.getElementById("game");
const gameArea = document.getElementById("gameArea");
const moneyEl = document.getElementById("money");
const stageNameEl = document.getElementById("stageName");
const progressEl = document.getElementById("progress");
const decor = document.getElementById("decor");
const shopOverlay = document.getElementById("shopOverlay");
const clearOverlay = document.getElementById("clearOverlay");

function wonPerClick() {
    return (1000 + incomeLevel * 1000) * (1 + countLevel);
}

function formatWon(n) {
    return "₩" + Math.floor(n).toLocaleString("ko-KR");
}

function renderDecor() {
    const d = [
        '<div class="house">🏠</div><div class="tree">🌳</div>',
        '<div class="car">🚗</div><div class="street-line"></div>',
        '<div class="door">🚪</div>',
        '<div class="house">🏢</div><div class="door">🚪</div>',
        '<div class="building">🏙️</div>'
    ];
    decor.innerHTML = d[stage];
}

function updateUI() {
    const s = stages[stage];

    game.className = "";
    game.classList.add(s.className);

    stageNameEl.textContent = s.name;
    moneyEl.textContent = "💰 " + formatWon(money) + " / " + formatWon(s.goal);

    const percent = Math.min(100, (money / s.goal) * 100);
    progressEl.style.width = percent + "%";

    document.getElementById("incomeInfo").textContent =
        "현재 클릭 수익: " + formatWon(1000 + incomeLevel * 1000) + " × " + (1 + countLevel);

    document.getElementById("incomePrice").textContent =
        "구매: " + formatWon(incomePrice);

    document.getElementById("countInfo").textContent =
        "한 번 터치하면 " + (1 + countLevel) + "번 클릭";

    document.getElementById("countPrice").textContent =
        "구매: " + formatWon(countPrice);

    document.getElementById("incomeUpgrade").classList.toggle("disabled", money < incomePrice);
    document.getElementById("countUpgrade").classList.toggle("disabled", money < countPrice);

    renderDecor();
}

function playClickSound() {
    try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!AudioContext) return;

        if (!window.audioCtx) window.audioCtx = new AudioContext();
        const ctx = window.audioCtx;

        if (ctx.state === "suspended") ctx.resume();

        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = "sine";
        osc.frequency.setValueAtTime(520, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(720, ctx.currentTime + 0.06);

        gain.gain.setValueAtTime(0.0001, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.08, ctx.currentTime + 0.01);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.09);

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.start();
        osc.stop(ctx.currentTime + 0.1);
    } catch (e) {}
}

function showFloatingMoney(amount, x, y) {
    const el = document.createElement("div");
    el.className = "float-money";
    el.textContent = "+" + formatWon(amount);

    const rect = game.getBoundingClientRect();
    el.style.left = Math.max(10, Math.min(rect.width - 100, x - rect.left - 30)) + "px";
    el.style.top = Math.max(130, Math.min(rect.height - 80, y - rect.top - 15)) + "px";

    game.appendChild(el);

    setTimeout(() => el.remove(), 750);
}

function checkClear() {
    if (money >= stages[stage].goal && !cleared) {
        cleared = true;
        clearOverlay.style.display = "flex";

        if (stage === stages.length - 1) {
            document.getElementById("clearTitle").textContent = "🏆 모든 스테이지 클리어!";
            document.getElementById("clearDesc").textContent =
                "축하합니다! 모든 탈출에 성공했습니다.";
            document.getElementById("nextStage").textContent = "새 게임 시작 🔄";
            document.getElementById("nextStage").classList.add("final");
        } else {
            document.getElementById("clearTitle").textContent = "🎉 스테이지 클리어!";
            document.getElementById("clearDesc").textContent =
                "목표 금액을 달성했습니다! 다음 탈출을 시작해보세요.";
            document.getElementById("nextStage").textContent = "다음 스테이지로 ➜";
        }
    }
}

gameArea.addEventListener("click", (e) => {
    if (cleared || shopOpen) return;

    const earned = wonPerClick();
    money += earned;

    playClickSound();
    showFloatingMoney(earned, e.clientX, e.clientY);
    updateUI();
    checkClear();
});

document.getElementById("shopOpen").addEventListener("click", (e) => {
    e.stopPropagation();
    shopOpen = true;
    shopOverlay.style.display = "flex";
});

document.getElementById("shopClose").addEventListener("click", (e) => {
    e.stopPropagation();
    shopOpen = false;
    shopOverlay.style.display = "none";
});

document.getElementById("incomeUpgrade").addEventListener("click", (e) => {
    e.stopPropagation();
    if (money >= incomePrice) {
        money -= incomePrice;
        incomeLevel++;
        incomePrice = Math.round(incomePrice * 1.5);
        updateUI();
    }
});

document.getElementById("countUpgrade").addEventListener("click", (e) => {
    e.stopPropagation();
    if (money >= countPrice) {
        money -= countPrice;
        countLevel++;
        countPrice = Math.round(countPrice * 1.5);
        updateUI();
    }
});

document.getElementById("nextStage").addEventListener("click", (e) => {
    e.stopPropagation();

    if (stage === stages.length - 1) {
        stage = 0;
        money = 0;
        incomeLevel = 0;
        countLevel = 0;
        incomePrice = 1000;
        countPrice = 1000;
    } else {
        stage++;
    }

    cleared = false;
    clearOverlay.style.display = "none";
    updateUI();
});

updateUI();
</script>
</body>
</html>
"""

components.html(game_html, height=700, scrolling=False)
