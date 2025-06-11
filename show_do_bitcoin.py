import random														                                                                        #import para embaralhar as perguntas														
import requests														                                                                        #import das perguntas para a API

def btc_para_decimal(valor_btc_str): 																	        							#converte string para decimal
    if valor_btc_str == "0 BTC":																				        					#para calcular o premio	
        return 0.0																								                       		#remove BTC para nao dar problema
    return float(valor_btc_str.replace(" BTC", ""))

def decimal_para_btc(valor_float):																							            	#converte float de volta para strng em formato BTC
    return f"{valor_float:.8f}".rstrip('0').rstrip('.') + " BTC"																			#(formato com 8 casas decimais, sem zero e ponto final			
															                                                                                #volta BTC como complemento depois
def exibe_pergunta(pergunta_atual, numero_pergunta):																						#mostra a pergunta por nivel de dificuldade
    print(f"\n--- Pergunta {numero_pergunta} (Dificuldade: {pergunta_atual['nivel_dificuldade'].capitalize()}) ---")				
    print(pergunta_atual["text"])

    embaralha_opcao = list(pergunta_atual["options"])																						#embaralham a pergunta e as respostas
    random.shuffle(embaralha_opcao)

    opcao_correta_atual = embaralha_opcao.index(pergunta_atual["correct_answer"])

    for indice_opcoes, texto_opcoes in enumerate(embaralha_opcao):
        print(f"{chr(65 + indice_opcoes)}) {texto_opcoes}")
    
    return embaralha_opcao, opcao_correta_atual

def respostas_dadas(pergunta_da_rodada, progresso_jogo):
    while True:
        opcoes_da_rodada, posicao_correta_apos_sorteio = exibe_pergunta(pergunta_da_rodada, progresso_jogo + 1)				                #pede a resposta do jogador, valida se é uma das letras válidas (A,B,C,D,P ou D)
        																																	#e repete o loop ate ser digitada uma opção valida		
        pega_resposta = input("Sua resposta (A, B, C, D), 'P' para Pular ou 'D' para Desistir: ").upper()
        if pega_resposta in ['A', 'B', 'C', 'D', 'P', 'D']:
            return pega_resposta, opcoes_da_rodada, posicao_correta_apos_sorteio
        else:
            print("Valor inválido! Por favor, digite A, B, C, D, 'P' ou 'D'.")

def checa_resposta(resposta_marcada, posicao_correta_apos_sorteio):																			#checa se a resposta selecionada pelo user ta correta
    mapeia_respostas = {'A': 0, 'B': 1, 'C': 2, 'D': 3}																						#mapeia as letras pelo indica numerico e compara se e o mesmo da resposta correta
    if mapeia_respostas.get(resposta_marcada) == posicao_correta_apos_sorteio:
        return True
    else:
        return False

def atualiza_premio(guarda_nivel):																								            #determina o valor do premio atual e aumenta o premio a cada pergunta correta
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
    if 0 <= guarda_nivel < len(valor_premios):																							       #verifica se o nivel esta dentro dos limites da lista, retorna o premio que 
        return valor_premios[guarda_nivel]                                                                                                     #corresponde ao nivel e se nao, retorna nivel invalido
    return "0 BTC"

def regras():																												                   #exibe as regras do jogo			
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

def get_token():														                                                                        #função que comunica com a API			
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

def get_questions_from_api(token, qtd_questions, difficulty=None):									    										#busca perguntas na API com base no token, quantidade e nivel de dificuldade
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
        response = requests.get('https://tryvia.ptr.red/api.php', params=params)																#faz a requisição para obter as perguntas
        response.raise_for_status()
        data = response.json()
        if data.get("response_code") != 0:

            if data.get("response_code") == 1:
                print(f"Aviso: Nenhuma pergunta encontrada para os parâmetros: {params}")							                            #avisa se nao encontrou perguntas
            else:
                print(f"Erro ao obter perguntas da API: Código {data.get('response_code')}")							                        #avisa se tiver erro de conexão
            return None
        return data.get("results")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao obter perguntas: {e}")
        return None
    except ValueError as e:
        print(f"Erro ao decodificar JSON das perguntas: {e}")
        return None

