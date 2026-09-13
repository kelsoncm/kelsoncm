# Windows Setup & Temas

Este diretório contém os scripts de provisionamento e configurações para ambiente Windows.

## Conteúdo

- `setup_user.ps1`: Script de automação para instalação de aplicativos via `winget`, `scoop`, fontes e configuração inicial do Oh My Posh.
- `apps.json`: Lista/definições de aplicativos para instalação.
- `themes/agnoster.omp.json`: Tema customizado do **Oh My Posh** baseado no `agnoster`, adicionando o segmento de **tempo de execução (`executiontime`)** com ícone `` e cores harmonizadas com a paleta pastel original.

---

## Como utilizar o tema no PowerShell

### Pré-requisitos
1. **Oh My Posh** instalado:
   ```powershell
   winget install JanDeDobbeleer.OhMyPosh -s winget
   ```
2. **Nerd Font** instalada (ex: MesloLGS NF):
   ```powershell
   oh-my-posh font install Meslo
   ```

---

### Opção 1: Direto pela URL do GitHub (Sem necessidade de clone local)

Adicione ao seu perfil do PowerShell (`notepad $PROFILE`):

```powershell
oh-my-posh init pwsh --config "https://raw.githubusercontent.com/kelsoncm/kelsoncm/refs/heads/main/bashscripts/windows/themes/agnoster.omp.json" | Invoke-Expression
```

---

### Opção 2: Utilizando arquivo local

Se você executou o `setup_user.ps1` ou baixou o tema para sua máquina:

```powershell
$theme = "$env:LOCALAPPDATA\Programs\oh-my-posh\themes\agnoster.omp.json"
oh-my-posh init pwsh --config $theme | Invoke-Expression
```

---

### Opção 3: Carregamento dinâmico com fallback (Recomendado para perfil portátil)

Se você sincroniza seu perfil via OneDrive ou repositório e coloca o `agnoster.omp.json` na mesma pasta do `$PROFILE`:

```powershell
$ompTheme = Join-Path (Split-Path $PROFILE) "agnoster.omp.json"
if (!(Test-Path $ompTheme)) {
    $ompTheme = "https://raw.githubusercontent.com/kelsoncm/kelsoncm/refs/heads/main/bashscripts/windows/themes/agnoster.omp.json"
}
oh-my-posh init pwsh --config $ompTheme | Invoke-Expression
```

Após editar, recarregue a sessão no terminal:
```powershell
& $PROFILE
```

---

## Executando o script de setup completo

Para instalar os aplicativos recomendados, ferramentas de desenvolvimento e configurar o tema automaticamente:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope Process
.\setup_user.ps1
```
