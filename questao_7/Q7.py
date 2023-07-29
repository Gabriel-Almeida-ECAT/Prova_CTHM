import socket
import datetime
import time
import os

host = '192.168.100.6'
port = 4545
#valores obtidos da caixa de mensagem do programa em java de simulação da caldeira

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))


def main():
    with open("values.txt", 'r+') as file_handler:
        list_registers = []
        register_holder = ''

        #de acordo com o arquivo de referência há 11 linhas em cada registro no arquivo de monitoramento
        for ind in range(11):
            register_holder + file_handler.readline()

        list_registers.append(register_holder)

        while True:
            time.sleep(1000)
            os.system('cls' if os.name == 'nt' else 'clear')
            msg, addr = s.recvfrom(1000) #tamanho de buffer obtido do arquivo 'client2014.h'

            if msg < 0:
                print("<! Error !>")
                exit(0)

            if len(list_registers) == 5:
                #remove o registro mais antigo caso já hajam 5 registros
                list_registers = list_registers[1:]
                list_registers.append(msg)
            else:
                list_registers.append(msg)

            file_handler.seek(0)

            for ind in range(5):
                file_handler.write(str(list_registers[ind]))

            curent_time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"in {curent_time} - muliplied: {msg.decode('UTF-8')}")


if __name__ == '__main__':
    main()
