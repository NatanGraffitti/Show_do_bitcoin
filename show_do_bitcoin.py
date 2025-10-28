import random
import requests

def btc_para_decimal(valor_btc_str):
    if valor_btc_str == "0 BTC":
        return 0.0
    return float(valor_btc_str.replace(" BTC", ""))

def decimal_para_btc(valor_float):
    return f"{valor_float:.8f}".rstrip('0').rstrip('.') + " BTC"

def exibe_pergunta(pergunta_atual, numero_pergunta):
    print(f"\n--- Pergunta {numero_pergunta} (Dificuldade: {pergunta_atual['nivel_dificuldade'].capitalize()}) ---")
    print(pergunta_atual["text"])

    embaralha_opcao = list(pergunta_atual["options"])
    random.shuffle(embaralha_opcao)

    opcao_correta_atual = embaralha_opcao.index(pergunta_atual["correct_answer"])

    for indice_opcoes, texto_opcoes in enumerate(embaralha_opcao):
        print(f"{chr(65 + indice_opcoes)}) {texto_opcoes}")
    
    return embaralha_opcao, opcao_correta_atual

def respostas_dadas(pergunta_da_rodada, progresso_jogo):
    while True:
        opcoes_da_rodada, posicao_correta_apos_sorteio = exibe_pergunta(pergunta_da_rodada, progresso_jogo + 1)
        pega_resposta = input("Sua resposta (A, B, C, D), 'P' para Pular ou 'D' para Desistir: ").upper()
        if pega_resposta in ['A', 'B', 'C', 'D', 'P', 'D']:
            return pega_resposta, opcoes_da_rodada, posicao_correta_apos_sorteio
        else:
            print("Valor inválido! Por favor, digite A, B, C, D, 'P' ou 'D'.")

def checa_resposta(resposta_marcada, posicao_correta_apos_sorteio):
    mapeia_respostas = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    if mapeia_respostas.get(resposta_marcada) == posicao_correta_apos_sorteio:
        return True
    else:
        return False

def atualiza_premio(guarda_nivel):
    valor_premios = [
        "0.1 BTC",
        "0.2 BTC",
        "0.3 BTC",
        "0.4 BTC",
        "0.5 BTC",
        "0.6 BTC",
        "0.7 BTC",
        "0.8 BTC",
        "0.9 BTC",
        "1 BTC"
    ]
    if 0 <= guarda_nivel < len(valor_premios):
        return valor_premios[guarda_nivel]
    return "0 BTC"

def regras():
    print("                                                                     ")
    print(" Bem vindo(a) ao show do Bitcoin! Vamos testar seus conhecimentos! ")
    print("                                                                     ")
    print(" ------------------------- REGRAS DO JOGO ------------------------- ")
    print("                                                                     ")
    print(" Objetivo: Acertar todas as perguntas até o prêmio final, 1 Bitcoin ")
    print(" Perguntas: Cada uma possui 4 alternativas e apenas uma está correta")
    print(" Pulos: Você tem 3 pulos. Ao usá-los o prêmio não avança e outra   ")
    print(" pergunta de mesmo nível de dificuldade será apresentada           ")
    print(" Desistir: Ao desistir, o prêmio será 50% do valor acumulado       ")
    print(" Erros: O jogo vai acabar e você receberá 10% do valor acumulado   ")
    print(" Cálculo: O jogo começa em 0 BTC e vai até 1.0 BTC, aumentando 0.1 a")
    print(" cada pergunta até o final                                         ")
    print(" Escolha: Ao selecionar a opção desejada, digite o valor referente ")
    print(" Controles: Pressione A, B, C ou D para selecionar a opção desejada,")
    print(" letra 'D' para desistir do jogo ou 'P' para pular a pergunta     ")
    print("                                                                     ")
    print("------- ATENÇÃO: ESTE GAME PRECISA DE CONEXÃO COM A INTERNET -------")
    print("                                                                     ")
    input("------------ Pressione ENTER para começar, e boa sorte! ------------")

def get_token():
    try:
        response = requests.get('https://tryvia.ptr.red/api_token.php?command=request')
        response.raise_for_status()
        data = response.json()
        if data.get("response_code") != 0:
            print(f"Erro ao obter token da API: Código {data.get('response_code')}")
            return None
        return data.get("token")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao obter token: {e}")
        return None
    except ValueError as e:
        print(f"Erro ao decodificar JSON do token: {e}")
        return None

