[![CI do portfólio](https://github.com/gustavobarcelos18/trabalho_esteira_devops/actions/workflows/ci.yml/badge.svg)](https://github.com/gustavobarcelos18/trabalho_esteira_devops/actions/workflows/ci.yml)
[![Deploy do portfólio](https://github.com/gustavobarcelos18/trabalho_esteira_devops/actions/workflows/deploy.yml/badge.svg)](https://github.com/gustavobarcelos18/trabalho_esteira_devops/actions/workflows/deploy.yml)

# Portfólio de Gustavo Barcelos

Portfólio de [Gustavo Barcelos](https://github.com/gustavobarcelos18) para o trabalho prático de CI/CD. A página usa HTML e CSS e apresenta os projetos TaskHub, DataFlow, Gestão de Almoxarifado e esta esteira de publicação. O deploy é feito pelo [GitHub Pages](https://gustavobarcelos18.github.io/trabalho_esteira_devops/).

- `index.html`, `style.css` e `imagens/` contêm os arquivos públicos.
- [CI](.github/workflows/ci.yml) roda em pull requests para `main`. Cada job verifica primeiro o `index.html`, usa `find` para barrar arquivos acima de 500.000 bytes e verifica os termos proibidos no código do site. A matriz roda o validador HTML em Node.js 18 e 20. O script Python verifica referências de links e imagens, incluindo caminhos locais, âncoras e respostas HTTP de URLs externas. O job `CI Gate` exige o sucesso de toda a matriz.
- [Deploy](.github/workflows/deploy.yml) publica os arquivos do site após cada push na `main`. As notificações de falha são configuradas nas preferências pessoais do GitHub Actions.

## 1. Suba os arquivos e habilite o Pages

1. Coloque estes arquivos na raiz do [repositório do trabalho](https://github.com/gustavobarcelos18/trabalho_esteira_devops). Se você já salvou um workflow de deploy de teste chamado `static.yml`, remova-o ao adotar `deploy.yml` para manter um único fluxo de publicação.
2. Em [Settings → Pages](https://github.com/gustavobarcelos18/trabalho_esteira_devops/settings/pages), em **Build and deployment → Source**, escolha **GitHub Actions**.
3. Em [Actions](https://github.com/gustavobarcelos18/trabalho_esteira_devops/actions), abra **Deploy do portfólio**. Se você habilitou o Pages depois do primeiro commit, use **Run workflow → main → Run workflow** para iniciar a publicação.

Se estiver usando a pasta local `portfolio` com o commit e o remoto já preparados, publique pelo PowerShell nessa pasta. Autorize a conta `gustavobarcelos18` no navegador quando solicitado.

```powershell
git credential-manager github login --username gustavobarcelos18
git -c credential.username=gustavobarcelos18 push -u origin main
```

## 2. Execute a CI e proteja a main

1. Crie a branch `demonstracao-ci` a partir da `main`. Faça uma mudança válida no HTML, como trocar o título de um projeto, e abra um pull request com **base: main**. Aguarde os dois jobs da matriz e o **CI Gate** ficarem verdes.
2. Abra [Settings → Branches](https://github.com/gustavobarcelos18/trabalho_esteira_devops/settings/branches) e adicione uma regra de proteção para `main`.
3. Marque **Require a pull request before merging**. Marque **Require status checks to pass before merging** e selecione **CI Gate**. Marque **Do not allow bypassing the above settings** se a interface exibir essa opção. Para um trabalho individual, deixe **Require approvals** desmarcado. Salve.
4. No mesmo PR, edite o `index.html` da branch de demonstração e adicione um `<img alt="Teste">` dentro do `main`. O linter exige o atributo `src`. Aguarde a falha e confirme no PR que o merge foi bloqueado.
5. Abra a execução vermelha em **Actions**, expanda **Validar HTML** em um dos jobs da matriz e tire um print com o erro. Remova a tag de teste na mesma branch e confirme que o **CI Gate** ficou verde novamente.
6. Faça o merge do PR depois dos checks passarem. Abra a execução de **Deploy do portfólio** referente ao merge e tire o print do deploy verde. Abra a URL pública e confira que a mudança está visível.

## 3. Configure a notificação de falha

1. Siga o [repositório do trabalho](https://github.com/gustavobarcelos18/trabalho_esteira_devops) pelo botão **Watch**.
2. Abra as [preferências de notificações do GitHub](https://github.com/settings/notifications). Em **System → Actions**, selecione **On GitHub** para receber os avisos na caixa de entrada. Se precisar receber o aviso fora da interface, selecione também **Email** para que o próprio GitHub envie o aviso.
3. Marque **Only notify for failed workflows** e salve. A preferência vale para as execuções que você dispara, incluindo o deploy iniciado pelo push resultante do merge. [Documentação das notificações do GitHub Actions](https://docs.github.com/en/subscriptions-and-notifications/how-tos/managing-github-actions-notifications)

## 4. Convide a colaboradora e entregue

1. Em [Settings → Collaborators](https://github.com/gustavobarcelos18/trabalho_esteira_devops/settings/access), clique em **Add people** e convide `09116428-collab`. Confirme o usuário selecionado antes de enviar.
2. Entregue o link do repositório com `.github/workflows/`, o print da CI vermelha por erro no HTML, o print do deploy verde e a URL pública. Confirme também que o convite aparece na seção de acesso do repositório.

## Executar no computador

```sh
npm ci
npm run lint:html -- index.html
python scripts/verificar-links.py
```

Para o script de referências, use Python 3.9 ou mais recente e uma conexão com a internet.
