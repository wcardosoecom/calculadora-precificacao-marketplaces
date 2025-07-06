# engine.py
# Este arquivo centraliza toda a lógica de cálculo para as diferentes plataformas.

# --- CONSTANTES GLOBAIS ---
TAXA_TRANSACAO_SHOPEE = 3.00
COMISSAO_PADRAO_SHOPEE_PERC = 14.0 
ADICIONAL_FRETE_GRATIS_PERC = 6.0
TETO_COMISSAO_PADRAO_SHOPEE = 100.00

# --- FUNÇÕES AUXILIARES DE CÁLCULO ---
def obter_taxa_fixa_meli(preco):
    if preco < 12.50: return 0.00
    elif preco < 29.00: return 6.25
    elif preco < 50.00: return 6.50
    elif preco < 79.00: return 6.75
    else: return 0.0

def obter_tarifa_dba_amazon(preco):
    if preco < 30.00: return 4.50
    elif preco < 79.00: return 8.00
    else: return 0.0

# --- FUNÇÃO PRINCIPAL DE CÁLCULO (REESTRUTURADA) ---
def calcular_preco(plataforma, dados_base, metodo_calculo, promocao_percentual, **kwargs):
    resultado = {
        'preco_de_lista': 0, 'preco_efetivo': 0, 'erro': None,
        # Inicializa todos os campos possíveis para evitar erros
        'taxa_fixa_aplicada': 0, 'custo_frete_gratis_aplicado': 0, 'valor_comissao_ml': 0,
        'valor_imposto': 0, 'valor_custo_unitario': 0, 'valor_lucro_liquido': 0,
        'valor_desconto': 0, 'margem_bruta': 0, 'taxa_transacao_aplicada': 0,
        'comissao_padrao_aplicada': 0, 'adicional_frete_aplicado': 0,
        'tarifa_dba_unidade': 0, 'custo_frete_dba_aplicado': 0, 'valor_comissao_amazon': 0,
    }
    
    if promocao_percentual >= 100:
        resultado['erro'] = 'O desconto não pode ser de 100% ou mais.'
        return resultado
        
    preco_efetivo = 0
    denominador_desconto = 1 - (promocao_percentual / 100)

    # =================================================================
    # LÓGICA PARA MERCADO LIVRE
    # =================================================================
    if plataforma == "Mercado Livre":
        if metodo_calculo == "Percentual sobre a Venda (Margem)":
            lucro_desejado = kwargs.get('lucro_desejado_percentual', 0)
            soma_percentuais = (dados_base['taxa_ml_percentual'] + dados_base['imposto_percentual'] + dados_base['custo_unitario_percentual'] + lucro_desejado)
            if soma_percentuais >= 100:
                resultado['erro'] = f"A soma dos percentuais ({soma_percentuais:.2f}%) é 100% ou mais."
                return resultado
            denominador = 1 - (soma_percentuais / 100)
            custos_base = dados_base['preco_custo']
            taxa_fixa_real = obter_taxa_fixa_meli((custos_base + 6.50) / denominador)
            if (custos_base + taxa_fixa_real) / denominador >= 79:
                preco_efetivo = (custos_base + dados_base['custo_frete_gratis']) / denominador
                resultado['custo_frete_gratis_aplicado'] = dados_base['custo_frete_gratis']
            else:
                preco_efetivo = (custos_base + taxa_fixa_real) / denominador
                resultado['taxa_fixa_aplicada'] = taxa_fixa_real
            resultado['valor_imposto'] = preco_efetivo * (dados_base['imposto_percentual'] / 100)
            resultado['valor_custo_unitario'] = preco_efetivo * (dados_base['custo_unitario_percentual'] / 100)
            resultado['valor_lucro_liquido'] = preco_efetivo * (lucro_desejado / 100)
        
        elif metodo_calculo == "Índice Markup sobre o Custo":
            markup = kwargs.get('markup_indice', 1)
            denominador_comissao = 1 - (dados_base['taxa_ml_percentual'] / 100)
            custos_base = dados_base['preco_custo']
            preco_provisorio = (custos_base * markup) / denominador_comissao
            taxa_fixa_real = obter_taxa_fixa_meli(preco_provisorio)
            if preco_provisorio >= 79:
                preco_efetivo = ((custos_base + dados_base['custo_frete_gratis']) * markup) / denominador_comissao
                resultado['custo_frete_gratis_aplicado'] = dados_base['custo_frete_gratis']
            else:
                preco_efetivo = ((custos_base + taxa_fixa_real) * markup) / denominador_comissao
                resultado['taxa_fixa_aplicada'] = taxa_fixa_real
        
        resultado['valor_comissao_ml'] = preco_efetivo * (dados_base['taxa_ml_percentual'] / 100)

    # =================================================================
    # LÓGICA PARA SHOPEE
    # =================================================================
    elif plataforma == "Shopee":
        resultado['taxa_transacao_aplicada'] = TAXA_TRANSACAO_SHOPEE
        comissao_total_perc = COMISSAO_PADRAO_SHOPEE_PERC
        if dados_base['participa_frete_gratis']:
            comissao_total_perc += ADICIONAL_FRETE_GRATIS_PERC
        if metodo_calculo == "Percentual sobre a Venda (Margem)":
            lucro_desejado = kwargs.get('lucro_desejado_percentual', 0)
            soma_percentuais = (comissao_total_perc + dados_base['imposto_percentual'] + dados_base['custo_unitario_percentual'] + lucro_desejado)
            if soma_percentuais >= 100:
                resultado['erro'] = f"A soma dos percentuais ({soma_percentuais:.2f}%) é 100% ou mais."
                return resultado
            denominador = 1 - (soma_percentuais / 100)
            preco_provisorio = (dados_base['preco_custo'] + TAXA_TRANSACAO_SHOPEE) / denominador
        else: # Markup
            denominador = 1 - (comissao_total_perc / 100)
            preco_provisorio = ((dados_base['preco_custo'] + TAXA_TRANSACAO_SHOPEE) * kwargs.get('markup_indice', 1)) / denominador

        comissao_base_calc = preco_provisorio * (COMISSAO_PADRAO_SHOPEE_PERC / 100)
        if comissao_base_calc <= TETO_COMISSAO_PADRAO_SHOPEE:
            preco_efetivo = preco_provisorio
            resultado['comissao_padrao_aplicada'] = comissao_base_calc
            if dados_base['participa_frete_gratis']:
                resultado['adicional_frete_aplicado'] = preco_efetivo * (ADICIONAL_FRETE_GRATIS_PERC / 100)
        else:
            resultado['comissao_padrao_aplicada'] = TETO_COMISSAO_PADRAO_SHOPEE
            adicional_frete_perc = ADICIONAL_FRETE_GRATIS_PERC if dados_base['participa_frete_gratis'] else 0
            if metodo_calculo == "Percentual sobre a Venda (Margem)":
                lucro_desejado = kwargs.get('lucro_desejado_percentual', 0)
                soma_perc_sem_comissao = (adicional_frete_perc + dados_base['imposto_percentual'] + dados_base['custo_unitario_percentual'] + lucro_desejado)
                denominador_recalc = 1 - (soma_perc_sem_comissao / 100)
                preco_efetivo = (dados_base['preco_custo'] + TAXA_TRANSACAO_SHOPEE + TETO_COMISSAO_PADRAO_SHOPEE) / denominador_recalc
            else: # Markup
                denominador_recalc = 1 - (adicional_frete_perc / 100)
                preco_efetivo = ((dados_base['preco_custo'] + TAXA_TRANSACAO_SHOPEE + TETO_COMISSAO_PADRAO_SHOPEE) * kwargs.get('markup_indice', 1)) / denominador_recalc
            if dados_base['participa_frete_gratis']:
                resultado['adicional_frete_aplicado'] = preco_efetivo * (ADICIONAL_FRETE_GRATIS_PERC / 100)
        
        # BLOCO DE CÁLCULO FALTANTE ADICIONADO AQUI
        if metodo_calculo == "Percentual sobre a Venda (Margem)":
            lucro_desejado = kwargs.get('lucro_desejado_percentual', 0)
            resultado['valor_imposto'] = preco_efetivo * (dados_base['imposto_percentual'] / 100)
            resultado['valor_custo_unitario'] = preco_efetivo * (dados_base['custo_unitario_percentual'] / 100)
            resultado['valor_lucro_liquido'] = preco_efetivo * (lucro_desejado / 100)
    
    # =================================================================
    # LÓGICA PARA AMAZON
    # =================================================================
    elif plataforma == "Amazon":
        if metodo_calculo == "Percentual sobre a Venda (Margem)":
            lucro_desejado = kwargs.get('lucro_desejado_percentual', 0)
            soma_percentuais = (dados_base['comissao_amazon_percentual'] + dados_base['imposto_percentual'] + dados_base['custo_unitario_percentual'] + lucro_desejado)
            denominador = 1 - (soma_percentuais / 100)
            custos_base = dados_base['preco_custo']
            tarifa_real = obter_tarifa_dba_amazon((custos_base + 8.00) / denominador)
            if (custos_base + tarifa_real) / denominador >= 79:
                preco_efetivo = (custos_base + dados_base['custo_frete_dba']) / denominador
                resultado['custo_frete_dba_aplicado'] = dados_base['custo_frete_dba']
            else:
                preco_efetivo = (custos_base + tarifa_real) / denominador
                resultado['tarifa_dba_unidade'] = tarifa_real
            
            # BLOCO DE CÁLCULO FALTANTE ADICIONADO AQUI
            resultado['valor_imposto'] = preco_efetivo * (dados_base['imposto_percentual'] / 100)
            resultado['valor_custo_unitario'] = preco_efetivo * (dados_base['custo_unitario_percentual'] / 100)
            resultado['valor_lucro_liquido'] = preco_efetivo * (lucro_desejado / 100)
        else: # Markup
            denominador_comissao = 1 - (dados_base['comissao_amazon_percentual'] / 100)
            custos_base = dados_base['preco_custo']
            preco_provisorio = (custos_base * kwargs.get('markup_indice', 1)) / denominador_comissao
            tarifa_real = obter_tarifa_dba_amazon(preco_provisorio)
            if preco_provisorio >= 79:
                preco_efetivo = ((custos_base + dados_base['custo_frete_dba']) * kwargs.get('markup_indice', 1)) / denominador_comissao
                resultado['custo_frete_dba_aplicado'] = dados_base['custo_frete_dba']
            else:
                preco_efetivo = ((custos_base + tarifa_real) * kwargs.get('markup_indice', 1)) / denominador_comissao
                resultado['tarifa_dba_unidade'] = tarifa_real

    # --- FINALIZAÇÃO COMUM A TODOS ---
    preco_de_lista = preco_efetivo / denominador_desconto
    resultado.update({
        'preco_de_lista': preco_de_lista, 'preco_efetivo': preco_efetivo,
        'valor_desconto': preco_de_lista - preco_efetivo
    })

    # Cálculo da margem bruta no final, após todos os custos serem definidos
    custos_plataforma = (resultado.get('valor_comissao_ml',0) + resultado.get('taxa_fixa_aplicada',0) + resultado.get('custo_frete_gratis_aplicado',0) +
                         resultado.get('comissao_padrao_aplicada',0) + resultado.get('adicional_frete_aplicado',0) + resultado.get('taxa_transacao_aplicada',0) +
                         resultado.get('valor_comissao_amazon',0) + resultado.get('tarifa_dba_unidade',0) + resultado.get('custo_frete_dba_aplicado',0))
    
    resultado['margem_bruta'] = preco_efetivo - dados_base['preco_custo'] - custos_plataforma - resultado.get('valor_custo_unitario', 0)
    
    return resultado
