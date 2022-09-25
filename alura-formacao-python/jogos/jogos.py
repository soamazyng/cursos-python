import forca
import adivinhacao

print("****************************************")
print("Bem-Vindx no jogo de Adivinhação")
print("****************************************")

print("Escolha um jogo (1) forca (2) adivinhação")

jogo = int(input("Qual o jogo escolhido?"))

if(jogo == 1):
    forca.jogar()
elif (jogo == 2):
    adivinhacao.jogar()
else:
    print("Este jogo não existe")