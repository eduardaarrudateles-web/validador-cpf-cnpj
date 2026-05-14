import pandas as pd
import re

# ==========================================
# 1. O "MOTOR" DO ROBÔ (A Regra Matemática)
# ==========================================
def validar_cpf(cpf):
    # Se a célula estiver vazia na planilha, já marca como inválido
    if pd.isna(cpf):
        return "Inválido (Em Branco)"

    cpf_limpo = re.sub(r'[^0-9]', '', str(cpf))

    if len(cpf_limpo) != 11 or cpf_limpo == cpf_limpo[0] * 11:
        return "Inválido"

    soma_1 = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
    digito_1 = (soma_1 * 10 % 11) % 10

    soma_2 = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
    digito_2 = (soma_2 * 10 % 11) % 10

    if cpf_limpo[-2:] == f"{digito_1}{digito_2}":
        return "Correto"
    else:
        return "Incorreto"

# ==========================================
# 2. CONFIGURAÇÕES DA SUA PLANILHA
# ==========================================
arquivo_entrada = 'base_entrada.xlsx'        # Nome da planilha que o robô vai ler
arquivo_saida = 'resultado_final.xlsx'       # Nome da planilha que o robô vai gerar

coluna_do_cpf = 'CPF'                        # Nome exato do cabeçalho onde estão os números
coluna_do_status = 'Status_Validacao'        # Nome exato do cabeçalho que o robô vai preencher

# ==========================================
# 3. EXECUÇÃO DO FLUXO (Leitura -> Preenchimento -> Geração)
# ==========================================
print(f"Lendo o arquivo '{arquivo_entrada}'...")

try:
    # Passo A: O robô abre a planilha de entrada
    df = pd.read_excel(arquivo_entrada)
    
    # Passo B: O robô vai na coluna de status e preenche linha por linha
    # Nota: Se a coluna 'Status_Validacao' não existir na sua planilha original, 
    # o pandas a cria automaticamente neste momento.
    print("Analisando a matemática dos CPFs...")
    df[coluna_do_status] = df[coluna_do_cpf].apply(validar_cpf)
    
    # Passo C: O robô gera o arquivo de resultado final
    df.to_excel(arquivo_saida, index=False)
    
    print(f"Sucesso! O processo terminou. Abra o arquivo '{arquivo_saida}' para ver o resultado.")

except FileNotFoundError:
    print(f"ERRO: Não encontrei o arquivo '{arquivo_entrada}'. Ele está na mesma pasta do script?")
except KeyError:
    print(f"ERRO: Não encontrei a coluna '{coluna_do_cpf}' na sua planilha. Verifique como está escrito no cabeçalho do Excel.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")