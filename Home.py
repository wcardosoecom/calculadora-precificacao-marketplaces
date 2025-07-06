# Home.py
import streamlit as st

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(
    page_title="Home | Calculadora de Precificação",
    page_icon="🏠",
    layout="wide"
)

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.title("Precificação para Marketplaces")
st.sidebar.markdown("---")
st.sidebar.markdown("Powered by William Cardoso")


# --- CSS CUSTOMIZADO PARA OS CARTÕES CLICÁVEIS ---
st.markdown("""
<style>
    a:link, a:visited {
        text-decoration: none;
        color: white;
    }
    a:hover, a:active {
        text-decoration: none;
        color: #f8c22c; 
    }
    .logo-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        border-radius: 10px;
        background-color: #262730; 
        transition: transform 0.2s, box-shadow 0.2s;
        height: 220px;
        border: 1px solid #444;
    }
    .logo-card:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        border-color: #f8c22c;
    }
    .logo-card img {
        max-height: 100px;
        margin-bottom: 20px;
        background-color: white;
        border-radius: 5px;
        padding: 5px;
    }
    .logo-card p {
        font-size: 1.2em;
        font-weight: bold;
        margin: 0;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# --- CONTEÚDO PRINCIPAL ---
st.title("Calculadora de Preço para Marketplaces")
st.markdown("---")

st.subheader("Acesse a Calculadora Desejada:")

# URLs das imagens
meli_logo_url = "https://www.cartacapital.com.br/cupons/img/lojas/logo/mercado-livre.png"
amazon_logo_url = "https://cdn.textstudio.com/output/graphic/preview/large/9/1/0/0/10019_3373a854.webp"
shopee_logo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT0YjQo6kVlPrp2XOAt9bc7MGi9GGkzo7J2YrTJYlt1LQo1k_RCShVfFfAwHqwskS5ry5o&usqp=CAU"

# Links para as páginas
link_meli = "Calculadora_Meli"
link_shopee = "Calculadora_Shopee"
# LINK ATUALIZADO PARA CORRESPONDER AO NOVO NOME DO ARQUIVO
link_amazon = "Calculadora_Amazon" 

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <a href="{link_meli}" target="_self" class="logo-card">
        <img src="{meli_logo_url}" alt="Mercado Livre Logo">
        <p>Mercado Livre</p>
    </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <a href="{link_amazon}" target="_self" class="logo-card">
        <img src="{amazon_logo_url}" alt="Amazon Logo">
        <p>Amazon</p>
    </a>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <a href="{link_shopee}" target="_self" class="logo-card">
        <img src="{shopee_logo_url}" alt="Shopee Logo">
        <p>Shopee</p>
    </a>
    """, unsafe_allow_html=True)


st.divider()

# Texto de apresentação
st.markdown(
    """
    Diferente das calculadoras disponibilizadas pelas plataformas, essa permite considerar aspectos internos 
    para definir o preço final de qualquer anúncio: impostos, custos da empresa, CMV e markup. 
    Além de incluir um desconto ou cupom no cálculo para encontrar o preço final de qualquer produto.

    Também é possível verificar se um anúncio antigo é lucrativo ou está gerando prejuízo, através do seu 
    preço de venda atual. A atualização dos custos é feita de forma automática, de acordo com as informações 
    de taxas e comissões disponibilizadas pelas plataformas na página oficial ou via API.
    """
)

# Seção de contato
st.markdown(
    """
    ### Fale Comigo
    - 👨‍💻 [Desenvolvedor](https://www.linkedin.com/in/william-cardoso-ecom) = William Cardoso
    """
)