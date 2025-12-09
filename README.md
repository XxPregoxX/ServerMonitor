# Software monitor

Esse é um software simples para monitoramento de servidores linux via interface web.

## :clipboard: Features
- Monitoramento remoto
- Atualização em tempo real dos valores de rede, memória, CPU e discos.
- Informações técnicas basicas da CPU, memorias e discos
- ~~Timers de atualização configuraveis~~ <sup>Planejado</sup>
- ~~Design mobile~~ <sup>Planejado</sup>
- ~~Lista de processos ativos em tempo real~~ <sup>Planejado</sup>

## :books: Sobre o projeto

### Inspiração
Esse projeto é inspirado primariamente no [htop](https://github.com/htop-dev/htop), porém também tem elementos inspirados no Gerenciador de tarefas do Windows, é meio que uma mescla de ambos com a possibilidade de monitorar tudo pela rede. 

### Design
O design foi pensado para ser minimalista e intuitivo porém com algumas animações simples de transição, isso com o intuíto de manter agradavel de olhar e evitar atualizações secas, também optei por adicinar animações em relação a coloração, principalmente relacionado ao load das CPUS, temperaturas. Com o intuíto de sinalizar valores elevadados nestes campos.

### Compatibilidade
Ele é apenas compativel com Linux, pois usa comandos exclusivos do linux para extrair algumas informações, lsblk, lscpu... Sim, tem como adaptar para o Windows, porém não está nos planos do projeto, talvez uma atualização futura, mas não está nos planos envolvendo este projeto.

### Acesso Web
O projeto foi pensado para ser acessado pela rede, a interface é web possibilita o monitoramento remoto, pode ser feito via tunel Cloudflare ou IP fixo.

## :black_joker: Instalação

Colocar aqui depois de pronto

## :computer: Requisitos

Nada muito especifico, uma maquina com linux, todas os pacotes e bibliotecas nescessárias.

A maquina mais fraca que eu consegui testar tem um Celeron J1800 e 4G de ram, não teve nenhum problema, é mais pesado para a maquina que abre a interface web do que para o servidor rodando o programa, de qualquer forma, em relação a hardware a principio deve rodar em tudo sem problema nenhum.
