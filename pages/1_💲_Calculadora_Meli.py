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
    dados_base = {'preco_custo': preco_custo}
    kwargs = {}

    if metodo_calculo == "Percentual sobre a Venda (Margem)":
        st.markdown("Arraste para definir seu lucro líquido desejado:")
        lucro_desejado_percentual = st.slider("Lucro Líquido Desejado (%)", min_value=0.0, max_value=100.0, value=15.0, step=0.5, format="%.2f%%")
        dados_base.update({'imposto_percentual': imposto_percentual, 'custo_unitario_percentual': custo_unitario_percentual})
        kwargs = {'lucro_desejado_percentual': lucro_desejado_percentual}
    else:
        kwargs = {'markup_indice': markup_indice}

    dados_base.update({'taxa_ml_percentual': taxa_ml_percentual, 'custo_frete_gratis': custo_frete_gratis})
    resultado_ml = calcular_preco("Mercado Livre", dados_base, metodo_calculo, promocao_percentual, **kwargs)
    
    st.divider()

    if resultado_ml.get('erro'):
        st.error(f"**Erro:** {resultado_ml['erro']}")
    else:
        st.subheader("Resultado da Precificação no Mercado Livre")
        st.metric(label="Preço de Vitrine (preço cheio)", value=f"R$ {resultado_ml['preco_de_lista']:.2f}")
        if promocao_percentual > 0:
            st.metric(label=f"Preço Final com Desconto ({promocao_percentual}%)", value=f"R$ {resultado_ml['preco_efetivo']:.2f}", delta=f"- R$ {resultado_ml['valor_desconto']:.2f}", delta_color="inverse")
        
        with st.expander("Ver Detalhamento dos Custos e Lucro"):
            st.markdown("##### Custos e Taxas do Mercado Livre")
            col_a, col_b = st.columns(2)
            col_a.metric("Tarifa de Venda", f"R$ {resultado_ml.get('valor_comissao_ml', 0):.2f}")
            if resultado_ml.get('taxa_fixa_aplicada', 0) > 0: col_b.metric("Custo Fixo (< R$ 79)", f"R$ {resultado_ml['taxa_fixa_aplicada']:.2f}")
            if resultado_ml.get('custo_frete_gratis_aplicado', 0) > 0: col_b.metric("Custo Frete Grátis (>= R$ 79)", f"R$ {resultado_ml['custo_frete_gratis_aplicado']:.2f}")
            
            st.markdown("##### Outros Custos e Lucro")
            col_c, col_d, col_e = st.columns(3)
            col_c.metric("Impostos", f"R$ {resultado_ml.get('valor_imposto', 0):.2f}")
            col_d.metric("Custo Unit. Venda", f"R$ {resultado_ml.get('valor_custo_unitario', 0):.2f}")
            col_e.metric("Lucro Líquido (R$)", f"R$ {resultado_ml.get('valor_lucro_liquido', 0):.2f}")

        st.divider()
        st.subheader("💡 Sugestões para Outras Plataformas")
        with st.expander("Calcular preço para Shopee e Amazon com os mesmos dados de custo e lucro"):
            sug_col1, sug_col2 = st.columns(2)
            with sug_col1:
                st.markdown("##### Shopee")
                shopee_frete_gratis = st.toggle("Participa do Frete Grátis da Shopee?", value=True, key="shopee_frete", help="Marque se participa do programa que adiciona 6% de comissão.")
            with sug_col2:
                st.markdown("##### Amazon (DBA)")
                amazon_comissao = st.number_input("Comissão da Amazon (%)", value=15.0, step=0.5, format="%.2f", key="amazon_comissao", help="Comissão da Amazon para a categoria. [Consulte aqui](https://venda.amazon.com.br/precos).")
                amazon_frete = st.number_input("Custo Frete DBA (>= R$79)", value=20.0, step=0.5, format="%.2f", key="amazon_frete", help="Tarifa DBA para produtos acima de R$79. [Consulte aqui](https://sellercentral.amazon.com.br/help/hub/reference/external/201382050).")
            
            if st.button("Calcular Sugestões de Preço"):
                # Calcular para Shopee
                dados_shopee = dados_base.copy()
                dados_shopee['participa_frete_gratis'] = shopee_frete_gratis
                resultado_shopee = calcular_preco("Shopee", dados_shopee, metodo_calculo, promocao_percentual, **kwargs)
                # Calcular para Amazon
                dados_amazon = dados_base.copy()
                dados_amazon['comissao_amazon_percentual'] = amazon_comissao
                dados_amazon['custo_frete_dba'] = amazon_frete
                resultado_amazon = calcular_preco("Amazon", dados_amazon, metodo_calculo, promocao_percentual, **kwargs)

                st.markdown("---")
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.markdown("##### Preço Sugerido na Shopee")
                    st.metric("Preço de Venda", f"R$ {resultado_shopee.get('preco_de_lista', 0):.2f}")
                with res_col2:
                    st.markdown("##### Preço Sugerido na Amazon")
                    st.metric("Preço de Venda", f"R$ {resultado_amazon.get('preco_de_lista', 0):.2f}")

st.divider()
hoje = datetime.date.today()
data_formatada = hoje.strftime("%d/%m/%Y")
st.caption(f"Informações sobre taxas atualizadas em {data_formatada}.")
