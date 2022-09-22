import random

print("****************************************")
print("Bem-Vindx no jogo de Adivinhação")
print("****************************************")

numero_secreto = random.randrange(1, 101)

total_tentativas = 3

for rodada in range(1, total_tentativas + 1):

    print("Tentativa {} de {}".format(rodada, total_tentativas))

    chute = input("Digite um número entre 1 e 100:")

    print("Você digitou o número: ", chute)

    chute = int(chute)

    acertou = chute == numero_secreto
    maior = chute > numero_secreto
    menor = chute < numero_secreto

    if chute < 1 or chute > 100:
        print("Você deve digitar um número entre 1 e 100!")
        continue

    if acertou:
        print("Você acertou!")
        break
    else:
        if menor:
            print("Você errou! O seu chute foi menor!")
        elif maior:
            print("Você errou! O seu chute foi maior!")

print("Fim do jogo!")
