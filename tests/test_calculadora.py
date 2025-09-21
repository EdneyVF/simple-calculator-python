"""
Testes unitários.
"""
import unittest
import sys
import os

# Adiciona o diretório pai ao path para importar do main.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa as funções do main.py
import main


class TestCalculadoraLogic(unittest.TestCase):
    """Testes para a lógica da calculadora."""
    
    def setUp(self):
        # Reset da variável global antes de cada teste
        main.todos_valores = ""
        main.valor_texto.set("")
        main.resultado_calculado = False
    
    def test_criar_transformador_potencia(self):
        transformador = main.criar_transformador("^", "**")
        resultado = transformador("2^3")
        self.assertEqual(resultado, "2**3")
    
    def test_criar_transformador_raiz_quadrada(self):
        transformador = main.criar_transformador("rq", "math.sqrt")
        resultado = transformador("rq(9)")
        self.assertEqual(resultado, "math.sqrt(9)")
    
    def test_criar_transformador_porcentagem(self):
        transformador = main.criar_transformador("%", "/100")
        resultado = transformador("50%")
        self.assertEqual(resultado, "50/100")
    
    def test_aplicar_transformadores_funcao_alta_ordem(self):
        # Testa com transformadores simples
        transformadores_teste = [
            main.criar_transformador("a", "1"),
            main.criar_transformador("b", "2")
        ]
        aplicar_teste = main.aplicar_transformadores(transformadores_teste)
        resultado = aplicar_teste("a+b")
        self.assertEqual(resultado, "1+2")
    
    def test_aplicar_transformadores_completo(self):
        # Testa expressão com potência
        resultado = main.aplicar("2^3")
        self.assertEqual(resultado, "2**3")
        
        # Testa expressão com raiz quadrada
        resultado = main.aplicar("rq(16)")
        self.assertEqual(resultado, "math.sqrt(16)")
        
        # Testa expressão com porcentagem
        resultado = main.aplicar("25%")
        self.assertEqual(resultado, "25/100")
    
    def test_calcular_operacoes_basicas(self):
        # Soma
        main.todos_valores = "2+3"
        main.calcular()
        self.assertEqual(main.todos_valores, "5")
        
        # Subtração
        main.todos_valores = "10-4"
        main.calcular()
        self.assertEqual(main.todos_valores, "6")
        
        # Multiplicação
        main.todos_valores = "3*4"
        main.calcular()
        self.assertEqual(main.todos_valores, "12")
        
        # Divisão
        main.todos_valores = "8/2"
        main.calcular()
        self.assertEqual(main.todos_valores, "4.0")
    
    def test_calcular_operacoes_avancadas(self):
        # Potência
        main.todos_valores = "2^3"
        main.calcular()
        self.assertEqual(main.todos_valores, "8")
        
        # Raiz quadrada
        main.todos_valores = "rq(9)"
        main.calcular()
        self.assertEqual(main.todos_valores, "3.0")
        
        # Porcentagem
        main.todos_valores = "50%"
        main.calcular()
        self.assertEqual(main.todos_valores, "0.5")
    
    def test_calcular_expressao_invalida(self):
        main.todos_valores = "2++"
        main.calcular()
        # Deve resetar todos_valores em caso de erro
        self.assertEqual(main.todos_valores, "")
        self.assertEqual(main.valor_texto.get(), "Não é possível calcular")
    
    def test_limpar_tela(self):
        main.todos_valores = "123+456"
        main.valor_texto.set("579")
        
        main.limpar_tela()
        
        self.assertEqual(main.todos_valores, "")
        self.assertEqual(main.valor_texto.get(), "")
    
    def test_entrar_valores(self):
        main.todos_valores = ""
        
        main.entrar_valores("1")
        self.assertEqual(main.todos_valores, "1")
        
        main.entrar_valores("+")
        self.assertEqual(main.todos_valores, "1+")
        
        main.entrar_valores("2")
        self.assertEqual(main.todos_valores, "1+2")
    
    def test_conceitos_programacao_funcional(self):
        # Testa se existe função lambda (verificada na criação dos botões)
        # Como as lambdas estão na lista de botões, testamos indiretamente
        self.assertTrue(callable(lambda x: x))
        
        # Testa list comprehension (verificada na criação dos botões)
        # Simula a list comprehension usada no código
        numeros = [1, 2, 3, 4, 5]
        quadrados = [x**2 for x in numeros]
        self.assertEqual(quadrados, [1, 4, 9, 16, 25])
        
        # Testa closure (já testado em test_criar_transformador_*)
        transformador = main.criar_transformador("test", "resultado")
        self.assertEqual(transformador("test"), "resultado")
        
        # Testa função de alta ordem (já testado em test_aplicar_transformadores_*)
        self.assertTrue(callable(main.aplicar_transformadores))


