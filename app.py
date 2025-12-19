import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from datetime import datetime

# --- CONFIGURAÇÃO DE AMBIENTE MASTER ---
st.set_page_config(page_title="ORACLE MASTER V9", layout="wide", initial_sidebar_state="expanded")

def init_db():
    with sqlite3.connect('oracle_master.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users 
                     (username TEXT PRIMARY KEY, password TEXT, role TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS logs 
                     (id INTEGER PRIMARY KEY, data TEXT, esporte TEXT, time_a TEXT, time_b TEXT, 
                     prob_a REAL, prob_e REAL, prob_b REAL, resultado_real TEXT)''')
        # Usuário Master padrão conforme solicitado
        try:
            conn.execute("INSERT INTO users VALUES ('master', 'admin123', 'MASTER')")
        except: pass

# --- ESTILIZAÇÃO AGGRESSIVE DARK ---
def apply_theme():
    st.markdown("""
        <style>
        .main { background-color: #050505; color: #e0e0e0; }
        .stMetric { background: #0d1117; border: 1px solid #ff4b4b; border-radius: 12px; padding: 15px; }
        .hot-bet { background: linear-gradient(135deg, #1e3a8a 0%, #020617 100%); padding: 20px; border-radius: 15px; border-left: 5px solid #ff4b4b; margin-bottom: 10px; }
        .stButton>button { background: #ff4b4b; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
        .placar-box { background: #161b22; padding: 10px; border-radius: 5px; border: 1px solid #30363d; text-align: center; font-size: 20px; color: #ff4b4b; }
        </style>
    """, unsafe_allow_html=True)

# --- ENGINE MATEMÁTICO (POISSON) ---
def calculate_poisson(l1, l2):
    max_g = 8
    m1 = [poisson.pmf(i, l1) for i in range(max_g)]
    m2 = [poisson.pmf(i, l2) for i in range(max_g)]
    matrix = np.outer(m1, m2)
    p_a = np.sum(np.tril(matrix, -1))
    p_e = np.sum(np.diag(matrix))
    p_b = np.sum(np.triu(matrix, 1))
    return p_a, p_e, p_b

# --- INTERFACE PRINCIPAL ---
def main():
    apply_theme()
    init_db()

    if 'logged' not in st.session_state:
        st.session_state.logged = False

    if not st.session_state.logged:
        st.title("🛡️ TERMINAL ORACLE ALPHA MASTER")
        u = st.text_input("Usuário Master")
        p = st.text_input("Chave de Acesso", type="password")
        if st.button("DESBLOQUEAR SISTEMA"):
            with sqlite3.connect('oracle_master.db') as conn:
                res = conn.execute("SELECT role FROM users WHERE username=? AND password=?", (u, p)).fetchone()
                if res:
                    st.session_state.logged, st.session_state.user, st.session_state.role = True, u, res[0]
                    st.rerun()
                else: st.error("Acesso Negado.")
        return

    # MENU LATERAL MASTER
    st.sidebar.title(f"💎 MASTER: {st.session_state.user}")
    aba = st.sidebar.radio("Navegação Alpha", ["🚀 Oportunidades & Placares", "🎯 War Room Visual", "📊 Performance Histórica", "👑 Gestão de Logins"])

    # --- ABA 1: OPORTUNIDADES & PLACARES TÉCNICOS ---
    if aba == "🚀 Oportunidades & Placares":
        st.title("🔥 Inteligência de Sinais e Incidentes")
        
        jogos_abertos = [
            {
                "esp": "⚽ Futebol", "evento": "Real Madrid vs Man. City", "local": "Santiago Bernabéu",
                "xG_a": 1.9, "xG_b": 1.5, "agressividade": "Alta", "arbitro": "Marciniak (Rígido)",
                "esc_a": "Mbappé, Vini Jr, Bellingham", "esc_b": "Haaland, De Bruyne, Foden"
            },
            {
                "esp": "🏀 NBA", "evento": "Lakers vs Celtics", "local": "Crypto.com Arena",
                "xG_a": 112, "xG_b": 108, "agressividade": "Média", "arbitro": "Scott Foster",
                "esc_a": "LeBron, Davis", "esc_b": "Tatum, Brown"
            }
        ]

        for jogo in jogos_abertos:
            with st.expander(f"📊 {jogo['evento']} - ANÁLISE TÉCNICA COMPLETA"):
                c1, c2, c3 = st.columns([1, 1, 1])
                
                with c1:
                    st.subheader("🎯 Placares e Vitória")
                    if "Futebol" in jogo['esp']:
                        p_a, p_e, p_b = calculate_poisson(jogo['xG_a'], jogo['xG_b'])
                        st.write(f"**Vencedor Provável:** {'Mandante' if p_a > p_b else 'Visitante'}")
                        st.markdown(f"<div class='placar-box'>{int(jogo['xG_a'])} - {int(jogo['xG_b'])}</div>", unsafe_allow_html=True)
                        st.caption(f"Prob. Empate: {p_e*100:.1f}%")
                    else:
                        st.metric("Projeção Total", f"{jogo['xG_a']} x {jogo['xG_b']}")

                with c2:
                    st.subheader("⚠️ Incidentes")
                    faltas = 24 if jogo['agressividade'] == "Alta" else 16
                    cartoes = 6 if "Rígido" in jogo['arbitro'] else 3
                    st.write(f"**Est. Faltas:** {faltas}")
                    st.write(f"**Est. Cartões:** {cartoes}")
                    st.warning(f"Árbitro: {jogo['arbitro']}")

                with c3:
                    st.subheader("📝 Escalação")
                    st.caption(f"**Destaques:** {jogo['esc_a']} vs {jogo['esc_b']}")
                    st.info(f"📍 {jogo['local']}")

    # --- ABA 2: WAR ROOM VISUAL ---
    elif aba == "🎯 War Room Visual":
        st.title("🎛️ Terminal de Análise em Tempo Real")
        c_vid, c_stats = st.columns([2, 1])
        
        with c_vid:
            st.markdown("<div style='height:350px; background:black; border: 2px solid #ff4b4b; border-radius:15px; display:flex; align-items:center; justify-content:center;'>📺 SINAL DE TRANSMISSÃO / RADAR AO VIVO</div>", unsafe_allow_html=True)
            pressao = pd.DataFrame({'Minuto': range(20), 'Pressão': np.random.randint(10, 100, 20)})
            st.plotly_chart(px.line(pressao, x='Minuto', y='Pressão', title="Gráfico de Pressão de Jogo", template="plotly_dark"))

        with c_stats:
            st.subheader("⚡ Live Stats")
            st.table(pd.DataFrame({"Casa": ["Bet365", "Pinnacle", "Betano"], "Odd": [1.90, 2.05, 1.98]}))
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Placeholder Youtube

    # --- ABA 4: GESTÃO MASTER ---
    elif aba == "👑 Gestão de Logins":
        if st.session_state.role == "MASTER":
            st.title("👑 Painel de Controle Master")
            with st.form("new_user"):
                new_u = st.text_input("Novo Usuário")
                new_p = st.text_input("Senha Temporária")
                if st.form_submit_button("GERAR ACESSO"):
                    with sqlite3.connect('oracle_master.db') as conn:
                        try:
                            conn.execute("INSERT INTO users VALUES (?,?,'USER')", (new_u, new_p))
                            st.success(f"Acesso Liberado para {new_u}!")
                        except: st.error("Usuário já existe.")
        else: st.error("Acesso Negado.")

if __name__ == "__main__":
    main()
