import random
import time
import requests


def btc_para_decimal(valor_btc_str):
    if valor_btc_str == "0 BTC" or not valor_btc_str: # Adicionado checagem para string vazia ou None
        return 0.0
    try:
        return float(valor_btc_str.replace(" BTC", ""))
    except ValueError: # Adicionado tratamento de erro para conversão float
        print(f"Aviso: Não foi possível converter '{valor_btc_str}' para decimal. Retornando 0.0.")
        return 0.0


def decimal_para_btc(valor_float):
    if valor_float < 0: # Evitar valores negativos
        valor_float = 0.0
    return f"{valor_float:.8f}".rstrip('0').rstrip('.') + " BTC"


def exibe_pergunta(pergunta_atual, numero_pergunta):
    print(f"\n--- Pergunta {numero_pergunta} (Dificuldade: {pergunta_atual['nivel_dificuldade'].capitalize()}) ---")
    print(pergunta_atual["text"])

    embaralha_opcao = list(pergunta_atual["options"])
    random.shuffle(embaralha_opcao)

    # Garante que a resposta correta ainda seja encontrada após o embaralhamento
    opcao_correta_atual = embaralha_opcao.index(pergunta_atual["correct_answer"])

    for indice_opcoes, texto_opcoes in enumerate(embaralha_opcao):
        print(f"{chr(65 + indice_opcoes)}) {texto_opcoes}")

    return embaralha_opcao, opcao_correta_atual


def respostas_dadas(pergunta_da_rodada, progresso_jogo):
    while True:
        # Passar a pergunta atual e o número da pergunta para a função de exibição
        opcoes_da_rodada, posicao_correta_apos_sorteio = exibe_pergunta(pergunta_da_rodada, progresso_jogo + 1)

        pega_resposta = input("Sua resposta (A, B, C, D), 'P' para Pular ou 'D' para Desistir: ").upper()
        if pega_resposta in ['A', 'B', 'C', 'D', 'P', 'D']:
            return pega_resposta, opcoes_da_rodada, posicao_correta_apos_sorteio
        else:
            print("Valor inválido! Por favor, digite A, B, C, D, 'P' ou 'D'.")


def checa_resposta(resposta_marcada, posicao_correta_apos_sorteio):
    mapeia_respostas = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    # Retorna True se a resposta marcada corresponde à posição correta
    return mapeia_respostas.get(resposta_marcada) == posicao_correta_apos_sorteio


def atualiza_premio(guarda_nivel):
    valor_premios = [
        "0.1 BTC", "0.2 BTC", "0.3 BTC", "0.4 BTC", "0.5 BTC",
        "0.6 BTC", "0.7 BTC", "0.8 BTC", "0.9 BTC", "1 BTC"
    ]
    if 0 <= guarda_nivel < len(valor_premios):
        return valor_premios[guarda_nivel]
    return "0 BTC" # Retorna "0 BTC" se o nível estiver fora do alcance


def regras():
    print("                                                                   ")
    print(" Bem vindo(a) ao show do Bitcoin! Vamos testar seus conhecimentos! ")
    print("                                                                   ")
    print(" ------------------------- REGRAS DO JOGO ------------------------- ")
    print("                                                                   ")
    print(" Objetivo: Acertar todas as perguntas até o prêmio final, 1 Bitcoin ")
    print(" Perguntas: Cada uma possui 4 alternativas e apenas uma está correta")
    print(" Pulos: Você tem 3 pulos. Ao usá-los o prêmio não avança e outra    ")
    print(" pergunta de mesmo nível de dificuldade será apresentada           ")
    print(" Desistir: Ao desistir, o prêmio será 50% do valor acumulado        ")
    print(" Erros: O jogo vai acabar e você receberá 10% do valor acumulado    ")
    print(" Cálculo: O jogo começa em 0 BTC e vai até 1.0 BTC, aumentando 0.1 a")
    print(" cada pergunta até o final                                         ")
    print(" Escolha: Ao selecionar a opção desejada, digite o valor referente  ")
    print(" Controles: Pressione A, B, C ou D para selecionar a opção desejada,")
    print(" letra 'D' para desistir do jogo ou 'P' para pular a pergunta      ")
    print("                                                                   ")
    print("------- ATENÇÃO: ESTE GAME PRECISA DE CONEXÃO COM A INTERNET -------")
    print("                                                                   ")
    input("------------ Pressione ENTER para começar, e boa sorte! ------------")


