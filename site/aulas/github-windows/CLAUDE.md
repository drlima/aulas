# CLAUDE.md — aula `github-windows` (GitHub no Windows (Tech Challenge Fase 2))

Guia de consulta, em pt-BR, para o aluno sair do cadastro no GitHub e chegar ao
repositório do grupo no ar. Publicado em
https://drlima.github.io/aulas/aulas/github-windows/ (não há versão en).

As regras do repositório inteiro (camada compartilhada, API do core.js, i18n,
verificação, fluxo com o autor) estão no `CLAUDE.md` da raiz. Aqui fica só o que
vale para esta aula. `GUIA_DO_PROFESSOR.md` é o roteiro de uso em sala.

## Regras firmes, decididas com o autor

1. **Conteúdo intacto.** `CONTEUDO.md` é a fonte da verdade e está aprovado. Todo
   texto, comando, tabela e ordem de seções dele aparece no `index.html` exatamente
   como está. Permitido: converter Markdown em HTML semântico, linkar os domínios
   citados (abrem em nova aba) e rótulos curtos de interface ("Copiar", "Copiado",
   "Marcar como feito", "Limpar progresso"). **Proibido:** reescrever, resumir,
   reordenar, "melhorar" frases ou acrescentar dicas. Achou erro no conteúdo? Não
   corrija: registre e reporte ao autor. Mudou o `CONTEUDO.md` (só com o autor)?
   Regenere a página e rode o verificador.
2. **Formato: guia de consulta, não aula setup-punch.** Sem `div.q`, sem
   `details.reveal`, sem widget de chute, sem vocabulário progressivo.
3. **Só pt-BR.** Não existe `en/index.html`; o `aulas.json` declara
   `"idiomas": ["pt-BR"]` e não tem a chave `en`. Não crie a versão en.
4. **Sem Pyodide e sem verificador numérico.** Não há afirmação numérica a reconferir.
   O verificador desta aula é o de fidelidade de conteúdo.
5. Nenhuma menção a critérios de correção nem a pontuação na página, no
   `aulas.json` nem nos assets. O `verifica-github-windows.py` confere.
6. Sem JS a página fica completa: 5A, 5B e 5C aparecem em sequência. O mesmo vale
   na impressão. O `aula.js` só acrescenta comportamento; nunca esconde conteúdo
   que o HTML estático mostra, exceto as abas, e só depois de montá-las.
7. O `localStorage` só é usado por `safeStore` (do core); a página funciona sem ele.
8. Texto de interface só em `window.STR`, no HTML. Nenhum texto no JS.

## Estrutura

| id | Seção |
|---|---|
| s1 a s4 | passos 1 a 4 (a tabela do passo 4 é a da comparação) |
| s5 | contém o seletor `#tabs5` com os painéis `5a`, `5b`, `5c` (5A, 5B, 5C) |
| s6 a s10 | passos 6 a 10 (o checklist é o `ol#checklist` do passo 10) |
| erros | Erros comuns |

O seletor vem logo depois do texto do passo 4 (tabela, "Recomendado" e "O template
é o repositório…"), para não reordenar o conteúdo. 5A é a aba padrão. `#5b` e
`#5c` abrem a aba certa. A escolha fica em `aulas:github-windows:aba`, o progresso
em `aulas:github-windows:progresso`.

## Contrato de ids (lidos pelo `aula.js`)

`tabs5`, `checklist`, `toc`, `tocProg`, `tocTools`, mais `s1` a `s10`, `5a`, `5b`,
`5c`. Os ids `tab-5a`, `tab-5b` e `tab-5c` são criados pelo core (`tabSet`).
Os placeholders que o aluno troca ficam em `<span class="ph">` dentro do código:
`Seu Nome`, `email-da-conta-github`, `USUARIO`, `REPO`, `URL-COPIADA`,
`nome-do-repo`, `URL-DO-REPO`. Eles são copiados como estão.

## Antes do push

```bash
python3 scripts/check.py
python3 scripts/verifica-github-windows.py    # tem de terminar em TUDO BATE
python3 scripts/github-windows/testa_pagina.py --out <pasta de screenshots>
```
