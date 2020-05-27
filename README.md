Projeto de Bloco Faculdade Infnet - Projeto Pyhton

Projeto realizado em 02/10/2018

Desenvolvimento do Sistema
Projetado utilizando a tecnologia python 3.6, foram utilizadas algumas bibliotecas para auxiliar o desenvolvimento como: socket, pickle, cpuinfo, psutil e OS. O projeto fui feito em cima da comunicação via socket sendo o mesmo dividido em parte cliente e parte servidor. Na parte cliente o usuário se depara com um menu simples e intuitivo onde basta alguns cliques e ele estará com as informações que precisa. O trabalho ocorre no ‘back-end’ ou seja, na parte servidor onde estará sendo processadas as informações pedidas pelo usuário, utilizando as bibliotecas cpuinfo, psutil e OS, conseguimos pegar informações importantes da máquina do usuário e utilizando a biblioteca pickle enviamos os pacotes de dados (informações) do nosso servidor para nosso cliente.
Utilizamos a conexão TCP, pois queremos uma conexão segura entre de nosso sistema onde teremos a confiança de que toda informação pedida no lado cliente será recebida por nosso servidor e toda mensagem enviada pelo servidor chegará no cliente de maneira confiável e segura.
Como mencionado, o sistema e dividido em duas partes para maior otimização do mesmo, cliente e servidor, trabalhando de forma integrada para melhor servir o usuário.

