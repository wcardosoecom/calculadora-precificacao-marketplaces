# pages/3_📦_Calculadora_Amazon.py
import streamlit as st
import datetime
from engine import calcular_preco

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(page_title="Calculadora Amazon", page_icon="📦", layout="wide")

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
    preco_custo = st.number_input("Custo do Produto (R$)", min_value=0.01, value=50.0, step=1.0, format="%.2f", help="O valor que você pagou pelo produto (unidade).", key="az_main_custo")
    comissao_amazon_percentual = st.number_input("Comissão da Amazon (%)", min_value=0.0, value=15.0, step=0.5, format="%.2f", help="A comissão que a Amazon cobra para a categoria do seu produto. [Consulte a tabela de comissões aqui](https://venda.amazon.com.br/precos).", key="az_main_comissao")
    custo_frete_dba = st.number_input("Custo do Frete (Tarifa DBA p/ >= R$79)", min_value=0.0, value=20.0, step=0.5, format="%.2f", help="Para produtos a partir de R$ 79, a tarifa DBA varia com peso e origem. Use a tabela no link para estimar. [Saiba mais sobre as tarifas DBA](https://sellercentral.amazon.com.br/help/hub/reference/external/201382050).", key="az_main_frete")
    promocao_percentual = st.number_input("Promoção / Desconto a Oferecer (%)", min_value=0.0, value=0.0, step=1.0, format="%.1f", help="Se quiser que o preço final tenha um desconto, insira a porcentagem aqui.", key="az_main_promo")
    st.subheader("Método de Cálculo de Custos e Lucro")
    metodo_calculo = st.radio("Escolha como calcular:", ("Percentual sobre a Venda (Margem)", "Índice Markup sobre o Custo"), label_visibility="collapsed", key="az_main_metodo")
    if metodo_calculo == "Percentual sobre a Venda (Margem)":
        imposto_percentual = st.number_input("Imposto sobre a Venda (%)", min_value=0.0, value=7.0, step=0.5, format="%.2f", help="Alíquota de imposto (Ex: SIMPLES Nacional) que incide sobre seu faturamento.", key="az_main_imposto")
        custo_unitario_percentual = st.number_input("Custo Unitário da Venda (%)", min_value=0.0, value=10.0, step=0.5, format="%.2f", help="Para descobir o custo de operação da venda considere a média mensal dos últimos 12 meses para a seguinte fórmula, sem incluir o custo com fornedores dos produtos e impostos: (custos fixos + custos variáveis) / faturamento bruto", key="az_main_custo_op")
    else:
        markup_indice = st.number_input("Índice Markup", min_value=1.0, value=2.2, step=0.1, format="%.2f", help="Multiplicador sobre o custo para cobrir todas as despesas e lucro. Ex: 2.2 para 120% de markup.", key="az_main_markup")

