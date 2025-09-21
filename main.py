from tkinter import *
from tkinter import ttk
import math

# Lista de cores
cor1 = "#000000" # Preto
cor2 = "#FFFFFF" # Branco
cor3 = "#FFD700" # Dourado
cor4 = "#50c878" # Verde Esmeralda
cor5 = "#808080" # Cinza
cor6 = "#FF0000" # Vermelho

janela = Tk()
janela.title("Calculadora")
janela.geometry("320x450")
janela.minsize(300, 400)
janela.resizable(True, True)

janela.grid_rowconfigure(0, weight=1)
janela.grid_rowconfigure(1, weight=4)
janela.grid_rowconfigure(2, weight=0)
janela.grid_columnconfigure(0, weight=1)

frame_tela = Frame(janela, bg=cor2)
frame_tela.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

frame_corpo = Frame(janela, bg=cor1)
frame_corpo.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

frame_info = Frame(janela, bg=cor1)
frame_info.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

# Variáveis
todos_valores = ""
valor_texto = StringVar()
resultado_calculado = False  # Flag para controlar estado após o cálculo

# Funções
def entrar_valores(event):
    global todos_valores, resultado_calculado
    
    # limpa se acabou de calcular e clicou em um número ou ponto
    if resultado_calculado and (str(event).isdigit() or str(event) == "."):
        todos_valores = str(event)
        resultado_calculado = False
    # mantém o resultado se acabou de calcular e clicou em um operador
    elif resultado_calculado and str(event) in "+-*/^()%":
        todos_valores += str(event)
        resultado_calculado = False
    # mantém o resultado se acabou de calcular e clicou em "rq(" (raiz quadrada)
    elif resultado_calculado and str(event).startswith("rq"):
        todos_valores += str(event)
        resultado_calculado = False
    # comportamento padrão
    else:
        todos_valores += str(event)
    
    valor_texto.set(todos_valores)

# closure para a criação de cada transformador
def criar_transformador(antigo, novo):
    def transformar(expressao):
        return expressao.replace(antigo, novo)
    return transformar

# lista de transformadores
transformadores = [
    criar_transformador("^", "**"),           # Potência
    criar_transformador("rq", "math.sqrt"),   # Raiz quadrada
    criar_transformador("%", "/100")          # Porcentagem
]

# função de alta ordem para a aplicação de todos os tranformadores em sequência
def aplicar_transformadores(transformadores):
    def aplicar(expressao):
        for t in transformadores:
            expressao = t(expressao)
        return expressao
    return aplicar

# versão configurada com todos os transformadores
aplicar = aplicar_transformadores(transformadores)

def calcular():
    global todos_valores, resultado_calculado
    try:
        expressao = aplicar(todos_valores)
        resultado = eval(expressao)
        valor_texto.set(str(resultado))
        todos_valores = str(resultado)
        resultado_calculado = True
    except:
        valor_texto.set("Não é possível calcular")
        todos_valores = ""
        resultado_calculado = False

def limpar_tela():
    global todos_valores, resultado_calculado
    todos_valores = ""
    valor_texto.set("")
    resultado_calculado = False

# configurar grid do frame_tela
frame_tela.grid_rowconfigure(0, weight=1)
frame_tela.grid_columnconfigure(0, weight=1)

# label (display)
app_label = Label(frame_tela, textvariable=valor_texto, relief=FLAT, anchor="e", justify=RIGHT, bg=cor2, fg=cor1, font=('Arial', 16, 'bold'))
app_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Configurar grid do frame_corpo para os botões em caso de redimensionamento
for i in range(6):  # 6 linhas de botões
    frame_corpo.grid_rowconfigure(i, weight=1)
for i in range(4):  # 4 colunas de botões
    frame_corpo.grid_columnconfigure(i, weight=1)

# label de informações do grupo
texto_extra = Label(frame_info, text="Calculadora Grupo 37\nEdney Freitas, Felipe da Silva\nMary Ruth Vasconcelos, Mateus Trigueiro\nRaquel Santana e Vitor Samuel Mendonça", relief=FLAT, anchor="center", justify="center", bg=cor1, fg=cor2, font=('Arial', 8))
texto_extra.pack(fill=X, pady=5)

# configuração dos botões (texto, função, linha, coluna, colspan, cor)
botoes_grid = [
    ("C", limpar_tela, 0, 0, 2, cor3),
    ("(", lambda: entrar_valores("("), 0, 2, 1, cor3),
    (")", lambda: entrar_valores(")"), 0, 3, 1, cor3),
    ("^", lambda: entrar_valores("^("), 1, 0, 1, cor3),
    ("rq", lambda: entrar_valores("rq("), 1, 1, 1, cor3),
    ("%", lambda: entrar_valores("%"), 1, 2, 1, cor3),
    ("/", lambda: entrar_valores("/"), 1, 3, 1, cor3),
    ("7", lambda: entrar_valores("7"), 2, 0, 1, cor5),
    ("8", lambda: entrar_valores("8"), 2, 1, 1, cor5),
    ("9", lambda: entrar_valores("9"), 2, 2, 1, cor5),
    ("*", lambda: entrar_valores("*"), 2, 3, 1, cor3),
    ("4", lambda: entrar_valores("4"), 3, 0, 1, cor5),
    ("5", lambda: entrar_valores("5"), 3, 1, 1, cor5),
    ("6", lambda: entrar_valores("6"), 3, 2, 1, cor5),
    ("-", lambda: entrar_valores("-"), 3, 3, 1, cor3),
    ("1", lambda: entrar_valores("1"), 4, 0, 1, cor5),
    ("2", lambda: entrar_valores("2"), 4, 1, 1, cor5),
    ("3", lambda: entrar_valores("3"), 4, 2, 1, cor5),
    ("+", lambda: entrar_valores("+"), 4, 3, 1, cor3),
    (".", lambda: entrar_valores("."), 5, 0, 1, cor5),
    ("0", lambda: entrar_valores("0"), 5, 1, 1, cor5),
    ("=", calcular, 5, 2, 2, cor4)
]

# criação dos botões com list comprehension usando grid
[Button(frame_corpo, text=txt, command=cmd, bg=cor, font=('Arial', 12, 'bold'), relief=RAISED, bd=2)
 .grid(row=linha, column=coluna, columnspan=colspan, sticky="nsew", padx=2, pady=2)
 for txt, cmd, linha, coluna, colspan, cor in botoes_grid]

janela.mainloop()