def get_token():
    try:
        response = requests.get('https://tryvia.ptr.red/api_token.php?command=request', timeout=5) # Adicionado timeout
        response.raise_for_status()  # Levanta HTTPError para 4xx/5xx respostas
        data = response.json()
        if data.get("response_code") != 0:
            print(f"Erro ao obter token da API: Código {data.get('response_code')} - {data.get('response')}")
            return None
        return data.get("token")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao obter token: {e}")
        return None
    except ValueError as e:
        print(f"Erro ao decodificar JSON do token: {e}")
        return None


def get_questions_from_api(token, qtd_questions, difficulty=None):
    params = {
        'amount': qtd_questions,
        'category': 9, # Definindo a categoria para 'General Knowledge' (ID 9) para ter mais chances de perguntas
        'type': 'multiple',
        'token': token
    }
    if difficulty and difficulty != "null" and difficulty != "0":
        params['difficulty'] = difficulty

    try:
        response = requests.get('https://tryvia.ptr.red/api.php', params=params, timeout=10) # Adicionado timeout
        response.raise_for_status()
        data = response.json()
        if data.get("response_code") != 0:
            print(f"Erro ao obter perguntas da API: Código {data.get('response_code')} - {data.get('response')}")
            return [] # Retorna lista vazia em caso de erro na API
        results = data.get("results")
        if not isinstance(results, list): # Garante que 'results' é uma lista
            print(f"Aviso: Formato inesperado para 'results' da API: {type(results)}. Esperado lista.")
            return []
        return results
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao obter perguntas: {e}")
        return []
    except ValueError as e:
        print(f"Erro ao decodificar JSON das perguntas: {e}")
        return []


def baixa_perguntas():
    print("\nTentando baixar as perguntas do jogo...")

    session_token = get_token()
    if not session_token:
        print("Não foi possível obter o token da API. Impossível baixar perguntas.")
        return None

    # Ajustado para pedir mais perguntas do que o necessário, para garantir a quantidade
    # e ter uma pool maior para randomizar e evitar repetições em pulos
    total_perguntas_por_dificuldade = {
        'easy': 6, # Pede mais para ter opções de pulo
        'medium': 5,
        'hard': 5
    }

    perguntas_do_jogo_raw = {
        "easy": [],
        "medium": [],
        "hard": []
    }

    print("Baixando perguntas fáceis...")
    faceis = get_questions_from_api(session_token, total_perguntas_por_dificuldade['easy'], 'easy')
    perguntas_do_jogo_raw["easy"].extend(faceis)

    print("Baixando perguntas médias...")
    medias = get_questions_from_api(session_token, total_perguntas_por_dificuldade['medium'], 'medium')
    perguntas_do_jogo_raw["medium"].extend(medias)

    print("Baixando perguntas difíceis...")
    dificeis = get_questions_from_api(session_token, total_perguntas_por_dificuldade['hard'], 'hard')
    perguntas_do_jogo_raw["hard"].extend(dificeis)

    if not any(perguntas_do_jogo_raw.values()): # Verifica se há perguntas em qualquer nível
        print("Erro: Nenhuma pergunta foi baixada com sucesso. Verifique sua conexão ou a API.")
        return None

    formatted_questions_by_difficulty = {
        "easy": [],
        "medium": [],
        "hard": []
    }

    for difficulty, raw_questions in perguntas_do_jogo_raw.items():
        for q in raw_questions:
            # Decodifica entidades HTML se necessário (a API Open Trivia DB usa)
            question_text = requests.utils.unquote(q.get("question", "")).replace("&quot;", "\"").replace("&#039;", "'").replace("&amp;", "&")
            correct_answer = requests.utils.unquote(q.get("correct_answer", "")).replace("&quot;", "\"").replace("&#039;", "'").replace("&amp;", "&")
            incorrect_answers_raw = q.get("incorrect_answers", [])

            incorrect_answers = []
            if isinstance(incorrect_answers_raw, list):
                for ans in incorrect_answers_raw:
                    incorrect_answers.append(requests.utils.unquote(ans).replace("&quot;", "\"").replace("&#039;", "'").replace("&amp;", "&"))
            else:
                print(f"Aviso: 'incorrect_answers' não é uma lista para a pergunta: {question_text}")

            options = incorrect_answers + [correct_answer]
            random.shuffle(options)

            formatted_questions_by_difficulty[difficulty].append({
                "text": question_text,
                "options": options,
                "correct_answer": correct_answer,
                "nivel_dificuldade": difficulty # Já está normalizado para 'easy', 'medium', 'hard'
            })
    
    total_baixadas = sum(len(q_list) for q_list in formatted_questions_by_difficulty.values())
    print(f"Perguntas baixadas e formatadas com sucesso! Total: {total_baixadas}")

    return formatted_questions_by_difficulty


