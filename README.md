Projeto Triplo Integrado: Chat de Aconselhamento
Objetivo
O projeto Triplo Integrado é uma aplicação de chat de aconselhamento que integra conceitos de Sistemas Operacionais, Protocolos de Redes e Estruturas de Dados. O principal objetivo é criar um ambiente virtual onde conselheiros e aconselhados podem se comunicar em tempo real, fornecendo suporte e aconselhamento.

Funcionalidades Principais
Servidor
Login e Registro: Os usuários podem realizar login ou se registrar para acessar o chat.
Emparelhamento Dinâmico: O servidor emparelha conselheiros e aconselhados com base em suas notas e preferências, usando uma árvore de busca binária e dicionários para definir notas mínimas.
Chat Privado: Os usuários podem participar de vários chats privados simultaneamente, com assuntos e intensidades específicas.
Cliente
Login e Registro: Os usuários podem criar uma conta ou fazer login usando credenciais existentes.
Escolha de Intensidade e Assunto: Os aconselhados podem escolher a intensidade (baixa, média, alta) e o assunto do chat.
Comunicação em Tempo Real: Os usuários podem trocar mensagens em tempo real durante o chat.
Notificação de Eventos: Os usuários são notificados sobre eventos importantes, como início de um chat ou desconexão.
Tecnologias Utilizadas
Sistemas Operacionais
Threads: Utilização de threads para permitir a comunicação simultânea com vários clientes, gerenciando concorrência por meio de mutex para garantir exclusão mútua.
Mutex: Mecanismo de mutex (exclusão mútua) para proteger seções críticas do código e evitar condições de corrida.
Protocolos de Redes
TCP/IP: Comunicação entre clientes e servidor usando o protocolo TCP/IP para garantir uma transferência confiável e ordenada de dados.
Dicionários para Protocolo: Uso de dicionários para definir códigos e mensagens padronizadas entre o servidor e os clientes.
Estruturas de Dados
Chaining Hash Table: Utilizada para armazenar usuários online, informações de conselheiros e chats ativos.
Binary Search Tree: Usada para armazenar conselheiros com base em suas notas, facilitando a busca e seleção eficientes.
Como Executar o Projeto
Clone o repositório para sua máquina local.
Execute o servidor usando o comando python server.py.
Execute os clientes usando o comando python client.py.
Certifique-se de ter as bibliotecas necessárias instaladas. Consulte o arquivo requirements.txt para obter informações detalhadas.
