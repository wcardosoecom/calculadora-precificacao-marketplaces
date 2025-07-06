# pages/1_💲_Calculadora_Meli.py
import streamlit as st
import datetime
from engine import calcular_preco

st.set_page_config(page_title="Calculadora Meli", page_icon="💲", layout="wide")

st.sidebar.title("Precificação para Marketplaces")
st.sidebar.markdown("---")
st.sidebar.markdown("Powered by William Cardoso")

st.markdown("# Calculadora de Precificação - Mercado Livre")
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Insira os Dados do Produto")
    preco_custo = st.number_input("Custo do Produto (R$)", min_value=0.01, value=50.0, step=1.0, format="%.2f", help="O valor que você pagou pelo produto (unidade).", key="ml_main_custo")
    taxa_ml_percentual = st.number_input("Comissão do Anúncio (%)", min_value=0.0, value=17.5, step=0.5, format="%.2f", help="A comissão que o Mercado Livre cobra para a categoria e tipo do seu anúncio. [Consulte as tarifas aqui](https://www.mercadolivre.com.br/landing/custos-de-venda/tarifas-de-venda).", key="ml_main_taxa")
    custo_frete_gratis = st.number_input("Custo do Frete Grátis (R$)", min_value=0.0, value=18.76, step=0.5, format="%.2f", help="O valor do frete que será descontado de você em vendas a partir de R$ 79,00. [Saiba mais sobre os custos de frete](https://www.mercadolivre.com.br/ajuda/40538).", key="ml_main_frete")
    promocao_percentual = st.number_input("Promoção / Desconto a Oferecer (%)", min_value=0.0, value=0.0, step=1.0, format="%.1f", help="Se quiser que o preço final tenha um desconto, insira a porcentagem aqui.", key="ml_main_promo")
    st.subheader("Método de Cálculo de Custos e Lucro")
    metodo_calculo = st.radio("Escolha como calcular:", ("Percentual sobre a Venda (Margem)", "Índice Markup sobre o Custo"), label_visibility="collapsed", key="ml_main_metodo")
    if metodo_calculo == "Percentual sobre a Venda (Margem)":
        imposto_percentual = st.number_input("Imposto sobre a Venda (%)", min_value=0.0, value=7.0, step=0.5, format="%.2f", help="Alíquota de imposto (Ex: SIMPLES Nacional) que incide sobre seu faturamento.", key="ml_main_imposto")
        custo_unitario_percentual = st.number_input("Custo Unitário da Venda (%)", min_value=0.0, value=10.0, step=0.5, format="%.2f", help="Para descobir o custo de operação da venda considere a média mensal dos últimos 12 meses para a seguinte fórmula, sem incluir o custo com fornedores dos produtos e impostos: (custos fixos + custos variáveis) / faturamento bruto", key="ml_main_custo_op")
    else:
        markup_indice = st.number_input("Índice Markup", min_value=1.0, value=2.2, step=0.1, format="%.2f", help="Multiplicador sobre o custo para cobrir todas as despesas e lucro. Ex: 2.2 para 120% de markup.", key="ml_main_markup")

with col2:
    st.header("2. Simule e Analise o Preço Final")
    dados_base = {'preco_custo': preco_custo, 'taxa_ml_percentual': taxa_ml_percentual, 'custo_frete_gratis': custo_frete_gratis}
    kwargs = {}
    if metodo_calculo == "Percentual sobre a Venda (Margem)":
        st.markdown("Arraste para definir seu lucro líquido desejado:")
        lucro_desejado_percentual = st.slider("Lucro Líquido Desejado (%)", min_value=0.0, max_value=100.0, value=15.0, step=0.5, format="%.2f%%")
        dados_base.update({'imposto_percentual': imposto_percentual, 'custo_unitario_percentual': custo_unitario_percentual})
        kwargs = {'lucro_desejado_percentual': lucro_desejado_percentual}
    else:
        kwargs = {'markup_indice': markup_indice}

    resultado_ml = calcular_preco("Mercado Livre", dados_base, metodo_calculo, promocao_percentual, **kwargs)
    
    st.divider()

    if resultado_ml.get('erro'):
        st.error(f"**Erro:** {resultado_ml['erro']}")
    else:
        # (O restante do código de exibição do resultado e das sugestões continua o mesmo)
        st.subheader("Resultado da Precificação no Mercado Livre")
        # ... e assim por diante