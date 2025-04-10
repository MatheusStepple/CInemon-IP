# Projeto - IP
Projeto de Introdução à Programação do semestre 2024.2, o objetivo era que o grupo será responsável por criar um sistema interativo em um ambiente 2D, no qual o usuário controla um objeto com a finalidade de coletar outros objetos dispostos na tela. Deverão ser incluídos no mínimo três tipos distintos de objetos coletáveis. O sistema deverá manter um registro da quantidade de objetos coletados para cada tipo e exibirá essas informações ao usuário. Além disso, o projeto deverá ser estruturado com base na Orientação a Objetos


## Título do Projeto:  CINEMON IP - A Revolução
## Link do repositório no GitHub do projeto: [Clique aqui!](https://github.com/MatheusStepple/CInemon-IP)
## Organização técnica do Código:
O código foi divido em módulos como aconselhado pelos professores e monitores. Eles estão organizados dessa maneira abaixo:
- **Main**: É o principal módulo do projeto, ele que é o responsável por criar a tela em que o jogo passará, além de importar todos os outros módulos do projeto;
- **Batalha_ui**: Módulo direcionado para o confronto entre cinemons, onde nele tem os cinemons inimigos e aliados, vantagens e desvategens entre diferentes tipos de cinemons;
- **Cinemon**: Módulo de definicação da cada cinemon que existe no jogo, sendo suas cores, classes e etc;
- **Config**: É um banco de varíaveis que são utilizadas no projeto todo, como por exemplos os parámetros de vantagens e fraquezas;
- **Gema**: É o modulo onde está definido a posição, quantidade e propriedades do coletável "Gema";
- **Inimigo**: É onde a gente define o nome, a imagem, a posição de cada inimigo do jogo;
- **Jogo_base**: É onde detém a lógica de colisão, troca de mapa, a posição de todas as gemas,definição dos cinemons iniciáis, diálogos entre os NPC's, trigger de início da batalha e verificação dos crachás;
- **Jogo_ui**: É onde estão todas as caixas de mensagens dos NPC's, sistema de zoom e o diálogo inicial;
- **NPC**: Modulo direcionado ao carregamento dos sprites dos NPC's e suas hitbox's;
- **Personagem**: Este é o módulo em que tem as sprites do personagem principal, além do código de suas animação em game.
## Ferramentas utilizadas no projeto:
O jogo foi desenvolvido em **Python** junto ao **Pygame**, escolhido pelas suas enormes ferramentas de criação de jogos, além de ter vindo pela inspiração do vídeo do canal [*ClearCode*](https://www.youtube.com/@ClearCode)

Para rodar o jogo é necessário ter instalado o [Python](https://docs.python.org/pt-br/3/), o módulo [Pygame](https://www.pygame.org/docs/) e o  [PyTmx](https://pytmx.readthedocs.io/en/latest/).
### Instalação do Pygame

Para instalar o Pygame, pode-se usar o comando:
```bash
python3 -m pip install -U pygame --user
```
### Instalção PyTMX
Para instalar o PyTMX, pode-se usar o comando:
```bash
pip install pytmx
```
Outra ferramenta utilizada no projeto foi o **Tiled** um editor gratuito e de código aberto voltado para criação de mapas 2D baseados em tiles (blocos). Ideal para desenvolvedores de jogos, ele permite montar cenários completos de forma visual e intuitiva, usando imagens organizadas em tilesets. Com suporte a múltiplas camadas, objetos personalizados e exportação em diversos formatos (como .tmx e .json), o Tiled se integra facilmente a engines e bibliotecas como Pygame, Godot, Unity (com plugins) e muito mais. É a ferramenta perfeita para quem quer criar mundos ricos e organizados com precisão, sem precisar codar cada pedacinho do mapa.
![tiled](https://i.ytimg.com/vi/pu-yShBRCqM/maxresdefault.jpg)

##   Sobre o Projeto:
O projeto foi inspirado no vídeo do canal *ClearCode* [The ultimate introduction to Pygame
](https://www.youtube.com/watch?v=AY9MnQ4x3zk&t=3093s), seguindo diretamente suas noções de uso, organizacionais e técnicas.

Foi utilizado também o aplicativo [Drive](https://drive.google.com/?authuser=0) e [Google Docs](https://docs.google.com/document/?usp=docs_ald&authuser=0) para uma melhor organização de ideias e de imagens utilizadas no projeto.

O CINemon IP é um jogo 2D com câmera top-down quem tem como foco o controle do jogador Pooh, o qual é um estudante da UFPE recrutado para conter a revolução de Pedro Noites, que criou criaturas digitais (CInemons) para dominar o campus e restaurar a grade antiga do CIn. Seu objetivo é escolher 3 CInemons e enfrentar os líderes revolucionários (Sergio, Fernanda e Ricardo) para restaurar a ordem acadêmica.

## Conceitos vistos na disciplina e usados no código
 - **Lista**: Guardam coleções ordenadas (ex: CInemons do jogador, linhas de mensagem), usada para iterar e desenhar itens como CInemons e mensagens na tela.
 - **Dicionários**: Armazenam pares chave-valor, usada para cache de sprites (self.sprites_cache) para evitar recarregamento de imagens.
 - **Condicionais**:  Controlam decisões no código, elas estão usando por exemplo na verificassão se o CInemon pode ser trocado, se está desmaiado, se há tremor, etc.
 - **Laços**: Elas repetem ações sobre coleções, elas estão basicamente interando sobre a  listas de CInemons ou linhas de texto para renderizar elementos.
 - **Funções**: Eles estão encapsulando os blocos de lógica reutilizáveis, como por exemplo no carregamento de sprites, desenhar barras de vida, mostrar menus e telas da batalha.
 - **Programação Orientada a Objetos**: Uma concepção de criar código utilizada em todo o jogo, com classes para o player, inimigos, coletáveis, level, cada um com uma infinidade de atributos e métodos, e foi visível a grande importância dessa forma de programação em grandes projetos como esse jogo, facilitando a organização, compartilhamento de caracteristícas, funções e etc.

## COMO JOGAR:
- **Movimento**: WASD ou setas
- **Interação**: Espaço
- **Menu**: ESC
- **Batalhas**: 
- 1/2: **Ataques** 
- 3: **Trocar CInemon**

**CINEMONS DISPONÍVEIS**:
- 🔥 **Fogo**: Heatbug, Patchburn
- ⚡ **Elétrico**: Pikacode, Ampereon
- 🌍 **Terra**: Minerbit, Terrabyte
- 💧 **Água**: Hydrabyte, Debbubble
- 🌿 **Planta**: Dataflora, Treebit

CHEFES:
- **(Sérgio - CIn)**
- **(Fernanda- CIn)**
- **(Pedro Noites CIn)** - com Paradoxium (tipo Discreto)

**SISTEMA DE BATALHA**:
- **Fogo** > **Planta** > **Terra** > **Elétrico** > **Água** > **Fogo**
- **Tipos Especiais** têm resistências únicas.

**OBJETIVO FINAL**:
 Chegar no CIn, recuperando os pedaços dos crachás e impedindo Pedro Noites de restaurar a antiga grade do CIn

- **Gênero**: RPG Acadêmico-Tático
- **Plataforma**: PC (Python/Pygame)

## Contribuidores e suas funções no Projeto
- Matheus Henrique [GitHub](https://github.com/MatheusHenriqueCIN)
  - Responsável pela criação do mapa principal do jogo e sua renderização
  - Atualização da documentação.
  - Idealizador do roteiro do jogo
- Matheus Stepple [GitHub](https://github.com/MatheusStepple)
  - Coordenador do processo de merge, criação de branches e ferramentas do Git/GitHub.
  - Criação da colisão no jogo
  - Ajustes do sistema de batalha
  - Responsável pela estruturação e base do código
- Gabriel Machado [GitHub](https://github.com/gabriotz)
  - Criação do teleporte
  - Responsável pela estruturação e base do código
  - Divisão do código em modulos
- Vinícius Pena [GitHub](https://github.com/ViniciusCavalcantiap)
  - Idealização dos cinemons e suas habilidades
  - Criação do sistema de cura do jogo
  - Criação do sistema de ""crachá""
- Felipe Berardo [GitHub](https://github.com/FelipeBerardo)
  - Criação da ultima fase do jogo (CIn)
  - Idealizador do roteiro do jogo
  - Idealização dos cinemons e suas habilidades
- Guilherme Máximo [GitHub](https://github.com/GuiFM05)
  - Criação das sprites dos personagens principais e NPC's
  - Criação dos designs dos cinemons

## Desafios e Erros
 - **Maior erro do projeto**: A falta de tempo, alinhada com a falta de conhecimento e noção, fizeram com que nós idealizássemos um jogo muito mais complexo do que nós imaginamos, levando a um grande problema de organização e uma correria maior e desnecessária para a finalização do projeto.
 - **Maior desafio do projeto**: O maior desafio do projeto ao nosso ver foi entender a documentação do PyTMX e a sua relação com o Pygame. Contornamos esse desafio na base da tentativa e erro, até que chegamos a aprender o assunto.
 - **Lições aprendidas**: Este projeto foi extremamente importante para nós, com ele conseguimos botar em prática os conceitos aprendidos ao longo da matéria e por em prática e entender a importância da Progrmação Orientada a Objetos. Além disso, percebemos o quão importante é aprender a utilizar o GitHub, um aplicativo fundamental para nossa área.  