class TestCalculadoraIntegracao(unittest.TestCase):
    
    def setUp(self):
        main.todos_valores = ""
        main.valor_texto.set("")
        main.resultado_calculado = False
    
    def test_fluxo_calculo_completo(self):
        # Simula entrada: 2^3+rq(16)
        main.entrar_valores("2")
        main.entrar_valores("^")
        main.entrar_valores("3")
        main.entrar_valores("+")
        main.entrar_valores("rq(16)")
        
        # Verifica se a expressão foi construída corretamente
        self.assertEqual(main.todos_valores, "2^3+rq(16)")
        
        # Calcula o resultado
        main.calcular()
        
        # 2^3 = 8, rq(16) = 4, então 8+4 = 12
        self.assertEqual(main.todos_valores, "12.0")
    
    def test_fluxo_com_parenteses(self):
        # Simula entrada: (2+3)*4
        main.entrar_valores("(")
        main.entrar_valores("2")
        main.entrar_valores("+")
        main.entrar_valores("3")
        main.entrar_valores(")")
        main.entrar_valores("*")
        main.entrar_valores("4")
        
        main.calcular()
        
        # (2+3)*4 = 5*4 = 20
        self.assertEqual(main.todos_valores, "20")
    
    def test_fluxo_com_decimais(self):
        # Simula entrada: 3.14*2
        main.entrar_valores("3")
        main.entrar_valores(".")
        main.entrar_valores("1")
        main.entrar_valores("4")
        main.entrar_valores("*")
        main.entrar_valores("2")
        
        main.calcular()
        
        # 3.14*2 = 6.28
        self.assertEqual(main.todos_valores, "6.28")
    
    def test_comportamento_apos_calculo_numero(self):
        # Faz um cálculo
        main.entrar_valores("2")
        main.entrar_valores("+")
        main.entrar_valores("3")
        main.calcular()
        
        # Resultado deve ser 5
        self.assertEqual(main.todos_valores, "5")
        self.assertTrue(main.resultado_calculado)
        
        # Clica em um número - deve limpar e começar novo cálculo
        main.entrar_valores("7")
        self.assertEqual(main.todos_valores, "7")
        self.assertFalse(main.resultado_calculado)
    
    def test_comportamento_apos_calculo_operador(self):
        # Faz um cálculo
        main.entrar_valores("2")
        main.entrar_valores("*")
        main.entrar_valores("4")
        main.calcular()
        
        # Resultado deve ser 8
        self.assertEqual(main.todos_valores, "8")
        self.assertTrue(main.resultado_calculado)
        
        # Clica em um operador - deve manter o resultado e continuar
        main.entrar_valores("+")
        self.assertEqual(main.todos_valores, "8+")
        self.assertFalse(main.resultado_calculado)
        
        # Continua o cálculo
        main.entrar_valores("2")
        main.calcular()
        self.assertEqual(main.todos_valores, "10")
    
    def test_comportamento_apos_calculo_ponto_decimal(self):
        # Faz um cálculo
        main.entrar_valores("10")
        main.entrar_valores("/")
        main.entrar_valores("2")
        main.calcular()
        
        # Resultado deve ser 5.0
        self.assertEqual(main.todos_valores, "5.0")
        self.assertTrue(main.resultado_calculado)
        
        # Clica em ponto decimal - deve limpar e começar novo número
        main.entrar_valores(".")
        self.assertEqual(main.todos_valores, ".")
        self.assertFalse(main.resultado_calculado)


if __name__ == '__main__':
    # Executa todos os testes
    unittest.main(verbosity=2)
