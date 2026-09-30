# Tutorial: GitHub no Windows (Tech Challenge Fase 2)

**Glossário:** *repo* = projeto no GitHub; *clonar* = copiar o repo para o computador; *commit* = versão salva; *push* / *pull* = enviar / baixar.

## 1. Criar conta no GitHub
Acesse github.com/signup e crie a conta. Anote o **usuário** (URL do repositório e convites) e o **e-mail** (passo 3).

## 2. Instalar as ferramentas
- **VS Code:** code.visualstudio.com (instale **antes** do Git).
- **Git:** git-scm.com/download/win → baixe o instalador de 64 bits. No instalador, clique *Next* em tudo, exceto **Editor padrão: Visual Studio Code**.
- **GitHub Desktop:** desktop.github.com → depois *File → Options → Accounts → Sign in*.
- **Google Colab:** não instala nada, basta uma conta Google.

Confirme a instalação abrindo o **PowerShell** e rodando `git --version`.

Na primeira vez que você enviar arquivos ao GitHub (push), abre uma janela do navegador para você entrar na sua conta. O GitHub não aceita mais senha no terminal.

## 3. Configurar sua identidade (uma vez por computador)
```
git config --global user.name "Seu Nome"
git config --global user.email "email-da-conta-github"
git config --global init.defaultBranch main
git config --global pull.rebase false
```

## 4. Escolher como obter o template

| | Use this template | Fork | Download ZIP |
|---|---|---|---|
| Repo novo na sua conta | Sim | Sim | Só depois de criar manualmente |
| Histórico | Limpo (1 commit) | Herda o original | Nenhum |
| Vínculo com o original | Não | Sim | Não |
| Receber correções do professor | Copiar à mão | `git pull upstream main` | Copiar à mão |
| Dificuldade | Baixa | Baixa | Alta |

**Recomendado:** *Use this template*. Use Fork se quiser receber atualizações do template. Use ZIP só se não conseguir das outras formas.

O template é o repositório https://github.com/drlima/postech-tech-challenge-fase2-template. Escolha **uma** opção (5A, 5B ou 5C).

## 5A. Use this template (recomendado)
1. Abra o repositório do template e clique em **Use this template → Create a new repository**.
2. Preencha:
   - **Owner:** sua conta.
   - **Name:** por exemplo `tech-challenge-fase2-grupoXX`.
   - **Visibility: Public.** O professor não consegue acessar repositórios privados.
3. Clique em **Create repository**.

## 5B. Fork
1. No template, clique em **Fork** (canto superior direito) → **Create fork**.
2. Abra a aba **Actions** do seu fork e clique em **I understand my workflows, go ahead and enable them**. Em forks, os workflows vêm desativados.
3. Opcional, para receber atualizações do template, **depois de clonar (passo 6)**, na pasta do repo:
```
git remote add upstream https://github.com/drlima/postech-tech-challenge-fase2-template.git
git pull upstream main
```

## 5C. Download ZIP
1. No template, clique em **Code → Download ZIP**, use *Extrair tudo* e, em "Destino", digite apenas `C:\projetos`.
2. No GitHub, clique em **New repository**, use o nome sugerido na 5A (por exemplo `tech-challenge-fase2-grupoXX`) e marque **Public**. **Não** marque README, .gitignore nem License.
3. No PowerShell:
```
cd C:\projetos\postech-tech-challenge-fase2-template-main
dir
```
O `dir` deve listar `README.md`; se não, entre na subpasta com `cd`. Depois:
```
git init -b main
git add .
git commit -m "Primeiro commit"
git remote add origin https://github.com/USUARIO/REPO.git
git push -u origin main
```
No GitHub Desktop, **em vez dos passos 2 e 3**: *File → Add local repository → create a repository → Create repository → Commit to main → Publish repository*, desmarcando "Keep this code private".

## 6. Clonar para o seu computador (5A e 5B)
No repositório, clique em **Code → HTTPS** e copie a URL.

