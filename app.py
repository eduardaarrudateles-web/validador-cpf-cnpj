import streamlit as st
import pandas as pd
import re
import io

# 1. A Matemática do Robô (O Motor)
def validar_documento(doc):
    if pd.isna(doc):
        return "Inválido (Em Branco)"
    doc_limpo = re.sub(r'[^0-9]', '', str(doc))

    if len(doc_limpo) == 11:
        if doc_limpo == doc_limpo[0] * 11: return "CPF Incorreto"
        soma_1 = sum(int(doc_limpo[i]) * (10 - i) for i in range(9))
        digito_1 = (soma_1 * 10 % 11) % 10
        soma_2 = sum(int(doc_limpo[i]) * (11 - i) for i in range(10))
        digito_2 = (soma_2 * 10 % 11) % 10
        return "CPF Correto" if doc_limpo[-2:] == f"{digito_1}{digito_2}" else "CPF Incorreto"

    elif len(doc_limpo) == 14:
        if doc_limpo == doc_limpo[0] * 14: return "CNPJ Incorreto"
        pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma_1 = sum(int(doc_limpo[i]) * pesos_1[i] for i in range(12))
        digito_1 = 0 if (soma_1 % 11) < 2 else 11 - (soma_1 % 11)
        soma_2 = sum(int(doc_limpo[i]) * pesos_2[i] for i in range(13))
        digito_2 = 0 if (soma_2 % 11) < 2 else 11 - (soma_2 % 11)
        return "CNPJ Correto" if doc_limpo[-2:] == f"{digito_1}{digito_2}" else "CNPJ Incorreto"
    else:
        return f"Tamanho Inválido ({len(doc_limpo)} dígitos)"

# 2. A Interface Visual do Site (O que as pessoas vão ver)
st.set_page_config(page_title="Validador Fiscal", page_icon="📊")

st.title("📊 Robô de Auditoria: CPF e CNPJ")
st.write("Faça o upload da sua planilha para validar a estrutura dos documentos e higienizar a base de dados.")

# Caixinha para a pessoa arrastar a planilha
arquivo_subido = st.file_uploader("Escolha sua planilha do Excel (.xlsx)", type=["xlsx"])

# O que acontece DEPOIS que a pessoa coloca o arquivo
if arquivo_subido is not None:
    st.info("Planilha carregada! Analisando os dados...")
    df = pd.read_excel(arquivo_subido)
    
    # Pergunta em qual coluna estão os dados
    coluna = st.selectbox("Selecione qual coluna contém os CPFs/CNPJs:", df.columns)
    
    # Botão de iniciar
    if st.button("Iniciar Validação"):
        with st.spinner('O robô está trabalhando nas contas...'):
            df['Status_Validacao'] = df[coluna].apply(validar_documento)
            
            st.success("Validação concluída com sucesso!")
            
            # Prepara o arquivo para a pessoa baixar
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            
            # Botão de Download
            st.download_button(
                label="📥 Baixar Relatório Validado",
                data=buffer.getvalue(),
                file_name="base_higienizada.xlsx",
                mime="application/vnd.ms-excel"
            )