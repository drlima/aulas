# Guia do professor — GitHub no Windows (Tech Challenge Fase 2)

A página é um **guia de consulta**: o aluno a segue passo a passo, com você ao lado.
Não há perguntas nem Revelar. Este guia diz como usá-la em sala; ele não acrescenta
nada à página. Os tempos são estimativas (cerca de 60 min).

**Antes de começar:** peça que todos abram o link e usem o **Índice** (lateral no
computador; no celular, o botão "Índice" no topo). O botão **Copiar** de cada bloco
copia o comando; os trechos destacados em amarelo são do aluno e precisam ser
trocados antes de rodar. **Marcar como feito** e o checklist do passo 10 guardam o
progresso no próprio navegador; **Limpar progresso** zera tudo.

## Ordem sugerida

| Passo | Tempo | O que fazer em sala |
|---|---|---|
| Glossário e 1 | 5 min | Leia o glossário em voz alta. Cada um cria a conta e anota **usuário** e **e-mail**. |
| 2 | 10 min | Instalar na ordem da página: VS Code **antes** do Git. Confirmar com `git --version` no PowerShell. |
| 3 | 5 min | Os quatro comandos com o nome e o e-mail de cada um. |
| 4 | 5 min | Olhar a tabela juntos e escolher. A página recomenda *Use this template*. |
| 5 (A, B ou C) | 10 min | Só o **grupo**: quem é o dono cria o repositório. Use o seletor 5A / 5B / 5C; o link `#5b` ou `#5c` abre direto a opção. |
| 6 | 10 min | Todos clonam para `C:\projetos`, fora do OneDrive. Conferir com `git remote -v`. |
| 7 | 10 min | Um ciclo completo: editar, `git add .`, `git commit`, `git pull`, `git push`. |
| 8 | 5 min | O dono convida os colegas; cada colega aceita o convite e clona. Releia as regras de conflito. |
| 9 e 10 | fora da aula | Consulta para o Colab e para o checklist antes de entregar. |

## Onde os alunos costumam travar

Tudo abaixo já está na página; aponte a seção em vez de explicar de novo.

- **`git` não é reconhecido:** terminal aberto antes da instalação. Erros comuns, 1º item.
- **`Author identity unknown`:** o passo 3 não foi feito neste computador.
- **`rejected... fetch first`:** faltou `git pull` antes do `git push`.
- **`403` / `Permission denied` no push:** convite não aceito (passo 8) ou conta errada.
- **Repositório privado:** o passo 5A pede *Visibility: Public*; o passo 10 ensina a
  conferir em janela anônima.
- **Origem errada:** `git remote -v` no passo 6 deve mostrar o repo do **grupo**, não o do template.
- **Passo 5C:** o `dir` deve listar `README.md`; se não, o aluno entrou na pasta errada.
- **Trabalho em grupo (passo 8):** quem não atualiza com `git pull` antes de trabalhar
  gera conflito; dois alunos no **mesmo notebook** geram conflito difícil. Na tela do
  `CONFLICT`, mostre *Accept Current Change* e *Accept Incoming Change*, e `git merge --abort` para desistir.
- **Colab (passo 9):** depois de salvar pelo Colab, `git pull` no computador.

## Se algo der errado

- **Não abre o link do template:** a URL está no passo 4 (e abre em nova aba).
- **A página não lembra o progresso:** o navegador bloqueou o armazenamento; a página
  avisa. O guia continua valendo, só não guarda os "feitos".
- **Precisa de papel:** imprima a página; nela aparecem 5A, 5B e 5C completas, uma
  depois da outra.