**PowerShell:**
```
mkdir -Force C:\projetos
cd C:\projetos
git clone URL-COPIADA
cd nome-do-repo
code .
```
Evite pastas sincronizadas com o OneDrive, como *Documentos* e *Área de Trabalho*.

**GitHub Desktop:** *File → Clone repository → GitHub.com →* escolha o repo, mude *Local path* para `C:\projetos\nome-do-repo` → *Clone*.

Confirme com `git remote -v`: o endereço do **`origin`** deve ser o do repo do **seu grupo**, nunca o do template.

## 7. Rotina de trabalho
Edite os arquivos no VS Code. Os dados brutos ficam **só** em `data/raw/` e **não** vão para o Git, conforme `data/README.md`. O repositório é público: não coloque senhas nem chaves de API.

**PowerShell** (no VS Code: *Terminal → New Terminal*, que já abre na pasta do repo). Ao começar a trabalhar, rode `git pull`. Para enviar:
```
git add .
git commit -m "descreva o que mudou"
git pull
git push
```
**VS Code:** ícone *Source Control* (`Ctrl+Shift+G`) → mensagem → **Commit** → **Sync Changes**.

**GitHub Desktop:** **Fetch origin** e, se aparecer, **Pull origin** (ao começar e antes do push); depois mensagem em *Summary* → **Commit to main** → **Push origin**.

O ✗ na aba **Actions** é esperado até você preencher o `README.md` e o `submissao/entrega.json`.

## 8. Trabalho em grupo (1 a 5 integrantes)
Um integrante é o dono do repositório. Só ele cria o repo pelo passo 5 e convida os demais:
1. Ele abre **Settings → Collaborators → Add people** e digita o usuário de cada colega.
2. Cada colega aceita o convite em até 7 dias (chega por e-mail).
3. Cada colega faz os passos 1 a 3 (se ainda não fez) e clona o repo do grupo (passo 6).

Regras para evitar conflito:
- Rode `git pull` **antes** de começar a trabalhar e antes de cada push.
- Faça commits pequenos e frequentes.
- Não edite o **mesmo notebook** ao mesmo tempo. Arquivos `.ipynb` geram conflitos difíceis de resolver.
- Se o push for rejeitado, rode `git pull` (se abrir uma aba de mensagem, salve e feche). Se avisar `CONFLICT`, abra o arquivo no VS Code, escolha **Accept Current Change** (a sua) ou **Accept Incoming Change** (a do colega), salve e rode `git add .`, `git commit -m "resolve conflito"` e `git push`. Para desistir: `git merge --abort`.

## 9. Google Colab
- **Abrir:** *File → Open notebook → aba GitHub →* cole a URL do repo → escolha o notebook. O Colab abre só o notebook: na primeira célula, `!git clone URL-DO-REPO` e `%cd nome-do-repo/notebooks`; envie o dataset para `nome-do-repo/data/raw/` pelo painel *Arquivos*.
- **Salvar no repo:** *File → Save a copy in GitHub* → escolha o repo e escreva a mensagem de commit.
- Depois de salvar pelo Colab, rode `git pull` no computador antes de continuar.

## 10. Antes de entregar
1. Abra o link do repositório em uma **janela anônima**. Ele precisa abrir sem login; se aparecer **404** ou pedir login, o repositório está privado e o professor não conseguirá vê-lo. Corrija em *Settings → General → Danger Zone → Change visibility → Public*.
2. Preencha o `README.md`, apague o bloco `> **INSTRUÇÕES:**` e busque `PREENCHER` (`Ctrl+Shift+F`) até não restar nenhum.
3. Percorra o `CHECKLIST.md`.
4. Gere o PDF de submissão conforme `submissao/README.md` e confirme que o link do repo no README é **idêntico** ao do PDF.

## Erros comuns
- **`git` não é reconhecido:** feche e reabra o terminal. Se persistir, reinstale o Git.
- **`Author identity unknown`:** refaça o passo 3.
- **`rejected... fetch first`:** rode `git pull` e depois `git push`.
- **`403` / `Permission denied` no push:** aceite o convite do repo e use a conta certa.
