def operacoes():
    print("Escolha qual operacao deseja realizar: \n 0: multiplicacao \n 1: divisao \n 2: soma \n 3: subtracao")
    operacao = int(input("Escolha qual operacao deseja realizar: "))
    num1 = int(input("Digite o primeiro número: "))
    num2 = int(input("Digite o segundo número: "))
    print(opt[operacao ](num1, num2))


opt = [
        (lambda x, y : x / y),
        (lambda x, y : x * y),
        (lambda x, y : x + y),
        (lambda x, y : x - y)
    ]

operacoes()



