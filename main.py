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
janela.geometry("300x380")

# Frames
frame_tela = Frame(janela, width=300, height=60, bg=cor2)
frame_tela.grid(row=0, column=0)

frame_corpo = Frame(janela, width=300, height=320, bg=cor1)
frame_corpo.grid(row=1, column=0)

# Variáveis
todos_valores = ""
valor_texto = StringVar()

# Funções
def entrar_valores(event):
    global todos_valores
    todos_valores += str(event)
    valor_texto.set(todos_valores)

# Closure para a criação de cada transformador
def criar_transformador(antigo, novo):
    def transformar(expressao):
        return expressao.replace(antigo, novo)
    return transformar

# Lista de transformadores
transformadores = [
    criar_transformador("^", "**"),           # Potência
    criar_transformador("rq", "math.sqrt"),   # Raiz quadrada
    criar_transformador("%", "/100")          # Porcentagem
]

# Função de alta ordem para a aplicação de todos os tranformadores em sequência
def aplicar_transformadores(transformadores):
    def aplicar(expressao):
        for t in transformadores:
            expressao = t(expressao)
        return expressao
    return aplicar

# Versão configurada com todos os transformadores
aplicar = aplicar_transformadores(transformadores)

def calcular():
    global todos_valores
    try:
        expressao = aplicar(todos_valores)  # aplica transformadores de uma vez
        resultado = eval(expressao)
        valor_texto.set(str(resultado))
        todos_valores = str(resultado)  # mantém o resultado calculado
    except:
        valor_texto.set("Não é possível calcular")
        todos_valores = ""

def limpar_tela():
    global todos_valores
    todos_valores = ""
    valor_texto.set("")

# Label (Display)
app_label = Label(frame_tela, textvariable=valor_texto, width=40, height=5, padx=7, relief=FLAT, anchor="e", justify=RIGHT, bg=cor2, fg=cor1)
app_label.place(x=0, y=0)

texto_extra = Label( frame_corpo, text="Calculadora Grupo 37\nEdney Freitas, Felipe da Silva\nMary Ruth Vasconcelos, Mateus Trigueiro\nRaquel Santana e Vitor Samuel Mendonça ", width=40, height=6, padx=7, relief=FLAT, anchor="center", justify="center", bg=cor1, fg=cor2)
texto_extra.place(x=0, y=230)

# Configuração dos botões (texto, comando, x, y, largura, cor)
botoes = [
    ("C", limpar_tela, 0, 0, 20, cor3),
    ("(", lambda: entrar_valores("("), 150, 0, 10, cor3),
    (")", lambda: entrar_valores(")"), 225, 0, 10, cor3),
    ("^", lambda: entrar_valores("^("), 0, 40, 10, cor3),
    ("rq", lambda: entrar_valores("rq("), 75, 40, 10, cor3),
    ("%", lambda: entrar_valores("%"), 150, 40, 10, cor3),
    ("/", lambda: entrar_valores("/"), 225, 40, 10, cor3),
    ("1", lambda: entrar_valores("1"), 0, 80, 10, cor5),
    ("2", lambda: entrar_valores("2"), 75, 80, 10, cor5),
    ("3", lambda: entrar_valores("3"), 150, 80, 10, cor5),
    ("*", lambda: entrar_valores("*"), 225, 80, 10, cor3),
    ("4", lambda: entrar_valores("4"), 0, 120, 10, cor5),
    ("5", lambda: entrar_valores("5"), 75, 120, 10, cor5),
    ("6", lambda: entrar_valores("6"), 150, 120, 10, cor5),
    ("-", lambda: entrar_valores("-"), 225, 120, 10, cor3),
    ("7", lambda: entrar_valores("7"), 0, 160, 10, cor5),
    ("8", lambda: entrar_valores("8"), 75, 160, 10, cor5),
    ("9", lambda: entrar_valores("9"), 150, 160, 10, cor5),
    ("+", lambda: entrar_valores("+"), 225, 160, 10, cor3),
    (".", lambda: entrar_valores("."), 0, 200, 10, cor5),
    ("0", lambda: entrar_valores("0"), 75, 200, 20, cor5),
    ("=", calcular, 225, 200, 10, cor4)
]

# Criação dos botões com list comprehension
[Button(frame_corpo, text=txt, command=cmd, width=w, height=2, bg=cor).place(x=x, y=y)
 for txt, cmd, x, y, w, cor in botoes]

janela.mainloop()