def baixa_perguntas():																													        #função para baixar as perguntas necessarias para cada nivel do jogo
    print("\nTentando baixar as perguntas do jogo...")
    
    session_token = get_token()																												    #tenta obter o token.
    if not session_token:
        print("Não foi possível obter o token da API. Impossível baixar perguntas.")
        return None														 																        #se não conseguir o token, não pode baixar perguntas.

    total_de_perguntas_necessarias = 10 																									    #define quantas perguntas o jogo precisa no total.
    
    perguntas_do_jogo = []													 																    #lista para armazenar as perguntas baixadas.
    															 																				#por nivel de dificuldade
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


    if not perguntas_do_jogo:																													#se nao conseguir baixar printa um erro
        print("Erro: Nenhuma pergunta foi baixada com sucesso. Verifique sua conexão ou a API.")
        return None

    formatted_questions = []																													#formata as perguntas e guarda no padrão do jogo
    for q in perguntas_do_jogo:
        question_text = q.get("question", q.get("text"))
        
        incorrect_answers = q.get("incorrect_answers", [])																						#cria uma lista de respostas incorretas par armazenar e nao repetir
        if not isinstance(incorrect_answers, list):
            incorrect_answers = [] 
        
        options = incorrect_answers + [q["correct_answer"]]																						#junta as incorretas e a correta para embaralhar									
        random.shuffle(options)
        
        formatted_questions.append({																										    #add a formatada a lista
            "text": question_text,
            "options": options,
            "correct_answer": q["correct_answer"],
            "nivel_dificuldade": q["difficulty"],
            "foi_pulada": False 																											    #adiciona a nova chave aqui, inicializada como False
        })
    
    if len(formatted_questions) < total_de_perguntas_necessarias:																				#avisa de vieram menos perguntas q o necessario
        print(f"Aviso: Apenas {len(formatted_questions)} perguntas foram baixadas. O jogo terá menos rodadas.")
    elif len(formatted_questions) > total_de_perguntas_necessarias:																	            #limita o n° de perguntas se baixar mais q o necessario
        formatted_questions = formatted_questions[:total_de_perguntas_necessarias]


    print(f"Perguntas baixadas e formatadas com sucesso! Total: {len(formatted_questions)}")
    return formatted_questions																												    #retorna a lista de perguntas formatadas


# --- Lógica Principal do Jogo ---