def inicia_jogo(banco_de_perguntas_por_dificuldade):
    regras()

    print("\nInício do Jogo!")
    print("Responda corretamente as perguntas para ganhar até 1 BTC!")
    print("Você pode digitar 'P' para pular a pergunta ou 'D' para Desistir da partida a qualquer momento.")

    if not banco_de_perguntas_por_dificuldade or all(not lst for lst in banco_de_perguntas_por_dificuldade.values()):
        print("\nNão há perguntas para iniciar o jogo. Encerrando.")
        return

    # Sequência de dificuldade desejada
    # Prioriza ter pelo menos uma de cada tipo antes de repetir
    sequencia_minima = []
    for _ in range(min(len(banco_de_perguntas_por_dificuldade['easy']), 4)):
        sequencia_minima.append('easy')
    for _ in range(min(len(banco_de_perguntas_por_dificuldade['medium']), 3)):
        sequencia_minima.append('medium')
    for _ in range(min(len(banco_de_perguntas_por_dificuldade['hard']), 3)):
        sequencia_minima.append('hard')
    
    # Se ainda faltam perguntas para chegar a 10 (ou o máximo de perguntas baixadas),
    # adiciona mais do nível de dificuldade mais fácil disponível
    if len(sequencia_minima) < 10:
        dificuldades_para_completar = []
        if len(banco_de_perguntas_por_dificuldade['easy']) > len([s for s in sequencia_minima if s == 'easy']):
            dificuldades_para_completar.extend(['easy'] * (len(banco_de_perguntas_por_dificuldade['easy']) - len([s for s in sequencia_minima if s == 'easy'])))
        if len(banco_de_perguntas_por_dificuldade['medium']) > len([s for s in sequencia_minima if s == 'medium']):
            dificuldades_para_completar.extend(['medium'] * (len(banco_de_perguntas_por_dificuldade['medium']) - len([s for s in sequencia_minima if s == 'medium'])))
        if len(banco_de_perguntas_por_dificuldade['hard']) > len([s for s in sequencia_minima if s == 'hard']):
            dificuldades_para_completar.extend(['hard'] * (len(banco_de_perguntas_por_dificuldade['hard']) - len([s for s in sequencia_minima if s == 'hard'])))
        
        random.shuffle(dificuldades_para_completar)
        sequencia_final = sequencia_minima + dificuldades_para_completar
        sequencia_final = sequencia_final[:10] # Limita a 10 perguntas no máximo
    else:
        sequencia_final = sequencia_minima[:10]

    maximo_perguntas = len(sequencia_final)
    if maximo_perguntas == 0:
        print("Não há perguntas suficientes para iniciar o jogo. Por favor, tente novamente mais tarde.")
        return

    acumula_premio = "0 BTC"
    progresso_jogo = 0
    pulos_usados = 0
    perguntas_usadas_ids = set() # Usar IDs únicos ou hashes para evitar repetição exata da pergunta

    while progresso_jogo < maximo_perguntas:
        dificuldade_atual = sequencia_final[progresso_jogo]

        # Filtra perguntas disponíveis que ainda não foram usadas
        perguntas_disponiveis_rodada = [
            q for q in banco_de_perguntas_por_dificuldade[dificuldade_atual]
            if id(q) not in perguntas_usadas_ids # Usar id() do objeto para garantir unicidade
        ]

        if not perguntas_disponiveis_rodada:
            print(f"\nNão há mais perguntas novas disponíveis para o nível {dificuldade_atual.capitalize()}.")
            print("Tentando avançar para a próxima pergunta da sequência, se houver...")
            progresso_jogo += 1 # Tenta a próxima dificuldade na sequência
            continue # Reinicia o loop para pegar a próxima pergunta

        pergunta_da_rodada = random.choice(perguntas_disponiveis_rodada)
        
        premio_desiste_float = btc_para_decimal(acumula_premio) * 0.50
        premio_desiste = decimal_para_btc(premio_desiste_float)

        premio_erro_float = btc_
