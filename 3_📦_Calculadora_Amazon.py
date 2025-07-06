# pages/3_📦_Calculadora_Amazon.py
import streamlit as st
import datetime 
from engine import calcular_preco

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(page_title="Calculadora Amazon (DBA)", page_icon="📦", layout="wide")

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.title("Precificação para Marketplaces")
st.sidebar.markdown("---")
st.sidebar.markdown("Powered by William Cardoso")

# --- INTERFACE PRINCIPAL ---
st.markdown("# Calculadora de Precificação - Amazon (DBA)")
st.divider()
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Insira os Dados do Produto")
    preco_custo = st.number_input("Custo do Produto (R$)", min_value=0.01, value=50.0, step=1.0, format="%.2f", help="O valor que você pagou pelo produto (unidade).")
    comissao_amazon_percentual = st.number_input("Comissão da Amazon (%)", min_value=0.0, value=15.0, step=0.5, format="%.2f", help="A comissão que a Amazon cobra para a categoria do seu produto. [Consulte a tabela de comissões aqui](https://venda.amazon.com.br/precos).")
    custo_frete_dba = st.number_input("Custo do Frete (Tarifa DBA p/ >= R$79)", min_value=0.0, value=20.0, step=0.5, format="%.2f", help="Para produtos a partir de R$ 79, a tarifa DBA varia com peso e origem. Use a tabela no link para estimar. [Saiba mais sobre as tarifas DBA](https://sellercentral.amazon.com.br/help/hub/reference/external/201382050).")
    promocao_percentual = st.number_input("Promoção / Desconto a Oferecer (%)", min_value=0.0, value=0.0, step=1.0, format="%.1f", help="Se quiser que o preço final tenha um desconto, insira a porcentagem aqui.")
    st.subheader("Método de Cálculo de Custos e Lucro")
    metodo_calculo = st.radio("Escolha como calcular:", ("Percentual sobre a Venda (Margem)", "Índice Markup sobre o Custo"), label_visibility="collapsed", key="amazon_metodo")
    if metodo_calculo == "Percentual sobre a Venda (Margem)":
        imposto_percentual = st.number_input("Imposto sobre a Venda (%)", min_value=0.0, value=7.0, step=0.5, format="%.2f", help="Alíquota de imposto (Ex: SIMPLES Nacional) que incide sobre seu faturamento.")
        custo_unitario_percentual = st.number_input("Custo Unitário da Venda (%)", min_value=0.0, value=10.0, step=0.5, format="%.2f", help="Para descobir o custo de operação da venda considere a média mensal dos últimos 12 meses para a seguinte fórmula, sem incluir o custo com fornedores dos produtos e impostos: (custos fixos + custos variáveis) / faturamento bruto")
    else:
        markup_indice = st.number_input("Índice Markup", min_value=1.0, value=2.2, step=0.1, format="%.2f", help="Multiplicador sobre o custo para cobrir todas as despesas e lucro. Ex: 2.2 para 120% de markup.")

with col2:
    st.header("2. Simule e Analise o Preço Final")
    dados_base = {'preco_custo': preco_custo, 'comissao_amazon_percentual': comissao_amazon_percentual, 'custo_frete_dba': custo_frete_dba}
    kwargs = {}
    if metodo_calculo == "Percentual sobre a Venda (Margem)":
        st.markdown("Arraste para definir seu lucro líquido desejado:")
        lucro_desejado_percentual = st.slider("Lucro Líquido Desejado (%)", min_value=0.0, max_value=100.0, value=15.0, step=0.5, format="%.2f%%")
        dados_base['imposto_percentual'] = imposto_percentual
        dados_base['custo_unitario_percentual'] = custo_unitario_percentual
        kwargs = {'lucro_desejado_percentual': lucro_desejado_percentual}
    else:
        kwargs = {'markup_indice': markup_indice}

    resultado = calcular_preco("Amazon", dados_base, metodo_calculo, promocao_percentual, **kwargs)
    
    st.divider()

    if resultado['erro']:
        st.error(f"**Erro:** {resultado['erro']}")
    else:
        st.subheader("Resultado da Precificação na Amazon (DBA)")
        st.metric(label="Preço de Vitrine (preço cheio)", value=f"R$ {resultado['preco_de_lista']:.2f}")
        if promocao_percentual > 0:
            st.metric(label=f"Preço Final com Desconto ({promocao_percentual}%)", value=f"R$ {resultado['preco_efetivo']:.2f}", delta=f"- R$ {resultado['valor_desconto']:.2f}", delta_color="inverse")
        # ... (expander de detalhamento da Amazon) ...

        # --- SEÇÃO DE SUGESTÕES PARA OUTRAS PLATAFORMAS ---
        st.divider()
        st.subheader("💡 Sugestões para Outras Plataformas")
        with st.expander("Calcular preço para Mercado Livre e Shopee com os mesmos dados de custo e lucro"):
            sug_col1, sug_col2 = st.columns(2)
            with sug_col1:
                st.markdown("##### Mercado Livre")
                ml_taxa = st.number_input("Comissão do Meli (%)", value=17.5, step=0.5, format="%.2f", key="ml_taxa_sug_az")
                ml_frete = st.number_input("Custo Frete Grátis Meli (R$)", value=18.76, step=0.1, format="%.2f", key="ml_frete_sug_az")
            with sug_col2:
                st.markdown("##### Shopee")
                shopee_frete_gratis = st.toggle("Participa do Frete Grátis da Shopee?", value=True, key="shopee_frete_sug_az")

            if st.button("Calcular Sugestões de Preço", key="btn_amazon_sug"):
                # Preparar dados e calcular para Meli
                dados_ml_sug = dados_base.copy()
                dados_ml_sug['taxa_ml_percentual'] = ml_taxa
                dados_ml_sug['custo_frete_gratis'] = ml_frete
                resultado_ml = calcular_preco("Mercado Livre", dados_ml_sug, metodo_calculo, promocao_percentual, **kwargs)
                
                # Preparar dados e calcular para Shopee
                dados_shopee_sug = dados_base.copy()
                dados_shopee_sug['participa_frete_gratis'] = shopee_frete_gratis
                resultado_shopee = calcular_preco("Shopee", dados_shopee_sug, metodo_calculo, promocao_percentual, **kwargs)

                st.markdown("---")
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.markdown("##### Preço Sugerido no Meli")
                    st.metric("Preço de Venda", f"R$ {resultado_ml['preco_de_lista']:.2f}")
                with res_col2:
                    st.markdown("##### Preço Sugerido na Shopee")
                    st.metric("Preço de Venda", f"R$ {resultado_shopee['preco_de_lista']:.2f}")

st.divider()
hoje = datetime.date.today()
data_formatada = hoje.strftime("%d/%m/%Y")
st.caption(f"Informações sobre taxas atualizadas em {data_formatada}.")