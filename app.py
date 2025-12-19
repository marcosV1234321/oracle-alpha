import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from datetime import datetime

# --- CONFIGURAÇÃO DE AMBIENTE ---
st.set_page_config(page_title="ORACLE ALPHA MASTER V8", layout="wide", initial_sidebar_state="expanded")

def init_db():
    with sqlite3.connect('oracle_master.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users 
                     (username TEXT PRIMARY KEY, password TEXT, role TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS logs 
                     (id INTEGER PRIMARY KEY, data TEXT, esporte TEXT, time_a TEXT, time_b TEXT, 
                     prob_a REAL, prob_e REAL, prob_b REAL, resultado_real TEXT)''')
        try:
            conn.execute("INSERT INTO users VALUES ('master', 'admin123', 'MASTER')")
        except: pass

# --- ESTILIZAÇÃO PREMIUM ---
def apply_theme():
    st.markdown("""
        <style>
        .main { background-color: #050505; color: #e0e0e0; }
        .stMetric { background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 15px; }
        .hot-bet { background: linear-gradient(90deg, #1e3a8a 0%, #020617 100%); padding: 20px; border-radius: 15px; border-left: 5px solid #ff4b4b; margin-bottom: 10px; }
        .stButton>button { background: #ff4b4b; color: white; border-radius: 8px; width: 100%; }
        </style>
    """, unsafe_allow_html=True)

# --- MÓDULO DE CÁLCULO ---
def calculate_poisson(l1, l2):
    max_g = 8
    m1 = [poisson.pmf(i, l1) for i in range(max_g)]
    m2 = [poisson.pmf(i, l2) for i in range(max_g)]
    matrix = np.outer(m1, m2)
    return np.sum(np.tril(matrix, -1)), np.sum(np.diag(matrix)), np.sum(np.triu(matrix, 1))

# --- INTERFACE MASTER ---
def main():
    apply_theme()
    init_db()

    if 'logged' not in st.session_state:
        st.session_state.logged = False

    if not st.session_state.logged:
        st.title("🛡️ TERMINAL ORACLE ALPHA")
        u = st.text_input("Usuário Master")
        p = st.text_input("Chave de Acesso", type="password")
        if st.button("ENTRAR"):
            with sqlite3.connect('oracle_master.db') as conn:
                res = conn.execute("SELECT role FROM users WHERE username=? AND password=?", (u, p)).fetchone()
                if res:
                    st.session_state.logged, st.session_state.user, st.session_state.role = True, u, res[0]
                    st.rerun()
        return

    # MENU LATERAL
    st.sidebar.title(f"💎 {st.session_state.user}")
    aba = st.sidebar.radio("Navegação", ["🔥 Oportunidades", "🎯 Analisador War Room", "📊 Performance", "👑 Gestão de Logins"])

    # --- ABA 1: OPORTUNIDADES ---
    if aba == "🔥 Oportunidades":
        st.title("🚀 Sinais de Alta Rentabilidade")
        # Simulação de dados vindo da sua Google Sheets
        oportunidades = [
            {"esp": "⚽ Futebol", "jogo": "Real Madrid vs City", "odd": "1.95", "casa": "Pinnacle"},
            {"esp": "🥊 UFC", "jogo": "Jones vs Miocic", "odd": "2.10", "casa": "Bet365"}
        ]
        for opt in oportunidades:
            st.markdown(f"""<div class='hot-bet'><b>{opt['esp']}</b><br><h3>{opt['jogo']}</h3>
            🎯 Odd: {opt['odd']} na {opt['casa']} | <b>Rentabilidade: Alta</b></div>""", unsafe_allow_html=True)

    # --- ABA 2: WAR ROOM ---
    elif aba == "🎯 Analisador War Room":
        st.title("🎛️ Terminal de Análise Visual")
        esp = st.selectbox("Mercado", ["Futebol", "NBA", "UFC", "Beisebol", "Cavalos"])
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader("📺 Monitor de Transmissão")
            st.markdown("<div style='height:300px; background:black; border-radius:15px; display:flex; align-items:center; justify-content:center; color:#333;'>FEED DE VÍDEO / RADAR EM TEMPO REAL</div>", unsafe_allow_html=True)
            
            # Gráfico de Pressão
            fig = px.area(y=np.random.randint(0,100,20), title="Pressão de Ataque Real-Time", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("📊 Odds Comparadas")
            st.table(pd.DataFrame({"Casa": ["Pinnacle", "Bet365", "Betano"], "Odd": [2.05, 1.95, 1.98]}))
            t1 = st.text_input("Equipe A", "Casa")
            t2 = st.text_input("Equipe B", "Visitante")
            if st.button("GERAR PROBABILIDADE"):
                p_a, p_e, p_b = calculate_poisson(1.8, 1.2)
                st.metric(f"Chance {t1}", f"{p_a*100:.1f}%")
                st.metric(f"Chance {t2}", f"{p_b*100:.1f}%")

    # --- ABA 3: PERFORMANCE ---
    elif aba == "📊 Performance":
        st.title("📈 Estatísticas do Algoritmo")
        with sqlite3.connect('oracle_master.db') as conn:
            df = pd.read_sql_query("SELECT * FROM logs", conn)
        st.dataframe(df)

    # --- ABA 4: GESTÃO MASTER ---
    elif aba == "👑 Gestão de Logins":
        if st.session_state.role == "MASTER":
            st.title("Gerenciador de Usuários")
            new_u = st.text_input("Novo Usuário")
            new_p = st.text_input("Senha")
            if st.button("CRIAR ACESSO"):
                with sqlite3.connect('oracle_master.db') as conn:
                    conn.execute("INSERT INTO users VALUES (?,?,'USER')", (new_u, new_p))
                st.success("Usuário criado!")
        else: st.error("Acesso restrito ao Master.")

if __name__ == "__main__":
    main()
