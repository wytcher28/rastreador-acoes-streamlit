# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 15:51:51 2025

@author: a840760
"""
import streamlit as st
import requests
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

st.set_page_config(page_title="Rastreador de Ações BR", layout="centered")

def obter_dados_brapi(ticker, intervalo='1d', range_periodo='5d'):
    url = f"https://brapi.dev/api/quote/{ticker}?range={range_periodo}&interval={intervalo}&fundamental=false&dividends=false"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            dados = response.json()
            historico = dados['results'][0]['historicalDataPrice']
            df = pd.DataFrame(historico)
            df['date'] = pd.to_datetime(df['date'], unit='s')
            df.set_index('date', inplace=True)
            df.rename(columns={
                'close': 'Close',
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'volume': 'Volume'
            }, inplace=True)
            return df[['Open', 'High', 'Low', 'Close', 'Volume']]
        except Exception as e:
            st.error(f"Erro ao processar dados da API: {e}")
            return None
    else:
        if response.status_code == 404:
            st.warning("❌ Dados não encontrados para o ticker ou configuração escolhida.")
            st.info("💡 Dica: para intervalos curtos como '1h' ou '15m', use períodos curtos como '1d' ou '2d'.")
        else:
            st.error(f"Erro HTTP: {response.status_code}")
        return None

def plotar_graficos(dados_acao):
    if dados_acao is None or dados_acao.empty:
        st.warning("⚠️ Não há dados disponíveis para plotar.")
        return

    # Gráfico de linha com matplotlib
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dados_acao.index, dados_acao['Close'], label='Fechamento', color='blue')
    ax.set_title('Preço de Fechamento')
    ax.set_xlabel('Data')
    ax.set_ylabel('Preço (R$)')
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # Gráfico de candlestick com mplfinance
    st.subheader("Gráfico Candlestick")
    mpf.plot(dados_acao, type='candle', volume=True, style='charles', title='', mav=(3, 6), returnfig=True)
    fig_candle, _ = mpf.plot(dados_acao, type='candle', volume=True, style='charles', title='Gráfico Candlestick', returnfig=True)
    st.pyplot(fig_candle)

# Interface Streamlit
st.title("📈 Rastreador de Ações (B3 - Brapi)")

with st.form("form_acao"):
    ticker = st.text_input("Ticker (ex: VALE3, PETR4, BBDC4)", "VALE3").strip().upper()
    intervalo = st.selectbox("Intervalo", ['1d', '15m', '1h'])
    periodo = st.selectbox("Período", ['1d', '2d', '5d', '1mo', '6mo', '1y', 'max'])
    enviar = st.form_submit_button("Buscar")

if enviar:
    st.info("Buscando dados...")
    df = obter_dados_brapi(ticker, intervalo, periodo)

    if df is not None:
        st.success("✅ Dados carregados com sucesso!")
        st.dataframe(df.tail())
        plotar_graficos(df)
