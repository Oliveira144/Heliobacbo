import streamlit as st
from collections import Counter
from datetime import datetime

# ========== CONFIGURAÇÃO ==========
st.set_page_config(page_title="HS Bac Bo Tracker", layout="centered", page_icon="🎲")
st.title("🎲 HS Bac Bo Tracker - Visão Estrutural e Inteligente")

# ========== ESTADO INICIAL ==========
if "historico" not in st.session_state:
    st.session_state.historico = []

if "empates" not in st.session_state:
    st.session_state.empates = []

# ========== FUNÇÕES ==========
def adicionar_rodada(player_d1, player_d2, banker_d1, banker_d2):
    p_total = player_d1 + player_d2
    b_total = banker_d1 + banker_d2
    resultado = "Tie" if p_total == b_total else ("Player" if p_total > b_total else "Banker")
    rodada = {
        "player": [player_d1, player_d2],
        "banker": [banker_d1, banker_d2],
        "p_total": p_total,
        "b_total": b_total,
        "resultado": resultado,
        "data": datetime.now()
    }
    st.session_state.historico.append(rodada)
    if resultado == "Tie":
        st.session_state.empates.append(len(st.session_state.historico))

def analisar_empate():
    if len(st.session_state.empates) >= 2:
        espa = [b - a for a, b in zip(st.session_state.empates[:-1], st.session_state.empates[1:])]
        media = sum(espa) / len(espa)
        ultimo = st.session_state.empates[-1]
        rodada_atual = len(st.session_state.historico)
        diff = rodada_atual - ultimo
        if diff >= (media - 2):
            return "🚨 Alta chance de empate nas próximas rodadas!"
    return None

def detectar_88x():
    if not st.session_state.historico:
        return None
    ultimas = st.session_state.historico[-5:]
    for r in ultimas:
        if r["p_total"] == 12 and r["b_total"] == 12:
            return "💥 88x já ocorreu recentemente!"
        if r["p_total"] in [11, 12] and r["b_total"] in [11, 12]:
            return "⚠️ 88x pode estar sendo preparado!"
    return None

def sugerir_entrada():
    if len(st.session_state.historico) < 4:
        return "Aguardando mais dados..."
    ultimos = [r["resultado"] for r in st.session_state.historico[-5:]]
    if ultimos[-3:] == ["Player"] * 3:
        return "🔵 Sugerido: Continuar Player (sequência de 3)"
    elif ultimos[-3:] == ["Banker"] * 3:
        return "🔴 Sugerido: Continuar Banker (sequência de 3)"
    elif ultimos[-2:] == ["Player", "Banker"]:
        return "🎯 Sugerido: Player (quebra de padrão)"
    return "🤔 Nenhum padrão forte detectado"

def analisar_manipulacao():
    if len(st.session_state.historico) < 10:
        return None
    alertas = []
    repetidos = [r["p_total"] + r["b_total"] for r in st.session_state.historico[-10:]]
    contagem = Counter(repetidos)
    for soma, freq in contagem.items():
        if freq >= 3 and soma in [18, 19, 20, 21, 22, 23, 24]:
            alertas.append(f"⚠️ Soma total {soma} apareceu {freq}x. Manipulação estrutural?")
    return alertas

# ========== INTERFACE ==========
st.subheader("🎰 Inserir Rodada Bac Bo (Layout do Jogo)")
c1, c2 = st.columns(2)
with c1:
    st.markdown("### 🎲 Player")
    p_d1 = st.selectbox("Dado 1 (Player)", range(1, 7), key="p1")
    p_d2 = st.selectbox("Dado 2 (Player)", range(1, 7), key="p2")
with c2:
    st.markdown("### 👑 Banker")
    b_d1 = st.selectbox("Dado 1 (Banker)", range(1, 7), key="b1")
    b_d2 = st.selectbox("Dado 2 (Banker)", range(1, 7), key="b2")

if st.button("➕ Registrar rodada"):
    adicionar_rodada(p_d1, p_d2, b_d1, b_d2)
    st.success("Rodada adicionada com sucesso!")

# ========== ANÁLISE ==========
st.divider()
st.subheader("📊 Análise ao Vivo")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Sugestão de Entrada:**")
    st.info(sugerir_entrada())
with col2:
    st.markdown("**Empates / 88x:**")
    empate_msg = analisar_empate()
    x88 = detectar_88x()
    if empate_msg:
        st.warning(empate_msg)
    if x88:
        st.error(x88)

# ========== MANIPULAÇÃO ==========
st.divider()
st.subheader("🧪 Alerta de Manipulação")
alertas = analisar_manipulacao()
if alertas:
    for alerta in alertas:
        st.warning(alerta)
else:
    st.info("Nenhum padrão suspeito detectado nos últimos 10 resultados.")

# ========== HISTÓRICO ==========
st.divider()
st.subheader("📜 Histórico de Rodadas")
for i, r in enumerate(reversed(st.session_state.historico[-30:]), 1):
    st.markdown(f"{i}. 🧑‍🎲 Player: {r['player']} = {r['p_total']} | 👑 Banker: {r['banker']} = {r['b_total']} → Resultado: **{r['resultado']}**")