def inicia_jogo(banco_de_perguntas_param):																										#apresenta as regras, gerencia o fluxo principal controlando o progresso, premios, pulos e interações
    regras()

    banco_de_perguntas = banco_de_perguntas_param																								#recebe as perguntas baixadas
    
    if not banco_de_perguntas:																												    #se nao tiver as perguntas, termina o jogo com a mensagem
        print("\nNão há perguntas para iniciar o jogo. Encerrando.")
        return

    organiza_dificuldade = {																													#organiza as perguntas por dificuldade
        "easy": [q for q in banco_de_perguntas if q["nivel_dificuldade"].lower() == "easy"],
        "medium": [q for q in banco_de_perguntas if q["nivel_dificuldade"].lower() == "medium"],
        "hard": [q for q in banco_de_perguntas if q["nivel_dificuldade"].lower() == "hard"]
    }

    
    perguntas_disponiveis_pool = {																												#mantém uma cópia das perguntas disponíveis por dificuldade para sorteio. 
        "easy": list(organiza_dificuldade["easy"]),
        "medium": list(organiza_dificuldade["medium"]),
        "hard": list(organiza_dificuldade["hard"])
    }


    dificuldade_nivel_sequencia = (																												#define a sequencia por dificuldade limitando pela quant de perguntas
        ["easy"] * min(4, len(organiza_dificuldade["easy"])) +
        ["medium"] * min(3, len(organiza_dificuldade["medium"])) +
        ["hard"] * min(3, len(organiza_dificuldade["hard"]))
    )
    dificuldade_nivel_sequencia = dificuldade_nivel_sequencia[:len(banco_de_perguntas)]

    acumula_premio = "0 BTC"																													#premio começa em zero, conta quantas perguntas o jogador ja acertou e 
    progresso_jogo = 0																													        #coloca o numero total de perguntas do jogo
    maximo_perguntas = len(dificuldade_nivel_sequencia)

    pergunta_da_rodada = None 																												    #variável para guardar a pergunta atual.
    pulos_usados = 0																														    #conta os pulos usados

    while progresso_jogo < maximo_perguntas:																									#loop principal do jogo, continua enquanto tiver perguntas
        dificuldade_atual = dificuldade_nivel_sequencia[progresso_jogo]																			#pega a dificuldade atual
        	
        perguntas_disponiveis_para_sorteio = [																									#filtra as perguntas que podem ser sorteadas (puladas ou nao na rodada)
            q for q in perguntas_disponiveis_pool[dificuldade_atual]
            if not q.get("foi_pulada", False) and "já_usada_na_rodada" not in q 																#verifica se não foi pulada e não foi usada
        ]

        if not perguntas_disponiveis_para_sorteio:
            print(f"Não há mais perguntas disponíveis para o nível {dificuldade_atual.capitalize()}. Avançando para a próxima rodada ou encerrando...") #se nao tiver mais perguntas disponiveis, para o nivel atual, avança como se a pergunta tivesse sido respondida		
            progresso_jogo += 1													                                                                #pergunta tivesse sido respondida	
            if progresso_jogo >= maximo_perguntas:
                print("Todas as perguntas foram utilizadas ou não há mais perguntas disponíveis em nenhum nível.")				                #avança se tiver sido respondida, encerra se nao
                break																														    #volta o loop para a proxima dificuldade
            continue
        
        if pergunta_da_rodada is None or pergunta_da_rodada.get("foi_pulada", False):							                                #seleciona uma nova pergunta se a anterior foi pulada ou se é a primeira pergunta
            if pergunta_da_rodada and pergunta_da_rodada.get("foi_pulada", False):							
                pergunta_da_rodada["foi_pulada"] = False 										
                if "já_usada_na_rodada" in pergunta_da_rodada:
                    del pergunta_da_rodada["já_usada_na_rodada"]

            nova_pergunta_selecionada = random.choice(perguntas_disponiveis_para_sorteio)														#garante que a nova pergunta seja diferente da última, se aplicável
            nova_pergunta_selecionada["já_usada_na_rodada"] = True 																				#marca como usada para evitar repetição nesta rodada
            pergunta_da_rodada = nova_pergunta_selecionada
        
        premio_desiste_float = btc_para_decimal(acumula_premio) * 0.50																             #calcula os valores dos prêmios de desistência e erro.
        premio_desiste = decimal_para_btc(premio_desiste_float)

        premio_erro_float = btc_para_decimal(acumula_premio) * 0.10																	             #10% se error
        premio_erro = decimal_para_btc(premio_erro_float)
        
        print(f"\n--- Próximo Prêmio ao Acertar: {atualiza_premio(progresso_jogo)} ---")													     #exibe as infos da rodada
        print(f"--- Prêmio se Desistir Agora (50% do Acumulado): {premio_desiste} ---")
        print(f"--- Pulos restantes: {3 - pulos_usados} ---") 

        resposta_marcada, opcoes_da_rodada, posicao_correta_apos_sorteio = respostas_dadas(pergunta_da_rodada, progresso_jogo)					#pega a resposta do jogador

        if resposta_marcada == "D":																												#se pressionar D, marca a pergunta atual como pulada no dicionário dela
            print(f"\nVocê desistiu da partida. Seu prêmio final é: {premio_desiste}")															#pergunta que foi pulada não deve mais ser usada na mesma dificuldade, mas pode ser re-usada 
            break																														        #o nível de dificuldade permanece o mesmo.
        elif resposta_marcada == "P":																											#volta ao início do loop para pegar uma nova pergunta
            if pulos_usados < 3:
                pulos_usados += 1
                print(f"\nVocê pulou a pergunta. Pulos restantes: {3 - pulos_usados}.")
                pergunta_da_rodada["foi_pulada"] = True
                continue 
            else:
                print("\nVocê não tem mais pulos disponíveis! Responda à pergunta ou desista.")													#pede uma nova resposta para a mesma pergunta
                continue 														
        
        if "já_usada_na_rodada" in pergunta_da_rodada:																							#remove a marcação temporária da pergunta, já que ela foi respondida ou descartada.
            del pergunta_da_rodada["já_usada_na_rodada"]

        if checa_resposta(resposta_marcada, posicao_correta_apos_sorteio):																        #se a resposta estiver correta
            acumula_premio = atualiza_premio(progresso_jogo)																	                #atualiza o premio acumulada
            print(f"Parabéns! Resposta correta! Você agora tem: {acumula_premio}")
            
            if acumula_premio == "1 BTC":																										#se atingiu o premio maximo
                print("\nVOCÊ ALCANÇOU O PRÊMIO MÁXIMO! PARABÊNS, VOCÊ GANHOU 1 BTC!")
                break														                                                                    #encerra o jogo
            
            progresso_jogo += 1 																												#avança para a próxima pergunta/nível
            pergunta_da_rodada = None 																											#reseta para garantir que uma nova pergunta seja sorteada
        else:																															        #se estiver incorreta
            print(f"Ops! Resposta incorreta. A resposta correta era: {pergunta_da_rodada['correct_answer']}")
            print(f"Fim de jogo! Você perdeu, mas seu prêmio final é de 10% do acumulado: {premio_erro}")
            break																														        #encerra o jogo
    else: 																																		#executado se o loop while terminar normalmente (se todas as perguntas foram respondidas)
        if acumula_premio == "1 BTC":
            print("\nVOCÊ ALCANÇOU O PRÊMIO MÁXIMO! PARABÊNS, VOCÊ GANHOU 1 BTC!")
        else:
            print("\nParabéns! Você respondeu todas as perguntas!")
            print(f"Seu prêmio final é: {acumula_premio}")

    print(f"Pulos utilizados nesta partida: {pulos_usados}.")
    print("\nObrigado por jogar o Show do Bitcoin!")

if __name__ == "__main__":																													    #garante que as funções so rodem quando o script é executado diretamente 
    perguntas_baixadas = baixa_perguntas()																										#tenta baixar as perguntas
    
    if perguntas_baixadas is not None:																											#se baixou com sucesso 
        inicia_jogo(perguntas_baixadas)																											#inicia o jogo com elas
    else:
        print("\nNão foi possível iniciar o jogo devido à falha no download das perguntas.")
