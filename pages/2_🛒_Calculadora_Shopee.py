# pages/2_🛒_Calculadora_Shopee.py
import streamlit as st
import datetime
from engine import calcular_preco, COMISSAO_PADRAO_SHOPEE_PERC, ADICIONAL_FRETE_GRATIS_PERC

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(page_title="Calculadora Shopee", page_icon="🛒", layout="wide")

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.title("Precificação para Marketplaces")
st.sidebar.markdown("---")
st.sidebar.markdown("Powered by William Cardoso")

# --- INTERFACE PRINCIPAL ---
st.markdown("# Calculadora de Precificação - Shopee")
st.divider()
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Insira os Dados do Produto")
    preco_custo = st.number_input("Custo do Produto (R$)", min_value=0.01, value=50.0, step=1.0, format="%.2f", help="O valor que você pagou pelo produto (unidade).", key="shopee_main_custo")
    participa_frete_gratis = st.toggle("Participante do Programa de Frete Grátis", value=True, help="Por padrão, o cálculo considera a comissão adicional de 6%. Desmarque esta opção caso você **não** participe do programa.", key="shopee_main_frete")
    promocao_percentual = st.number_input("Promoção / Desconto a Oferecer (%)", min_value=0.0, value=0.0, step=1.0, format="%.1f", help="Se quiser que o preço final tenha um desconto, insira a porcentagem aqui.", key="shopee_main_promo")
    st.subheader("Método de Cálculo de Custos e Lucro")
    metodo_calculo = st.radio("Escolha como calcular:", ("Percentual sobre a Venda (Margem)", "Índice Markup sobre o Custo"), label_visibility="collapsed", key="shopee_main_metodo")
    if metodo_calculo == "Percentual sobre a Venda (Margem)":
        imposto_percentual = st.number_input("Imposto sobre a Venda (%)", min_value=0.0, value=7.0, step=0.5, format="%.2f", help="Alíquota de imposto (Ex: SIMPLES Nacional) que incide sobre seu faturamento.", key="shopee_main_imposto")
        custo_unitario_percentual = st.number_input("Custo da Venda (%)", min_value=0.0, value=10.0, step=0.5, format="%.2f", help="Para descobir o custo de operação da venda considere a média mensal dos últimos 12 meses para a seguinte fórmula, sem incluir o custo com fornedores dos produtos e impostos: (custos fixos + custos variáveis) / faturamento bruto. Ex: Custo médio mensal: R$5.000,00 e Faturamento médio mensal: R$25.000,00, logo o Custo da venda = 20%", key="shopee_main_custo_op")
    else:
        markup_indice = st.number_input("Índice Markup", min_value=1.0, value=2.2, step=0.1, format="%.2f", help="Multiplicador sobre o custo para cobrir todas as despesas e lucro. Ex: 2.2 para 120% de markup.", key="shopee_main_markup")

