#SOAP_Cliente_zeep.py
import os
import zeep

client = zeep.Client(wsdl='http://127.0.0.1:8888')

opcao = "a"

while(opcao != "s"):
    os.system('cls' if os.name == 'nt' else 'clear')

    print("1- para validar CPF")
    print("2- para verificar se o número é ímpar ou par")
    print("3- para realizar uma operação numérica")
    print("s para sair")
    opcao = input()

    os.system('cls' if os.name == 'nt' else 'clear')

    if(opcao == "1"):
        cpf = input("Digite o CPF: ")
        print (client.service.valida_CPF(cpf))
        aux = input()

    elif(opcao == "2"):
        numero = int(input("Digite um numero: "));
        print("PAR = TRUE, ÍMPAR = FALSE")
        print(str(client.service.verifica_NumeroPar(numero)))
        aux = input()

    elif(opcao == "3"):
        print("Digite o operador \n+ Para soma \n- Para subtração \n* Para multiplicação \n/ Para divisão")
        operador = input();
        num1 = int(input("Digite o primeiro número "));
        num2 = int(input("Digite o segundo número "));

        if(operador == "/" and num2 == 0):
            print("Segundo número é inválido, tente novamente")
        else:
            resultado = (str(client.service.math_operation(operador, num1, num2)))
            print(num1, operador, num2, "=", resultado)

        aux = input()
            
    elif(opcao == "s"):
        opcao = "s"
    else:
        print("Opção inválida")
        aux = input()