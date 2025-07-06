# pages/4_🔍_Calculadora_Reversa.py
import streamlit as st
import datetime 
from engine import obter_taxa_fixa_meli, obter_tarifa_dba_amazon

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(page_title="Calculadora Reversa", page_icon="🔍", layout="wide")

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.title("Precificação para Marketplaces")
st.sidebar.markdown("---")
st.sidebar.markdown("Powered by William Cardoso")

# --- CORPO DA PÁGINA ---
st.markdown("# 🔍 Calculadora Reversa de Lucratividade")
st.markdown("Descubra se um anúncio existente está dando lucro ou prejuízo com base no seu preço de venda atual.")
st.divider()

# --- SELEÇÃO DE PLATAFORMA ---
plataforma = st.selectbox(
    "Para qual plataforma é o anúncio que você quer analisar?",
    ("Mercado Livre", "Shopee", "Amazon")
)

# ===================================================================
# CALCULADORA REVERSA PARA MERCADO LIVRE
# ===================================================================
if plataforma == "Mercado Livre":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.header("1. Insira os Dados do Anúncio Meli")
        preco_venda_atual = st.number_input("Preço de Venda Atual (R$)", min_value=0.01, value=150.0, step=1.0, format="%.2f", help="O preço 'cheio' que está no seu anúncio agora.", key="ml_preco")
        promocao_percentual = st.number_input("Desconto oferecido no anúncio (%)", min_value=0.0, value=0.0, step=1.0, format="%.1f", help="Se o anúncio tem uma promoção ativa, insira a porcentagem aqui.", key="ml_promo")
        st.markdown("---")
        preco_custo = st.number_input("Custo do Produto (R$)", min_value=0.01, value=50.0, step=1.0, format="%.2f", help="O valor que você pagou pelo produto.", key="ml_custo")
        taxa_ml_percentual = st.number_input("Comissão do Anúncio (%)", min_value=0.0, value=17.5, step=0.5, format="%.2f", help="A comissão percentual que o Mercado Livre cobra neste anúncio.", key="ml_comissao")
        custo_frete_pago = st.number_input("Custo de Frete Pago por Venda (R$)", min_value=0.0, value=18.76, step=0.1, format="%.2f", help="O valor exato de frete que é descontado de você a cada venda deste item.", key="ml_frete")
        imposto_percentual = st.number_input("Imposto sobre a Venda (%)", min_value=0.0, value=7.0, step=0.5, format="%.2f", help="Sua alíquota de imposto sobre o faturamento.", key="ml_imposto")
        custo_unitario_percentual = st.number_input("Custo Unitário da Venda (%)", min_value=0.0, value=10.0, step=0.5, format="%.2f", help="Seu custo operacional como um percentual do faturamento.", key="ml_custo_op")

    preco_efetivo = preco_venda_atual * (1 - (promocao_percentual / 100))
    valor_comissao_ml = preco_efetivo * (taxa_ml_percentual / 100)
    taxa_fixa_aplicada = obter_taxa_fixa_meli(preco_efetivo)
    valor_imposto = preco_efetivo * (imposto_percentual / 100)
    valor_custo_unitario = preco_efetivo * (custo_unitario_percentual / 100)
    total_custos = (preco_custo + valor_comissao_ml + taxa_fixa_aplicada + custo_frete_pago + valor_imposto + valor_custo_unitario)
    lucro_prejuizo_valor = preco_efetivo - total_custos
    lucro_prejuizo_percentual = (lucro_prejuizo_valor / preco_efetivo) * 100 if preco_efetivo > 0 else 0

    with col2:
        st.header("2. Análise de Lucratividade")
        st.divider()
        if lucro_prejuizo_valor >= 0: st.success("Este anúncio está gerando LUCRO!")
        else: st.error("Atenção: Este anúncio está gerando PREJUÍZO!")
        st.metric(label="Resultado Final por Venda (Lucro/Prejuízo)", value=f"R$ {lucro_prejuizo_valor:.2f}", delta=f"{lucro_prejuizo_percentual:.2f} %", delta_color=("normal" if lucro_prejuizo_valor >= 0 else "inverse"))
        with st.expander("Ver Balanço Financeiro da Venda"):
            st.markdown(f"**Receita Efetiva (após desconto): R$ {preco_efetivo:.2f}**")
            st.markdown("---")
            st.markdown("**Custos Totais por Venda:**")
            st.table({"Item de Custo": ["Custo do Produto", "Comissão do ML", "Taxa Fixa do ML", "Frete Pago", "Impostos", "Custo Unitário da Venda"], "Valor (R$)": [f"R$ {preco_custo:.2f}", f"R$ {valor_comissao_ml:.2f}", f"R$ {taxa_fixa_aplicada:.2f}", f"R$ {custo_frete_pago:.2f}", f"R$ {valor_imposto:.2f}", f"R$ {valor_custo_unitario:.2f}"]})
            st.markdown(f"**Soma de Todos os Custos: R$ {total_custos:.2f}**")
            st.markdown("---")
            st.markdown(f"**Resultado (Receita - Custos): R$ {lucro_prejuizo_valor:.2f} ({lucro_prejuizo_percentual:.2f}%)**")

