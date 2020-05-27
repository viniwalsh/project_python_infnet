import socket, time, pickle, psutil

# Função que Imprime a lista formatada
def Imprimir(l):
    texto = ''
    for i in l:
        texto = texto + '{:>8.2f}'.format(i)
    print(texto)

def formatar_processos_2():
    titulo = '{:^7}'.format("PID")
    titulo = titulo + '{:^11}'.format("# Threads")
    titulo = titulo + '{:^26}'.format("Criação")
    titulo = titulo + '{:^9}'.format("T. Usu.")
    titulo = titulo + '{:^9}'.format("T. Sis.")
    titulo = titulo + '{:^12}'.format("Mem. (%)")
    titulo = titulo + '{:^12}'.format("RSS")
    titulo = titulo + '{:^12}'.format("VMS")
    titulo = titulo + " Executável"
    print(titulo)

def formatar_processos_1(pid):
    try:
        p = psutil.Process(pid)
        texto = '{:6}'.format(pid)
        texto = texto + '{:11}'.format(p.num_threads())
        texto = texto + " " + time.ctime(p.create_time()) + " "
        texto = texto + '{:8.2f}'.format(p.cpu_times().user)
        texto = texto + '{:8.2f}'.format(p.cpu_times().system)
        texto = texto + '{:10.2f}'.format(p.memory_percent()) + " MB"
        rss = p.memory_info().rss / 1024 / 1024
        texto = texto + '{:10.2f}'.format(rss) + " MB"
        vms = p.memory_info().vms / 1024 / 1024
        texto = texto + '{:10.2f}'.format(vms) + " MB"
        texto = texto + " " + p.exe()
        print(texto)
    except:
        pass


def formatar_redes(l):
    titulo = '{:11}'.format("Ip")
    titulo = titulo + '{:27}'.format("Netmask")
    titulo = titulo + '{:27}'.format("MAC")

    print(titulo)

# Cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Tenta se conectar ao servidor
s.connect((socket.gethostname(), 6666))

controle = True

menu = s.recv(1024)

while controle:
    print(menu.decode('utf-8'))
    msg1 = input('digite a opção desejada: ')
    if msg1 == '1':
        s.send(msg1.encode('utf-8'))
        msg = ' '
        print('{:>8}'.format('%CPU')+'{:>8}'.format('%MEM'))
        # Envia mensagem vazia apenas para indicar a requisição

        bytes = s.recv(1024)
        # Converte os bytes para lista

        lista = pickle.loads(bytes)
        #Uso de Cpu e memoria em Porcentagem#
        Imprimir(lista)

        info_cpu = s.recv(1024)
        info = pickle.loads(info_cpu)

        # Informações do Processador#
        print('Processador:', info['brand'])  # brand
        print('Arquitetura:', info['arch'])  # arch
        print('Bits: ', info['bits'])  # bits
        cpu = s.recv(1024)
        cpu_logico = pickle.loads(cpu)["cpu_logico"]
        print('Núcleos Lógicos:', cpu_logico) # de cpu por núcleos
        cpu_frequencia = pickle.loads(cpu)["cpu_frequencia"]
        print('Frequência:', cpu_frequencia) #frequencia total
        cpu_fisico = pickle.loads(cpu)["cpu_fisico"]
        print('Núcleos Físicos:', cpu_fisico) #nº de núcleos e Threads
        recebe_disco = s.recv(1024)
        disco = pickle.loads(recebe_disco)
        print("Percentual de Disco Usado:", disco.percent, '%')

    elif msg1 == '2':
        s.send(msg1.encode('utf-8'))
        bytes = s.recv(2048)
        lista2 = pickle.loads(bytes)
        titulo = '{:11}'.format("Tamanho") # 10 caracteres + 1 de espaço
        # Concatenar com 25 caracteres + 2 de espaços
        titulo = titulo + '{:27}'.format("Data de Modificação")
        # Concatenar com 25 caracteres + 2 de espaços
        titulo = titulo + '{:27}'.format("Data de Criação")
        titulo = titulo + "Nome"
        print(titulo)
        for i in lista2:
            kb = lista2[i][0]/1000
            tamanho = '{:10}'.format(str('{:.2f}'.format(kb)+' KB'))
            print(tamanho, time.ctime(lista2[i][2]), " ", time.ctime(lista2[i][1]), " ", i)

    elif msg1 == '3':
        s.send(msg1.encode('utf-8'))
        bytes = s.recv(1024)
        dic = pickle.loads(bytes)
        lista = psutil.pids()
        formatar_processos_2()
        for i in lista:
            formatar_processos_1(i)

    elif msg1 == '4':
        s.send(msg1.encode('utf-8'))
        bytes = s.recv(2048)
        dic_redes = pickle.loads(bytes)
        print('Endereço de Rede:',dic_redes['Ethernet'][1].address)
        print('Mascara de Rede:',dic_redes['Ethernet'][1].netmask)
        print('MAC:',dic_redes['Ethernet'][0].address)

    elif msg1 == '5':
        s.send(msg1.encode('utf-8'))
        bytes = s.recv(1024)
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        controle = False
    else:
        print('Opção inválida!')
