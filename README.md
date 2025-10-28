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

---



---

<h2 align="center"> The Bitcoin Show </h2>

This is a terminal-based project called Show do Bitcoin, which uses an API to fetch the questions that will appear. It simulates the Show do Milhão game, but in this version, the prize is given in cryptocurrency format, built in Python.

<h4 align="center"> Game Logic: </h4>

The player starts with a prize amount of 0 BTC. With each correctly answered question, the prize increases.
Questions are divided into different difficulty levels (easy, medium, and hard).
The player can skip up to 3 questions.
If the player answers incorrectly, the game ends, but they receive 10% of the accumulated prize.
The player may also choose to quit at any time, receiving 50% of the accumulated value.

<h4 align="center"> Question Structure: </h4>

Multiple-choice questions with 4 options.
Each question has one correct answer.
The prize increases with each correct answer.

<h4 align="center"> Features: </h4>

Skip questions (up to 3 times).
Quit the game and receive half of the accumulated value.
Wrong answers: End of the game with the prize reduced to 10% of the accumulated value.
Final prize: When the player answers all questions correctly, they win the maximum prize.

<h4 align="center"> Details: </h4>

The questions can be obtained from an API, as in the previous code.
Questions can be categorized into different difficulty levels.
The simulation can include a simple graphical interface displaying the questions and alternatives.

<h4 align="center"> Example Game Flow: </h4>

Game Start: Displays the rules.
First Question: Shows an easy question.
Answers: The player chooses A, B, C, or D.
If correct: The prize increases.
If wrong: The game ends with the prize reduced to 10% of the accumulated value.
If quit: The player receives 50% of the accumulated value.
If skip: The question is discarded, and another question of the same level is presented.
Ending: The final prize is displayed when the player reaches the maximum prize or decides to quit.

<h4 align="center"> How to Run the System </h4>

Make sure you have Python version 3.13 installed.
Ensure you have an internet connection, as the game uses an API to download the questions.

Then, type the following commands in the terminal:

<h5 align="center"> pip install -r requirements.txt (to install the necessary libraries) </h5>
<h5 align="center"> python show_do_bitcoin.py </h5>

What Will Happen:
The code will prompt you to press ENTER to start...
The game will download the questions from the API, display multiple-choice questions,
and the player will be able to interact according to the defined rules (answer, skip, or quit).