# ===================================================================
# CALCULADORA REVERSA PARA SHOPEE
# ===================================================================
elif plataforma == "Shopee":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.header("1. Insira os Dados do Anúncio Shopee")
        preco_venda_atual = st.number_input("Preço de Venda Atual (R$)", min_value=0.01, value=150.0, step=1.0, format="%.2f", help="O preço 'cheio' que está no seu anúncio agora.", key="shopee_preco")
        promocao_percentual = st.number_input("Desconto oferecido no anúncio (%)", min_value=0.0, value=0.0, step=1.0, format="%.1f", help="Se o anúncio tem uma promoção ativa, insira a porcentagem aqui.", key="shopee_promo")
        st.markdown("---")
        preco_custo = st.number_input("Custo do Produto (R$)", min_value=0.01, value=50.0, step=1.0, format="%.2f", help="O valor que você pagou pelo produto.", key="shopee_custo")
        participa_frete_gratis = st.toggle("Anúncio com selo de Frete Grátis?", value=True, help="Marque se este anúncio tem o selo do Programa de Frete Grátis (comissão adicional de 6%).")
        imposto_percentual = st.number_input("Imposto sobre a Venda (%)", min_value=0.0, value=7.0, step=0.5, format="%.2f", help="Sua alíquota de imposto sobre o faturamento.", key="shopee_imposto")
        custo_unitario_percentual = st.number_input("Custo Unitário da Venda (%)", min_value=0.0, value=10.0, step=0.5, format="%.2f", help="Seu custo operacional como um percentual do faturamento.", key="shopee_custo_op")

    preco_efetivo = preco_venda_atual * (1 - (promocao_percentual / 100))
    comissao_padrao = min(preco_efetivo * 0.14, 100.00)
    adicional_frete = preco_efetivo * 0.06 if participa_frete_gratis else 0
    taxa_transacao = 3.00
    valor_imposto = preco_efetivo * (imposto_percentual / 100)
    valor_custo_unitario = preco_efetivo * (custo_unitario_percentual / 100)
    total_custos = (preco_custo + comissao_padrao + adicional_frete + taxa_transacao + valor_imposto + valor_custo_unitario)
    lucro_prejuizo_valor = preco_efetivo - total_custos
    lucro_prejuizo_percentual = (lucro_prejuizo_valor / preco_efetivo) * 100 if preco_efetivo > 0 else 0

    with col2:
        st.header("2. Análise de Lucratividade")
        st.divider()
        if lucro_prejuizo_valor >= 0: st.success("Este anúncio está gerando LUCRO!")
        else: st.error("Atenção: Este anúncio está gerando PREJUÍZO!")
        st.metric(label="Resultado Final por Venda (Lucro/Prejuízo)", value=f"R$ {lucro_prejuizo_valor:.2f}", delta=f"{lucro_prejuizo_percentual:.2f} %", delta_color=("normal" if lucro_prejuizo_valor >= 0 else "inverse"))
        with st.expander("Ver Balanço Financeiro da Venda"):
            st.markdown(f"**Receita Efetiva (após desconto): R$ {preco_efetivo:.2f}**")
            st.markdown("---")
            st.markdown("**Custos Totais por Venda:**")
            st.table({"Item de Custo": ["Custo do Produto", "Comissão Padrão (14%)", "Adicional Frete Grátis (6%)", "Taxa de Transação", "Impostos", "Custo Unitário da Venda"], "Valor (R$)": [f"R$ {preco_custo:.2f}", f"R$ {comissao_padrao:.2f}", f"R$ {adicional_frete:.2f}", f"R$ {taxa_transacao:.2f}", f"R$ {valor_imposto:.2f}", f"R$ {valor_custo_unitario:.2f}"]})
            st.markdown(f"**Soma de Todos os Custos: R$ {total_custos:.2f}**")
            st.markdown("---")
            st.markdown(f"**Resultado (Receita - Custos): R$ {lucro_prejuizo_valor:.2f} ({lucro_prejuizo_percentual:.2f}%)**")