def get_questions_from_api(token, qtd_questions, difficulty=None):
    category = 9 

    params = {
        'amount': qtd_questions,
        'category': category,
        'type': 'multiple',
        'token': token
    }
    if difficulty and difficulty != "null" and difficulty != "0":
        params['difficulty'] = difficulty

    try:
        response = requests.get('https://tryvia.ptr.red/api.php', params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("response_code") != 0:
            if data.get("response_code") == 1:
                print(f"Aviso: Nenhuma pergunta encontrada para os parâmetros: {params}")
            else:
                print(f"Erro ao obter perguntas da API: Código {data.get('response_code')}")
            return None
        return data.get("results")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao obter perguntas: {e}")
        return None
    except ValueError as e:
        print(f"Erro ao decodificar JSON das perguntas: {e}")
        return None

def baixa_perguntas():
    print("\nTentando baixar as perguntas do jogo...")
    
    session_token = get_token()
    if not session_token:
        print("Não foi possível obter o token da API. Impossível baixar perguntas.")
        return None

    total_de_perguntas_necessarias = 10 
    
    perguntas_do_jogo = [] 
    
    print("Baixando perguntas fáceis...")
    perguntas_faceis = get_questions_from_api(session_token, 4, 'easy')
    if perguntas_faceis:
        perguntas_do_jogo.extend(perguntas_faceis)
    else:
        print("Aviso: Não foi possível obter perguntas fáceis. O jogo pode ter menos perguntas.")

    print("Baixando perguntas médias...")
    perguntas_medias = get_questions_from_api(session_token, 3, 'medium')
    if perguntas_medias:
        perguntas_do_jogo.extend(perguntas_medias)
    else:
        print("Aviso: Não foi possível obter perguntas médias. O jogo pode ter menos perguntas.")

    print("Baixando perguntas difíceis...")
    perguntas_dificeis = get_questions_from_api(session_token, 3, 'hard')
    if perguntas_dificeis:
        perguntas_do_jogo.extend(perguntas_dificeis)
    else:
        print("Aviso: Não foi possível obter perguntas difíceis. O jogo pode ter menos perguntas.")

    if not perguntas_do_jogo:
        print("Erro: Nenhuma pergunta foi baixada com sucesso. Verifique sua conexão ou a API.")
        return None

    formatted_questions = []
    for q in perguntas_do_jogo:
        question_text = q.get("question", q.get("text"))
        
        incorrect_answers = q.get("incorrect_answers", [])
        if not isinstance(incorrect_answers, list):
            incorrect_answers = [] 
        
        options = incorrect_answers + [q["correct_answer"]]
        random.shuffle(options)
        
        formatted_questions.append({
            "text": question_text,
            "options": options,
            "correct_answer": q["correct_answer"],
            "nivel_dificuldade": q["difficulty"],
            "foi_pulada": False 
        })
    
    if len(formatted_questions) < total_de_perguntas_necessarias:
        print(f"Aviso: Apenas {len(formatted_questions)} perguntas foram baixadas. O jogo terá menos rodadas.")
    elif len(formatted_questions) > total_de_perguntas_necessarias:
        formatted_questions = formatted_questions[:total_de_perguntas_necessarias]


    print(f"Perguntas baixadas e formatadas com sucesso! Total: {len(formatted_questions)}")
    return formatted_questions

def inicia_jogo(banco_de_perguntas_param):
    regras()

    banco_de_perguntas = banco_de_perguntas_param
    
    if not banco_de_perguntas:
        print("\nNão há perguntas para iniciar o jogo. Encerrando.")
        return

    organiza_dificuldade = {
        "easy": [q for q in banco_de_perguntas if q["nivel_dificuldade"].lower() == "easy"],
        "medium": [q for q in banco_de_perguntas if q["nivel_dificuldade"].lower() == "medium"],
        "hard": [q for q in banco_de_perguntas if q["nivel_dificuldade"].lower() == "hard"]
    }

    
    perguntas_disponiveis_pool = {
        "easy": list(organiza_dificuldade["easy"]),
        "medium
