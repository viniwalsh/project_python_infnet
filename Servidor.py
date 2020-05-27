import socket, psutil, pickle, os, cpuinfo

def uso_cpu_ram(socket_cliente):
    info1 =('Usuario solicitou Informações do computador')
    # Gera a lista de resposta
    resposta = []#lista dados
    resposta.append(psutil.cpu_percent())
    mem = psutil.virtual_memory()
    mem_percent = mem.used/mem.total * 100
    resposta.append(mem_percent)
    #Armazena Informações da CPU
    # info_cpu = cpuinfo.get_cpu_info()
    # socket_cliente.send(info_cpu)
    # Prepara a lista para o envio
    bytes_resp = pickle.dumps(resposta)#biblioteca compacta os arquivos ==> 1024 a 1024 bis-> bytes
    # Envia os dados
    socket_cliente.send(bytes_resp) # Envia mensagem
    print(info1)

def info_cpu(socket_cliente): #arquitewtura
    info = cpuinfo.get_cpu_info()
    envia_dados = pickle.dumps(info) #compacta dados - dicio
    socket_cliente.send(envia_dados)

def info_processador(socket_cliente):
    cpu_porc = psutil.cpu_count() #% de cpu por núcleos
    cpu_freq =psutil.cpu_freq().current #frequencia total
    cpu_nucleos = psutil.cpu_count(logical=False) #nº de núcleos e Threads
    resposta = {
        "cpu_logico": cpu_porc,
        "cpu_frequencia": cpu_freq,
        "cpu_fisico": cpu_nucleos
    }
    socket_cliente.send(pickle.dumps(resposta))

def info_disk(socket_cliente):
    disco = psutil.disk_usage('.')
    envia_dados = pickle.dumps(disco)
    socket_cliente.send(envia_dados)


def arquivos_diretorios(socket_cliente):
    info2 = 'Usuario solicitou Informações sobre processos ativos'
    #obtém lista de arquivos e diretórios
    lista = os.listdir()#obtem lista arquivos diretorio
    #Cria um dicionário
    dic = {}
    for i in lista: #varia na lista dos arquivos e diretórios
        if os.path.isfile(i):#checa se é um arquivo
            dic[i] = []
            dic[i].append(os.stat(i).st_size)#tamanho
            dic[i].append(os.stat(i).st_atime)#tempo de criação
            dic[i].append(os.stat(i).st_mtime)#Tempo de Modificação
    bytes_rep = pickle.dumps(dic)
    # Envia os dados
    socket_cliente.send(bytes_rep)  # Envia mensagem
    print(info2)

def processos_ativos(socket_cliente):
    lista = psutil.pids() #pids
    bytes_rep = pickle.dumps(lista)
    socket_cliente.send(bytes_rep)  # Envia mensagem


def info_redes(socket_cliente):
    dic_interfaces = psutil.net_if_addrs()
    ip = socket.gethostbyname(socket.gethostname())
    bytes_rep = pickle.dumps(dic_interfaces) #dicionario
    socket_cliente.send(bytes_rep)  
    

def encerrar_conexao(socket_cliente):
    info = ('Conexão Encerrada!')
    socket_cliente.send(info.encode('urf-8'))
    print("Fechando Conexão com", str(addr), "...")
    socket_cliente.shutdown(socket.SHUT_RDWR)
    socket_cliente.close()

# Cria o socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Obtem o nome da máquina
host = socket.gethostname()
porta = 6666
# Associa a porta
socket_servidor.bind((host, porta))
# Escutando...
socket_servidor.listen()
print("Servidor", host, "esperando conexão na porta", porta)
# Aceita alguma conexão
(socket_cliente,addr) = socket_servidor.accept()
print("Conectado a:", str(addr))

info = ("\n ====================MENU======================="
        "\n 1 - Informações da Máquina "
        "\n 2 - Informações de Arquivos "
        "\n 3 - Informações Processos Ativos "
        "\n 4 - Informações de Redes "
        "\n 5 - Sair "
        "\n ==============================================")
socket_cliente.send(info.encode('utf-8')) # Envia resposta

while True:
    # Decodifica mensagem em UTF-8:
    msg = socket_cliente.recv(1024)
    if '1' == msg.decode('utf-8'):
        uso_cpu_ram(socket_cliente)
        info_cpu(socket_cliente)
        info_processador(socket_cliente)
        info_disk(socket_cliente)
    elif '2' == msg.decode('utf-8'):
        arquivos_diretorios(socket_cliente)
        print('O Usuário Solicitou Informações sobre Arquivos.')
    elif '3' == msg.decode('utf-8'):
        processos_ativos(socket_cliente)
        print('O usuário solicitou informações sobre processos.')
    elif '4' == msg.decode('utf-8'):
        info_redes(socket_cliente)
        print('O Usuário solicitou informações de redes')
    elif '5' == msg.decode('utf-8'):
        encerrar_conexao(socket_cliente)
        break
    else:
        print('O usuário Digitou opções inválidas.')
