# Asteroids (singleplayer)

Clone de estilo _Asteroids_ em **Python** e **Pygame**: nave, asteroides em ondas, UFOs, pontuação, vidas, áudio e jogo em **tela cheia** (resolução lógica 960×720 escalada para o monitor).

## Requisitos

- [Python](https://www.python.org/) 3.10 ou superior (recomendado)
- [Pygame](https://www.pygame.org/) 2.x

## Instalação

```bash
pip install pygame
```

(Não há `requirements.txt` no repositório; o comando acima é suficiente.)

## Como executar

O ponto de entrada importa módulos da pasta `src`, por isso o comando deve ser executado **a partir de `src`**:

```bash
cd src
python main.py
```

No Windows (PowerShell), a partir da raiz do projeto:

```powershell
cd src; python main.py
```

## Controles

| Tecla              | Função                                                                          |
| ------------------ | ------------------------------------------------------------------------------- |
| **← / →**          | Rodar a nave                                                                    |
| **↑**              | Acelerar (impulso na direção da frente)                                         |
| **Espaço**         | Tiro (também contínuo enquanto mantiveres premido)                              |
| **S**              | Câmera / tempo mais lento enquanto há energia (gasta energia ao longo do tempo) |
| **Shift esquerdo** | Hiperespaço (teleporte aleatório no ecrã, custo em pontos)                      |
| **Ctrl direito**   | Dash (impulso à frente; custa energia e tem cooldown)                           |
| **ESC**            | Sair (menu ou jogo) ou voltar ao menu (ecrã de game over)                       |
| **Enter / Espaço** | No game over: jogar outra vez                                                   |
| **Qualquer tecla** | No menu: iniciar partida                                                        |

A **barra de energia** sobe quando acertas asteroides com balas; influencia a cadência de tiro, o dash e o modo lento (**S**).

## Estrutura do projeto

```
AsteroidsUpdate/
├── assets/          # Sons + diagramas C4 (.png)
├── src/
│   ├── main.py      # Entrada: inicia Game
│   ├── game.py      # Loop, cenas (menu / jogo / game over), mixer, fullscreen
│   ├── systems.py   # World: colisões, ondas, UFO, pontuação
│   ├── sprites.py   # Ship, balas, asteroides, UFO
│   ├── config.py    # Constantes e caminhos para assets
│   └── utils.py     # Matemática, wrap do ecrã, desenho auxiliar
├── LICENSE
└── README.md
```

## Configuração

Ajustes de dificuldade, física, custos (hiperespaço, dash, energia) e volumes de áudio estão em [`src/config.py`](src/config.py). Os ficheiros de som esperados estão listados no topo desse mesmo ficheiro (pasta `assets/`).

## Arquitetura C4

Diagramas exportados do modelo C4 (ficheiros em [`assets/`](assets/)):

| Nível | Ficheiro |
|-------|----------|
| Contexto | `Arquitetura Asteroids - C4 Model - Context - Asteroids.png` |
| Contêiner | `Arquitetura Asteroids - C4 Model - Container - Asteroids.png` |
| Componentes | `Arquitetura Asteroids - C4 Model - Components - Asteroids.png` |

### Nível 1 — Contexto do sistema

O sistema é um **jogo desktop local** em que o jogador controla uma nave, destrói asteroides e sobrevive a ondas. Não há serviços externos nem rede.

![C4 — Contexto](assets/Arquitetura%20Asteroids%20-%20C4%20Model%20-%20Context%20-%20Asteroids.png)

### Nível 2 — Contêiner

Tudo corre num **único processo Python**. Os únicos “contêineres” lógicos são a **aplicação** e os **recursos em ficheiro**.

![C4 — Contêiner](assets/Arquitetura%20Asteroids%20-%20C4%20Model%20-%20Container%20-%20Asteroids.png)

### Nível 3 — Componentes 

Os módulos em `src/` formam camadas **procedimentais** (sem framework MVC pesado): ponto de entrada → orquestração de cena → mundo de jogo → entidades → utilitários e constantes.

![C4 — Componentes](assets/Arquitetura%20Asteroids%20-%20C4%20Model%20-%20Components%20-%20Asteroids.png)

## Licença

Este projeto está licenciado nos termos do ficheiro [LICENSE](LICENSE) (MIT).