with col2:
    st.header("2. Simule e Analise o Preço Final")
    dados_base = {'preco_custo': preco_custo}
    kwargs = {}

    if metodo_calculo == "Percentual sobre a Venda (Margem)":
        st.markdown("Arraste para definir seu lucro líquido desejado:")
        lucro_desejado_percentual = st.slider("Lucro Líquido Desejado (%)", min_value=0.0, max_value=100.0, value=15.0, step=0.5, format="%.2f%%", key="az_main_lucro")
        dados_base.update({'imposto_percentual': imposto_percentual, 'custo_unitario_percentual': custo_unitario_percentual})
        kwargs = {'lucro_desejado_percentual': lucro_desejado_percentual}
    else:
        kwargs = {'markup_indice': markup_indice}

    dados_base.update({'comissao_amazon_percentual': comissao_amazon_percentual, 'custo_frete_dba': custo_frete_dba})
    resultado_amazon = calcular_preco("Amazon", dados_base, metodo_calculo, promocao_percentual, **kwargs)
    
    st.divider()

    if resultado_amazon.get('erro'):
        st.error(f"**Erro:** {resultado_amazon['erro']}")
    else:
        st.subheader("Resultado da Precificação na Amazon (DBA)")
        st.metric(label="Preço de Vitrine (preço cheio)", value=f"R$ {resultado_amazon['preco_de_lista']:.2f}")
        if promocao_percentual > 0:
            st.metric(label=f"Preço Final com Desconto ({promocao_percentual}%)", value=f"R$ {resultado_amazon['preco_efetivo']:.2f}", delta=f"- R$ {resultado_amazon['valor_desconto']:.2f}", delta_color="inverse")
        
        # --- BLOCO DE DETALHAMENTO QUE ESTAVA FALTANDO ---
        if metodo_calculo == "Percentual sobre a Venda (Margem)":
            with st.expander("Ver Detalhamento dos Custos e Lucro"):
                st.markdown("##### Custos e Taxas da Amazon (DBA)")
                col_a, col_b = st.columns(2)
                col_a.metric("Comissão Amazon", f"R$ {resultado_amazon.get('valor_comissao_amazon', 0):.2f}")
                if resultado_amazon.get('tarifa_dba_unidade', 0) > 0: col_b.metric("Tarifa por Unidade (< R$ 79)", f"R$ {resultado_amazon['tarifa_dba_unidade']:.2f}")
                if resultado_amazon.get('custo_frete_dba_aplicado', 0) > 0: col_b.metric("Custo Frete DBA (>= R$ 79)", f"R$ {resultado_amazon['custo_frete_dba_aplicado']:.2f}")
                
                st.markdown("##### Outros Custos e Lucro")
                col_c, col_d, col_e = st.columns(3)
                col_c.metric("Impostos", f"R$ {resultado_amazon.get('valor_imposto', 0):.2f}")
                col_d.metric("Custo Unit. Venda", f"R$ {resultado_amazon.get('valor_custo_unitario', 0):.2f}")
                col_e.metric("Lucro Líquido (R$)", f"R$ {resultado_amazon.get('valor_lucro_liquido', 0):.2f}")
        else: # Markup
            with st.expander("Ver Detalhamento da Composição do Preço"):
                st.metric("Custo do Produto", f"R$ {dados_base['preco_custo']:.2f}")
                st.markdown("---")
                st.markdown("##### Taxas da Amazon (DBA)")
                col_a, col_b = st.columns(2)
                col_a.metric(f"Comissão Amazon ({comissao_amazon_percentual}%)", f"R$ {resultado_amazon.get('valor_comissao_amazon', 0):.2f}")
                if resultado_amazon.get('tarifa_dba_unidade', 0) > 0: col_b.metric("Tarifa por Unidade (< R$ 79)", f"R$ {resultado_amazon['tarifa_dba_unidade']:.2f}")
                if resultado_amazon.get('custo_frete_dba_aplicado', 0) > 0: col_b.metric("Custo Frete DBA (>= R$ 79)", f"R$ {resultado_amazon['custo_frete_dba_aplicado']:.2f}")
                
                st.markdown("---")
                st.markdown("##### Resultado da Operação")
                margem_bruta_percentual = (resultado_amazon.get('margem_bruta', 0) / resultado_amazon['preco_efetivo']) * 100 if resultado_amazon['preco_efetivo'] > 0 else 0
                col_c, col_d = st.columns(2)
                col_c.metric("Margem Bruta (R$)", f"R$ {resultado_amazon.get('margem_bruta', 0):.2f}", help="Valor que sobra para cobrir seus impostos e gerar lucro.")
                col_d.metric("Margem Bruta (%)", f"{margem_bruta_percentual:.2f}%", help="Percentual do preço de venda que corresponde à sua margem bruta.")

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
                sug_dados_base = dados_base.copy()
                sug_kwargs = kwargs.copy()

                # Calcular para Meli
                sug_dados_base.update({'taxa_ml_percentual': ml_taxa, 'custo_frete_gratis': ml_frete})
                resultado_ml = calcular_preco("Mercado Livre", sug_dados_base, metodo_calculo, promocao_percentual, **sug_kwargs)
                
                # Calcular para Shopee
                sug_dados_base.update({'participa_frete_gratis': shopee_frete_gratis})
                resultado_shopee = calcular_preco("Shopee", sug_dados_base, metodo_calculo, promocao_percentual, **sug_kwargs)

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