with col2:
    st.header("2. Simule e Analise o Preço Final")
    dados_base = {'preco_custo': preco_custo, 'participa_frete_gratis': participa_frete_gratis}
    kwargs = {}
    if metodo_calculo == "Percentual sobre a Venda (Margem)":
        st.markdown("Arraste para definir seu lucro líquido desejado:")
        lucro_desejado_percentual = st.slider("Lucro Líquido Desejado (%)", min_value=0.0, max_value=100.0, value=15.0, step=0.5, format="%.2f%%", key="shopee_main_lucro")
        dados_base.update({'imposto_percentual': imposto_percentual, 'custo_unitario_percentual': custo_unitario_percentual})
        kwargs = {'lucro_desejado_percentual': lucro_desejado_percentual}
    else:
        kwargs = {'markup_indice': markup_indice}

    resultado_shopee = calcular_preco("Shopee", dados_base, metodo_calculo, promocao_percentual, **kwargs)
    
    st.divider()

    if resultado_shopee.get('erro'):
        st.error(f"**Erro:** {resultado_shopee['erro']}")
    else:
        st.subheader("Resultado da Precificação na Shopee")
        st.metric(label="Preço de Vitrine (preço cheio)", value=f"R$ {resultado_shopee['preco_de_lista']:.2f}")
        if promocao_percentual > 0:
            st.metric(label=f"Preço Final com Desconto ({promocao_percentual}%)", value=f"R$ {resultado_shopee['preco_efetivo']:.2f}", delta=f"- R$ {resultado_shopee['valor_desconto']:.2f}", delta_color="inverse")
        
        # --- BLOCO DE DETALHAMENTO QUE ESTAVA FALTANDO ---
        if metodo_calculo == "Percentual sobre a Venda (Margem)":
            with st.expander("Ver Detalhamento dos Custos e Lucro"):
                st.markdown("##### Custos e Taxas da Shopee")
                total_comissao = resultado_shopee.get('comissao_padrao_aplicada', 0) + resultado_shopee.get('adicional_frete_aplicado', 0)
                comissao_perc_exibida = COMISSAO_PADRAO_SHOPEE_PERC + (ADICIONAL_FRETE_GRATIS_PERC if dados_base['participa_frete_gratis'] else 0)
                
                col_a, col_b = st.columns(2)
                col_a.metric(f"Comissão Total ({comissao_perc_exibida:.0f}%)", f"R$ {total_comissao:.2f}", help=f"Comissão Padrão ({COMISSAO_PADRAO_SHOPEE_PERC}%): R${resultado_shopee.get('comissao_padrao_aplicada', 0):.2f} + Adicional Frete: R${resultado_shopee.get('adicional_frete_aplicado', 0):.2f}")
                col_b.metric("Taxa de Transação", f"R$ {resultado_shopee.get('taxa_transacao_aplicada', 0):.2f}")
                
                st.markdown("##### Outros Custos e Lucro")
                col_c, col_d, col_e = st.columns(3)
                col_c.metric("Impostos", f"R$ {resultado_shopee.get('valor_imposto', 0):.2f}")
                col_d.metric("Custo Unit. Venda", f"R$ {resultado_shopee.get('valor_custo_unitario', 0):.2f}")
                col_e.metric("Lucro Líquido (R$)", f"R$ {resultado_shopee.get('valor_lucro_liquido', 0):.2f}")
        else: # Markup
            with st.expander("Ver Detalhamento da Composição do Preço"):
                st.metric("Custo do Produto", f"R$ {dados_base['preco_custo']:.2f}")
                st.markdown("---")
                st.markdown("##### Taxas da Shopee")
                total_comissao = resultado_shopee.get('comissao_padrao_aplicada', 0) + resultado_shopee.get('adicional_frete_aplicado', 0)
                comissao_perc_exibida = COMISSAO_PADRAO_SHOPEE_PERC + (ADICIONAL_FRETE_GRATIS_PERC if dados_base['participa_frete_gratis'] else 0)
                
                col_a, col_b = st.columns(2)
                col_a.metric(f"Comissão Total ({comissao_perc_exibida:.0f}%)", f"R$ {total_comissao:.2f}", help=f"Comissão Padrão ({COMISSAO_PADRAO_SHOPEE_PERC}%): R${resultado_shopee.get('comissao_padrao_aplicada', 0):.2f} + Adicional Frete: R${resultado_shopee.get('adicional_frete_aplicado', 0):.2f}")
                col_b.metric("Taxa de Transação", f"R$ {resultado_shopee.get('taxa_transacao_aplicada', 0):.2f}")

                st.markdown("---")
                st.markdown("##### Resultado da Operação")
                margem_bruta_percentual = (resultado_shopee.get('margem_bruta', 0) / resultado_shopee['preco_efetivo']) * 100 if resultado_shopee['preco_efetivo'] > 0 else 0
                col_c, col_d = st.columns(2)
                col_c.metric("Margem Bruta (R$)", f"R$ {resultado_shopee.get('margem_bruta', 0):.2f}", help="Valor que sobra para cobrir seus impostos e gerar lucro.")
                col_d.metric("Margem Bruta (%)", f"{margem_bruta_percentual:.2f}%", help="Percentual do preço de venda que corresponde à sua margem bruta.")

        # --- SEÇÃO DE SUGESTÕES PARA OUTRAS PLATAFORMAS ---
        st.divider()
        st.subheader("💡 Sugestões para Outras Plataformas")
        with st.expander("Calcular preço para Mercado Livre e Amazon com os mesmos dados de custo e lucro"):
            sug_col1, sug_col2 = st.columns(2)
            with sug_col1:
                st.markdown("##### Mercado Livre")
                ml_taxa = st.number_input("Comissão do Meli (%)", value=17.5, step=0.5, format="%.2f", key="ml_taxa_sug_sh")
                ml_frete = st.number_input("Custo Frete Grátis Meli (R$)", value=18.76, step=0.1, format="%.2f", key="ml_frete_sug_sh")
            with sug_col2:
                st.markdown("##### Amazon (DBA)")
                amazon_comissao = st.number_input("Comissão da Amazon (%)", value=15.0, step=0.5, format="%.2f", key="amazon_comissao_sug_sh")
                amazon_frete = st.number_input("Custo Frete DBA (>= R$79)", value=20.0, step=0.1, format="%.2f", key="amazon_frete_sug_sh")

            if st.button("Calcular Sugestões de Preço", key="btn_shopee_sug_sh"):
                sug_dados_base = dados_base.copy()
                sug_kwargs = kwargs.copy()

                # Calcular para Meli
                sug_dados_base.update({'taxa_ml_percentual': ml_taxa, 'custo_frete_gratis': ml_frete})
                resultado_ml = calcular_preco("Mercado Livre", sug_dados_base, metodo_calculo, promocao_percentual, **sug_kwargs)
                
                # Calcular para Amazon
                sug_dados_base.update({'comissao_amazon_percentual': amazon_comissao, 'custo_frete_dba': amazon_frete})
                resultado_amazon = calcular_preco("Amazon", sug_dados_base, metodo_calculo, promocao_percentual, **sug_kwargs)

                st.markdown("---")
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.markdown("##### Preço Sugerido no Meli")
                    st.metric("Preço de Venda", f"R$ {resultado_ml['preco_de_lista']:.2f}")
                with res_col2:
                    st.markdown("##### Preço Sugerido na Amazon")
                    st.metric("Preço de Venda", f"R$ {resultado_amazon['preco_de_lista']:.2f}")
                    
st.divider()
hoje = datetime.date.today()
data_formatada = hoje.strftime("%d/%m/%Y")
st.caption(f"Informações sobre taxas atualizadas em {data_formatada}.")