# ===================================================================
# CALCULADORA REVERSA PARA AMAZON
# ===================================================================
elif plataforma == "Amazon":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.header("1. Insira os Dados do Anúncio Amazon (DBA)")
        preco_venda_atual = st.number_input("Preço de Venda Atual (R$)", min_value=0.01, value=150.0, step=1.0, format="%.2f", help="O preço 'cheio' que está no seu anúncio agora.", key="az_preco")
        promocao_percentual = st.number_input("Desconto oferecido no anúncio (%)", min_value=0.0, value=0.0, step=1.0, format="%.1f", help="Se o anúncio tem uma promoção ativa, insira a porcentagem aqui.", key="az_promo")
        st.markdown("---")
        preco_custo = st.number_input("Custo do Produto (R$)", min_value=0.01, value=50.0, step=1.0, format="%.2f", help="O valor que você pagou pelo produto.", key="az_custo")
        comissao_amazon_percentual = st.number_input("Comissão da Amazon (%)", min_value=0.0, value=15.0, step=0.5, format="%.2f", help="A comissão percentual que a Amazon cobra neste anúncio.", key="az_comissao")
        custo_frete_pago = st.number_input("Custo de Frete/Tarifa DBA Pago (R$)", min_value=0.0, value=20.0, step=0.1, format="%.2f", help="O valor exato da tarifa DBA (seja a fixa ou de frete) que é descontado de você.", key="az_frete")
        imposto_percentual = st.number_input("Imposto sobre a Venda (%)", min_value=0.0, value=7.0, step=0.5, format="%.2f", help="Sua alíquota de imposto sobre o faturamento.", key="az_imposto")
        custo_unitario_percentual = st.number_input("Custo Unitário da Venda (%)", min_value=0.0, value=10.0, step=0.5, format="%.2f", help="Seu custo operacional como um percentual do faturamento.", key="az_custo_op")

    preco_efetivo = preco_venda_atual * (1 - (promocao_percentual / 100))
    valor_comissao_amazon = preco_efetivo * (comissao_amazon_percentual / 100)
    # Na calculadora reversa da Amazon, o usuário informa o custo total do DBA, já que ele pode variar muito.
    valor_imposto = preco_efetivo * (imposto_percentual / 100)
    valor_custo_unitario = preco_efetivo * (custo_unitario_percentual / 100)
    total_custos = (preco_custo + valor_comissao_amazon + custo_frete_pago + valor_imposto + valor_custo_unitario)
    lucro_prejuizo_valor = preco_efetivo - total_custos
    lucro_prejuizo_percentual = (lucro_prejuizo_valor / preco_efetivo) * 100 if preco_efetivo > 0 else 0

    with col2:
        st.header("2. Análise de Lucratividade")
        st.divider()
        if lucro_prejuizo_valor >= 0: st.success("Este anúncio está gerando LUCRO!")
        else: st.error("Atenção: Este anúncio está gerando PREJUÍZO!")
        st.metric(label="Resultado Final por Venda (Lucro/Prejuízo)", value=f"R$ {lucro_prejuizo_valor:.2f}", delta=f"{lucro_prejuizo_percentual:.2f} %", delta_color=("normal" if lucro_prejuizo_valor >= 0 else "inverse"))
        with st.expander("Ver Balanço Financeiro da Venda"):
            st.markdown(f"**Receita Efetiva (após desconto): R$ {preco_efetivo:.2f}**")
            st.markdown("---")
            st.markdown("**Custos Totais por Venda:**")
            st.table({"Item de Custo": ["Custo do Produto", "Comissão da Amazon", "Custo do Frete/Tarifa DBA", "Impostos", "Custo Unitário da Venda"], "Valor (R$)": [f"R$ {preco_custo:.2f}", f"R$ {valor_comissao_amazon:.2f}", f"R$ {custo_frete_pago:.2f}", f"R$ {valor_imposto:.2f}", f"R$ {valor_custo_unitario:.2f}"]})
            st.markdown(f"**Soma de Todos os Custos: R$ {total_custos:.2f}**")
            st.markdown("---")
            st.markdown(f"**Resultado (Receita - Custos): R$ {lucro_prejuizo_valor:.2f} ({lucro_prejuizo_percentual:.2f}%)**")

st.divider()
hoje = datetime.date.today()
data_formatada = hoje.strftime("%d/%m/%Y")
st.caption(f"Informações sobre taxas atualizadas em {data_formatada}.")
