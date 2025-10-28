<h2 align="center"> Show do Bitcoin </h2>
Este e um projeto que roda em terminal chamado show do bitcoin utilizando uma API para solicitar as perguntas que irão aparecer, simula o jogo show do milhão mas neste a premiação seria dada no formato da criptomoeda, feito em Python.

<h4 align="center"> Lógica do Jogo: </h4>
O jogador começa com um valor de prêmio de 0 BTC.
A cada pergunta respondida corretamente, o prêmio aumenta.
As perguntas são de diferentes níveis de dificuldade (fáceis, médias e difíceis).
O jogador pode pular até 3 perguntas.
Se errar, o jogador perde o jogo, mas recebe 10% do prêmio acumulado.
O jogador pode desistir a qualquer momento, recebendo 50% do valor acumulado.

<h4 align="center"> Estrutura das Perguntas: </h4>
Perguntas de múltipla escolha com 4 alternativas.
Cada pergunta tem uma resposta correta.
O prêmio aumenta a cada pergunta correta.

<h4 align="center"> Funcionalidades: </h4>
Pular perguntas (até 3 vezes).
Desistir do jogo e receber metade do valor acumulado.
Respostas erradas: Fim do jogo com prêmio reduzido a 10% do valor acumulado.
Chegada ao prêmio final: Quando o jogador responde todas as perguntas corretamente, ganha o prêmio máximo.

<h4 align="center"> Detalhamento: </h4>
As perguntas podem ser obtidas de uma API, como no código anterior.
As perguntas podem ser categorizadas em diferentes níveis de dificuldade.
A simulação pode incluir uma tela com uma interface gráfica simples, exibindo perguntas e alternativas.
Exemplo de Fluxo de Jogo:
Início do jogo: Exibe as regras.
Primeira pergunta: Mostra a pergunta fácil.
Respostas: O jogador escolhe A, B, C ou D.
Se acertar: Prêmio aumenta.
Se errar: O jogo termina com um prêmio reduzido a 10% do acumulado.
Se desistir: O jogador recebe 50% do valor acumulado.
Se pular: A pergunta é descartada e outra pergunta do mesmo nível é apresentada.
Finalização: O prêmio final é mostrado quando o jogador atinge o prêmio máximo ou decide desistir.

Para rodar o sistema favor se atentar a versão necessaria do python==3.13, certifique-se que tem acesso a internet pois o jogo utilizará a API cpara baixar as perguntas, após digite no terminal:

<h5 align="center"> pip install -r requirements.txt (para instalar a biblioteca necessaria) </h5>
<h5 align="center">  python show_do_bitcoin.py </h5>

O que acontecerá:

O código irá pedir para você pressionar ENTER para começar...

O jogo vai baixar as perguntas da API, exibir as perguntas de múltipla escolha, e o jogador poderá interagir conforme as regras definidas (responder, pular, desistir).


