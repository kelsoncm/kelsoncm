# Guia de boas práticas para desenvolvimento de plugins Moodle

Este documento consolida as melhores práticas para desenvolvimento de plugins Moodle profissionais, baseado na análise de projetos reais bem-sucedidos, especialmente o **tiny_justify** como caso de estudo. O objetivo é fornecer um roteiro completo para criar plugins de alta qualidade, manuteníveis e seguros desde o início do projeto.

---

# Índice
- [Guia de boas práticas para desenvolvimento de plugins Moodle](#guia-de-boas-práticas-para-desenvolvimento-de-plugins-moodle)
- [Índice](#índice)
- [1. Visão Geral](#1-visão-geral)
  - [1.1. Princípios Fundamentais](#11-princípios-fundamentais)
  - [1.2. Por Que Isso Importa?](#12-por-que-isso-importa)
  - [1.3. Fundação inicial](#13-fundação-inicial)
- [2. Documentação](#2-documentação)
  - [2.1. `CHANGELOG.md`](#21-changelogmd)
  - [2.2. `CONTRIBUTING.md`](#22-contributingmd)
  - [2.3. `README.md`](#23-readmemd)
  - [2.4. `SECURITY.md`](#24-securitymd)
      - [Exemplo Mínimo de SECURITY.md](#exemplo-mínimo-de-securitymd)
- [3. CI/CD](#3-cicd)
  - [3.1. `.github/dependabot.yml`](#31-githubdependabotyml)
    - [3.1.1 Configuração Básica:](#311-configuração-básica)
    - [3.1.2 Configuração Avançada\*\*:](#312-configuração-avançada)
  - [3.2. `.github/workflows/moodle-plugin-ci.yml`](#32-githubworkflowsmoodle-plugin-ciyml)
    - [3.2.1 Exemplo de matrix de testes](#321-exemplo-de-matrix-de-testes)
    - [3.2.2. Exemplo completo](#322-exemplo-completo)
  - [3.3. `.github/workflows/release.yml`](#33-githubworkflowsreleaseyml)
    - [3.3.1 Workflow Completo](#331-workflow-completo)
    - [3.3.2 Workflow de Release](#332-workflow-de-release)
- [4. Tests](#4-tests)
  - [4.1. Behat Tests (Integration/E2E) ⭐ Essencial](#41-behat-tests-integratione2e--essencial)
  - [4.2. PHPUnit Tests (Unit/Component) 🔧 Recomendado](#42-phpunit-tests-unitcomponent--recomendado)
    - [4.2.1. Estrutura de Diretório:](#421-estrutura-de-diretório)
    - [4.2.2. Template Test Class:](#422-template-test-class)
    - [4.2.3. Running PHPUnit Locally:](#423-running-phpunit-locally)
  - [4.3. JavaScript/AMD Tests 🧪 Opcional](#43-javascriptamd-tests--opcional)
    - [4.3.1. Estrutura:](#431-estrutura)
    - [4.3.2. Template Test:](#432-template-test)
    - [4.3.3. Exemplo Real (tiny\_justify):](#433-exemplo-real-tiny_justify)
- [5. Versionamento e Releases](#5-versionamento-e-releases)
  - [5.1. Sistema de Versionamento Duplo](#51-sistema-de-versionamento-duplo)
  - [5.2. Sincronização de Versões](#52-sincronização-de-versões)
  - [5.3. Tags Git e Releases](#53-tags-git-e-releases)
  - [5.4. Conventional Commits](#54-conventional-commits)
    - [5.4.1. Formato:](#541-formato)
    - [5.4.2. Tipos Comuns:](#542-tipos-comuns)
    - [5.4.3. Exemplos Reais (tiny\_justify):](#543-exemplos-reais-tiny_justify)
    - [5.4.4. Benefícios:](#544-benefícios)
  - [5.5. Fluxo Completo de Release](#55-fluxo-completo-de-release)
- [6. Git Workflow e Branching](#6-git-workflow-e-branching)
  - [6.1. Estratégia de Branching (Trunk-Based Development)](#61-estratégia-de-branching-trunk-based-development)
    - [Estrutura de Branches:](#estrutura-de-branches)
    - [Naming Convention:](#naming-convention)
  - [6.2. GitHub Branch Protection Rules](#62-github-branch-protection-rules)
    - [Exemplo CODEOWNERS:](#exemplo-codeowners)
- [7. .gitignore Padrão para Plugins Moodle](#7-gitignore-padrão-para-plugins-moodle)
- [8. Code Review Best Practices](#8-code-review-best-practices)
  - [8.1. Para Autores de PR](#81-para-autores-de-pr)
  - [8.2. Para Reviewers](#82-para-reviewers)
- [9. Pre-Release Checklist](#9-pre-release-checklist)
  - [9.1. Antes de fazer uma release\*\*:](#91-antes-de-fazer-uma-release)
  - [9.2. Release Script Rápido](#92-release-script-rápido)
- [10. Referências](#10-referências)
- [11. Backup/Restore](#11-backuprestore)
  - [11.1. Matriz de Recomendações por Tipo de Plugin](#111-matriz-de-recomendações-por-tipo-de-plugin)
  - [11.2. Estrutura de Arquivos](#112-estrutura-de-arquivos)
  - [11.3. Arquivo `backup_plugintype_pluginname_activity.class.php`](#113-arquivo-backup_plugintype_pluginname_activityclassphp)
  - [11.4. Arquivo `restore_plugintype_pluginname_activity.class.php`](#114-arquivo-restore_plugintype_pluginname_activityclassphp)
- [12. External Service (API WEB SERVICE)](#12-external-service-api-web-service)
  - [12.1. Estrutura de Arquivos](#121-estrutura-de-arquivos)
  - [12.2. Arquivo `db/services.php`](#122-arquivo-dbservicesphp)
  - [12.3. Arquivo `classes/external/api.php`](#123-arquivo-classesexternalapiphp)
  - [12.4. Ativar o Web Service](#124-ativar-o-web-service)
  - [12.5. Chamar Web Service (Exemplo REST)](#125-chamar-web-service-exemplo-rest)
- [13. Tasks (Cron Jobs)](#13-tasks-cron-jobs)
  - [13.1. Arquivo `db/tasks.php`](#131-arquivo-dbtasksphp)
  - [13.2. Scheduled Task Class](#132-scheduled-task-class)
  - [13.3. Ad Hoc Task Class](#133-ad-hoc-task-class)
  - [13.4. Executar Ad Hoc Task Programaticamente](#134-executar-ad-hoc-task-programaticamente)
  - [13.5. Cleanup Task (Exemplo Prático)](#135-cleanup-task-exemplo-prático)
- [14. Capabilities (Permissões)](#14-capabilities-permissões)
  - [14.1. Arquivo `db/access.php`](#141-arquivo-dbaccessphp)
  - [14.2. Usando Capabilities no Código](#142-usando-capabilities-no-código)
  - [14.3. Nomes Convention para Capabilities](#143-nomes-convention-para-capabilities)
  - [14.4. Context Levels](#144-context-levels)
  - [14.5. Captype (Tipo de Permission)](#145-captype-tipo-de-permission)
- [15. Versão e Finalização](#15-versão-e-finalização)
  - [15.1. Checklist de Rastreabilidade](#151-checklist-de-rastreabilidade)
  - [15.2. Iteração Contínua](#152-iteração-contínua)

# 1. Visão Geral

## 1.1. Princípios Fundamentais

Um plugin Moodle moderno e profissional deve seguir estes princípios desde o primeiro commit:

1. ✅ **Infraestrutura primeiro, código depois** - CI/CD não é opcional
2. ✅ **Testes múltiplos níveis** - Unit, integration, e2e
3. ✅ **Documentação viva** - `CHANGELOG.md`, `CONTRIBUTING.md`, `README.md`, `SECURITY.md` e `LICENSE.md`
4. ✅ **Automação de releases** - Zero erros humanos
5. ✅ **Versionamento consistente** - Semântico + timestamp
6. ✅ **Segurança by design** - Capabilities, sanitization, prepared statements
7. ✅ **Commits descritivos** - Conventional Commits  

## 1.2. Por Que Isso Importa?

| Aspecto              | Sem Boas Práticas                  | Com Boas Práticas        |
| -------------------- | ---------------------------------- | ------------------------ |
| **Confiabilidade**   | Bugs em produção                   | Detectados em CI         |
| **Manutenibilidade** | Código legado em 6 meses           | Código vivo após anos    |
| **Onboarding**       | Dias explorando código             | Horas lendo docs         |
| **Releases**         | Processo manual, propensa a erros  | Automático, consistente  |
| **Compatibilidade**  | Quebra em novas versões Moodle     | Testado contra matrix    |
| **Segurança**        | Vulnerabilidades descobertas tarde | Preventiva e documentada |


## 1.3. Fundação inicial

**Instrução crítica**: Criar infraestrutura de CI/CD **no primeiro commit**, não depois.

| Categoria | Arquivos                                       |
| --------- | ---------------------------------------------- |
| CI/CD     | `.github/workflows/`, `.github/dependabot.yml` |
| Código    | `classes/`, `amd/src/`                         |
| Testes    | `tests/behat/`, `tests/javascript/`            |
| Database  | `db/install.php`, `db/upgrade.php`             |
| Lang      | `lang/en/`, `lang/pt_br/`                      |
| Config    | `version.php`, `styles.css`, `pix/`            |

# 2. Documentação

**Instrução crítica**: A documentação é crítica e deve ser criada no **primeiro commit**, não como afterthought, e atualizadas a cada iteração, sendo o mínimo:
1. ✅ `CHANGELOG.md`
2. ✅ `CONTRIBUTING.md`
3. ✅ `README.md`
4. ✅ `SECURITY.md`
5. ✅ `LICENSE.md` - Necessariamente em GPLv3

## 2.1. `CHANGELOG.md`

**O que é**: Histórico estruturado de todas as mudanças por versão.

**Por que é crítico**:
- Rastreabilidade de mudanças ao longo do tempo
- Ajuda usuários a entender impacto de atualizações
- Facilita debugging ("quando esse comportamento mudou?")
- Padrão internacional ([Keep a Changelog](https://keepachangelog.com/))

**Template Inicial**:
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

# [Unreleased]

### Added
- Feature A in progress
- Feature B planned

## [1.0.0] - 2026-03-04

### Added
- Initial release
- Main functionality X
- Support for Moodle 4.5-5.1

### Fixed
- Bug in edge case Y

### Security
- Input sanitization implemented
```

**Seções Padrão**: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`

**Exemplo Real (tiny_justify)**:
```markdown
## [1.0.21] - 2026-03-03
### Fixed
- Align plugin with Moodle contribution checklist
- Update PostgreSQL to version 15
- Add support for PHP 8.4 and Moodle 5.1
```

## 2.2. `CONTRIBUTING.md`

**O que é**: Guia completo para contribuidores externos e futuros mantenedores.

**Seções Obrigatórias**:

1. Overview
2. How to Contribute
3. Reporting Bugs
4. Suggesting Features
5. Code Style
6. Development Workflow (crítico!)
7. Troubleshooting
8. License

> Code style example:
>    1. Links:
>       1. [Moodle Coding style](https://moodledev.io/general/development/policies/codingstyle)
>       2. [Moodle Accessibility Guide](https://moodledev.io/general/development/policies/accessibility)
>    1. Tools:
>       1. PHP Lint: `phplint`
>       2. PHP Copy/Paste Detector: `phpcpd`
>       3. PHP Mess Detector: `phpmd`
>       4. Moodle Code Checker: `codechecker`
>       5. Moodle PHPDoc Checker: `phpdoc`
>       6. Validating: `validate`
>       7. Check upgrade savepoints: `savepoints`
>       8. Mustache Lint: `mustache`

## 2.3. `README.md`

1. Overview
2. Requirements
3. Installation
4. Configuration
5. Usage
6. License
7. Contributing
8. Support

## 2.4. `SECURITY.md`

**O que é**: Documento de segurança que descreve práticas e vulnerabilidades do plugin.

**Quando é essencial**:
- ✅ Plugin manipula dados de usuário
- ✅ Plugin executa queries SQL
- ✅ Plugin lida com capabilities/permissões
- ✅ Plugin aceita uploads de arquivos
- ✅ Plugin processa dados externos

**Quando é opcional, ainda que recomendado**:
- ⚠️ Plugin puramente visual (botões de editor, temas simples)
- ⚠️ Plugin read-only sem lógica de negócio

**Seções Obrigatórias**:

1. **Supported Versions** - Quais versões do Moodle, PHP, database são suportadas
2. **Security Properties** - Quais capacidades, validações e controles estão implementados
3. **Security Considerations** - Análise de riscos e mitigações (SQL injection, XSS, CSRF)
4. **Security Best Practices for Developers** - Como contribuir com segurança em mente
5. **Security Best Practices for Administrators** - Como instalar, configurar e monitorar
6. **Dependencies** - Versões mínimas obrigatórias do Moodle, PHP, database
7. **Test Matrix** - Quais combinações são testadas
8. **Reporting a Vulnerability** - Como reportar sem criar issues públicas
9. **License** - GPLv3
10. **Contact & Support** - Onde encontrar help

#### Exemplo Mínimo de SECURITY.md

```markdown
# Security Policy

## Supported Versions

| Version | Support Status     | Until      |
| ------- | ------------------ | ---------- |
| 1.0.20+ | Actively Supported | 2027-03-04 |
| 1.0.0   | End of Life        | 2025-12-31 |

## Security Properties

- **Capabilities**: Uses `moodle/course:viewparticipants` for access control
- **Input Validation**: All user inputs validated using `required_param()` and `optional_param()`
- **Database Queries**: All DB queries use parameterized statements via `$DB->prepare()`

## Security Considerations

- **SQL Injection**: Mitigated through parameterized queries
- **XSS**: Mitigated through Moodle's output filtering
- **CSRF**: Mitigated through Moodle's CSRF tokens

## Reporting a Vulnerability

**DO NOT** create a GitHub issue for security vulnerabilities.

Email: security@example.com

Include:
- Description
- Steps to reproduce
- Potential impact
- Affected versions

We respond within 48 hours and patch critical issues within 7 days.
```

# 3. CI/CD

## 3.1. `.github/dependabot.yml`

**Por que é importante**: Mantém dependências seguras automaticamente.

### 3.1.1 Configuração Básica:
```yaml
version: 2
updates:
  - package-ecosystem: "composer"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

### 3.1.2 Configuração Avançada**:
```yaml
version: 2
updates:
  - package-ecosystem: "composer"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
    labels:
      - "dependencies"
      - "composer"
    reviewers:
      - "maintainer-username"
    commit-message:
      prefix: "chore"
      include: "scope"
```


## 3.2. `.github/workflows/moodle-plugin-ci.yml`

**Objetivo**: Testar plugin contra múltiplas versões de Moodle, PHP e databases automaticamente.

### 3.2.1 Exemplo de matrix de testes

| PHP | Moodle 4.5 | Moodle 5.0 | Moodle 5.1 | Databases      |
| --- | ---------- | ---------- | ---------- | -------------- |
| 8.1 | ✅          | ❌          | ❌          | pgsql, mariadb |
| 8.2 | ✅          | ✅          | ✅          | pgsql, mariadb |
| 8.3 | ✅          | ✅          | ✅          | pgsql, mariadb |
| 8.4 | ❌          | ✅          | ✅          | pgsql, mariadb |

**Resultado**: ~20 combinações testadas automaticamente em cada push! Tempo total ~5min, se fosse linear seria ~120min.

### 3.2.2. Exemplo completo

```yaml
name: Moodle Plugin CI

on:
  push:
    branches: [main, MOODLE_*]
  pull_request:
    branches: [main, MOODLE_*]

permissions:
  contents: read

jobs:
  test:
    name: Moodle ${{ matrix.moodle-branch }} / PHP ${{ matrix.php }} / DB ${{ matrix.database }}
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_HOST_AUTH_METHOD: trust
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    strategy:
      fail-fast: true
      matrix:
        php: ['8.1', '8.2', '8.3', '8.4']
        moodle-branch: ['MOODLE_405_STABLE', 'MOODLE_500_STABLE', 'MOODLE_501_STABLE']
        database: [pgsql, mariadb]
        include:
          - database: mariadb
            service: mariadb
        exclude:
          # PHP 8.4 não suportado em Moodle 4.5
          - moodle-branch: 'MOODLE_405_STABLE'
            php: '8.4'
          # PHP 8.1 não suportado em Moodle 5.0+
          - moodle-branch: 'MOODLE_500_STABLE'
            php: '8.1'
          - moodle-branch: 'MOODLE_501_STABLE'
            php: '8.1'

    steps:
      - name: Check out repository code
        uses: actions/checkout@v4
        with:
          path: plugin

      - name: Setup PHP ${{ matrix.php }}
        uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php }}
          extensions: mbstring, pdo, pdo_pgsql, pgsql, mysqli, gd, intl, xml, zip, curl
          ini-values: max_input_vars=5000
          coverage: none

      - name: Start MariaDB service
        if: matrix.database == 'mariadb'
        run: |
          docker run -d \
            --name mariadb \
            -e MYSQL_ALLOW_EMPTY_PASSWORD=yes \
            -e MYSQL_CHARACTER_SET_SERVER=utf8mb4 \
            -e MYSQL_COLLATION_SERVER=utf8mb4_unicode_ci \
            -p 3306:3306 \
            mariadb:10.11
          sleep 10

      - name: Initialise moodle-plugin-ci
        run: |
          composer create-project -n --no-dev --prefer-dist \
            moodlehq/moodle-plugin-ci ci ^4
          echo "$(cd ci && pwd)/bin" >> $GITHUB_PATH
          echo "$(cd ci && pwd)/vendor/bin" >> $GITHUB_PATH
          sudo locale-gen en_AU.UTF-8

      - name: Install moodle-plugin-ci
        run: moodle-plugin-ci install --plugin ./plugin --db-host=127.0.0.1
        env:
          DB: ${{ matrix.database }}
          MOODLE_BRANCH: ${{ matrix.moodle-branch }}

      - name: PHP Lint
        if: ${{ !cancelled() }}
        run: moodle-plugin-ci phplint

      - name: PHP Mess Detector
        if: ${{ !cancelled() }}
        run: moodle-plugin-ci phpmd

      - name: Moodle Code Checker
        if: ${{ !cancelled() }}
        run: moodle-plugin-ci codechecker --max-warnings 0

      - name: Moodle PHPDoc Checker
        if: ${{ !cancelled() }}
        run: moodle-plugin-ci phpdoc --max-warnings 0

      - name: Validations
        if: ${{ !cancelled() }}
        run: moodle-plugin-ci validate

      - name: Check upgrade savepoints
        if: ${{ !cancelled() }}
        run: moodle-plugin-ci savepoints

      - name: Mustache Lint
        if: ${{ !cancelled() }}
        run: moodle-plugin-ci mustache

      - name: Grunt
        if: ${{ !cancelled() }}
        run: moodle-plugin-ci grunt --max-lint-warnings 0

      - name: PHPUnit tests
        if: ${{ !cancelled() }}
        run: moodle-plugin-ci phpunit --fail-on-warning

      - name: Behat features
        if: ${{ !cancelled() }}
        run: moodle-plugin-ci behat --profile chrome
```

## 3.3. `.github/workflows/release.yml`

**Objetivo**: Automatizar criação de releases, empacotamento ZIP, e upload para GitHub Releases e para Moodle Plugin Directory.

**Validações Implementadas**:
1. ✅ `$plugin->version` últimos 2 dígitos == `$plugin->release` últimos 2 dígitos
2. ✅ `$plugin->release` == git tag name
3. ✅ ZIP contém estrutura correta de diretório
4. ✅ Upload confirma sucesso antes de marcar release

### 3.3.1 Workflow Completo

```yaml
name: Release

on:
  push:
    tags:
      - '*'

jobs:
  release:
    name: Build and release plugin ZIP
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Extract and validate plugin version
        id: version
        run: |
          VERSION=$(grep -oP '\$plugin->version\s*=\s*\K[0-9]+' version.php)
          RELEASE=$(grep -oP "\\\$plugin->release\s*=\s*'\K[^']+" version.php)

          VERSION_SUFFIX="${VERSION: -2}"
          RELEASE_SUFFIX="${RELEASE##*.}"

          echo "Plugin version: $VERSION (suffix: $VERSION_SUFFIX)"
          echo "Plugin release: $RELEASE (suffix: $RELEASE_SUFFIX)"

          TAG="${GITHUB_REF_NAME#v}"

          echo "Tag (sem prefixo v): $TAG"

          # Validação 1: Últimos 2 dígitos devem corresponder
          if [ "$VERSION_SUFFIX" != "$RELEASE_SUFFIX" ]; then
            echo "::error::Version/release suffix mismatch"
            exit 1
          fi

          # Validação 2: Release deve corresponder à tag
          if [ "$RELEASE" != "$TAG" ]; then
            echo "::error::Release ($RELEASE) doesn't match tag ($TAG)"
            exit 1
          fi

          echo "number=$VERSION" >> "$GITHUB_OUTPUT"

      - name: Build plugin ZIP
        id: build
        env:
          PLUGIN_NAME: ${{ github.event.repository.name }}
        run: |
          mkdir -p /tmp/build/$PLUGIN_NAME

          rsync -a \
            --exclude='.git' \
            --exclude='.github' \
            --exclude='node_modules' \
            --exclude='.gitignore' \
            --exclude='tests' \
            --exclude='vendor' \
            . /tmp/build/$PLUGIN_NAME/

          cd /tmp/build
          zip -r "$GITHUB_WORKSPACE/$PLUGIN_NAME-${{ steps.version.outputs.number }}.zip" $PLUGIN_NAME/
          echo "zipfile=$PLUGIN_NAME-${{ steps.version.outputs.number }}.zip" >> "$GITHUB_OUTPUT"

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: ${{ steps.build.outputs.zipfile }}
          generate_release_notes: true

      - name: Upload to Moodle Plugin Directory
        if: ${{ secrets.MOODLE_DIRECTORY_TOKEN != '' }}
        env:
          MOODLE_DIRECTORY_TOKEN: ${{ secrets.MOODLE_DIRECTORY_TOKEN }}
          PLUGIN_NAME: ${{ github.event.repository.name }}
        run: |
          ZIPFILE="${PLUGIN_NAME}-${{ steps.version.outputs.number }}.zip"
          
          RESPONSE=$(curl -s -w "\n%{http_code}" \
            -F data=@"$GITHUB_WORKSPACE/$ZIPFILE" \
            "https://moodle.org/webservice/upload.php?token=$MOODLE_DIRECTORY_TOKEN")

          HTTP_CODE=$(echo "$RESPONSE" | tail -1)
          BODY=$(echo "$RESPONSE" | sed '$d')

          echo "HTTP status: $HTTP_CODE"
          echo "Response: $BODY"

          if [ "$HTTP_CODE" -ne 200 ] || echo "$BODY" | grep -q '"error"'; then
            echo "::error::Failed to upload to Moodle Plugin Directory"
            exit 1
          fi
          
          echo "✅ Successfully published to Moodle Plugin Directory"
```

### 3.3.2 Workflow de Release

**1. Update `version.php`**

```php
$plugin->version  = 2026030401;  # YYYYMMDDRR
$plugin->release  = '1.0.1';     # Semantic
```

**2. Update `CHANGELOG.md`**

Acrescente ao início do arquivo:

```markdown
## [1.0.1] - 2026-03-04
### Fixed
- Bug fix description ....

```

**3. Commit**

```bash
git add version.php CHANGELOG.md
git commit -m "chore: bump version to 1.0.1"
```

**4. Tag (trigger release workflow)**

```bash
git tag -a 1.0.1 -m "Release 1.0.1"
git push origin main --tags
```

**5. Automatic: CI tests run, ZIP created, release published**

> **Objetivo**: Zero erros humanos em releases!


# 4. Tests 

## 4.1. Behat Tests (Integration/E2E) ⭐ Essencial

**O que são**: Testes de integração em linguagem natural (Gherkin) que validam fluxos completos de usuário.

**Estrutura de Diretório**:
```
tests/
└── behat/
    ├── your_plugin.feature
    └── behat_your_plugin.php (optional custom steps)
```

**Template Feature File**:
```gherkin
@your_plugin @javascript
Feature: Your Plugin Functionality
  In order to use feature X
  As a teacher
  I need to perform action Y

  Background:
    Given the following "users" exist:
      | username | firstname | lastname | email |
      | teacher1 | Teacher | One | teacher1@example.com |
      | student1 | Student | One | student1@example.com |
    And the following "courses" exist:
      | fullname | shortname | category |
      | Course 1 | C1 | 0 |
    And the following "course enrolments" exist:
      | user | course | role |
      | teacher1 | C1 | editingteacher |
      | student1 | C1 | student |

  @javascript
  Scenario: Feature works for teacher
    Given I log in as "teacher1"
    And I am on "Course 1" course homepage
    When I perform action X
    Then I should see "expected result"
    And I should not see "unexpected result"

  Scenario: Feature respects capabilities
    Given I log in as "student1"
    And I am on "Course 1" course homepage
    Then I should not see "teacher-only feature"
```

**Exemplo Real (tiny_justify)**:
```gherkin
@editor_tiny @tiny_justify @javascript
Feature: TinyMCE Justify Plugin
  To format text with full justification
  As a user
  I need to use the justify button in TinyMCE

  Scenario: Justify button appears in toolbar
    Given I log in as "admin"
    And I navigate to "Settings > Site administration > Plugins > Text editors > TinyMCE editor"
    Then I should see "Justify" in the "#admin-tiny_justify" element
```

**Running Behat Locally**:
```bash
# 1. Initialize Behat
php admin/tool/behat/cli/init.php

# 2. Run specific feature
php admin/tool/behat/cli/run.php --tags=@your_plugin

# 3. Run specific scenario
php admin/tool/behat/cli/run.php --name="Feature works for teacher"
```

## 4.2. PHPUnit Tests (Unit/Component) 🔧 Recomendado

**O que são**: Testes unitários de classes e funções PHP isoladamente.

### 4.2.1. Estrutura de Diretório:
```
tests/
├── your_class_test.php
├── another_class_test.php
└── fixtures/
    └── test_data.xml
```

### 4.2.2. Template Test Class:
```php
<?php
namespace your_plugin;

/**
 * Unit tests for your_class.
 *
 * @package    your_plugin
 * @category   test
 * @copyright  2026 Your Name
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 * @covers \your_plugin\your_class
 */
final class your_class_test extends \advanced_testcase {

    /**
     * Setup before each test.
     */
    protected function setUp(): void {
        parent::setUp();
        $this->resetAfterTest(true);
    }

    /**
     * Test basic functionality.
     */
    public function test_basic_functionality(): void {
        $obj = new your_class();
        $result = $obj->do_something();
        
        $this->assertNotEmpty($result);
        $this->assertEquals('expected', $result);
    }

    /**
     * Test with database interactions.
     */
    public function test_database_interaction(): void {
        global $DB;
        
        // Create test data
        $course = $this->getDataGenerator()->create_course();
        $user = $this->getDataGenerator()->create_user();
        
        // Test your function
        $result = your_function($course->id, $user->id);
        
        // Assertions
        $this->assertTrue($result);
        
        // Verify database state
        $record = $DB->get_record('your_table', ['courseid' => $course->id]);
        $this->assertNotFalse($record);
    }

    /**
     * Test exception handling.
     */
    public function test_exception_thrown_on_invalid_input(): void {
        $this->expectException(\moodle_exception::class);
        $this->expectExceptionMessage('Invalid input');
        
        your_function_that_throws(-1);
    }
}
```

### 4.2.3. Running PHPUnit Locally:
```bash
# All tests
vendor/bin/phpunit

# Specific plugin
vendor/bin/phpunit --filter your_plugin

# Specific test class
vendor/bin/phpunit path/to/your_test.php

# With coverage
vendor/bin/phpunit --coverage-html coverage/
```

## 4.3. JavaScript/AMD Tests 🧪 Opcional

**Quando é necessário**: Se seu plugin tem módulos AMD com lógica complexa.

### 4.3.1. Estrutura:
```
tests/
└── javascript/
    ├── your_module_test.js
    └── index.js
```

### 4.3.2. Template Test:
```javascript
import {describe, it, expect, beforeEach} from '@jest/globals';
import {yourModule} from 'your_plugin/your_module';

describe('your_plugin/your_module', () => {
    beforeEach(() => {
        // Setup before each test
    });

    it('should initialize correctly', () => {
        const instance = yourModule.init();
        expect(instance).toBeDefined();
    });

    it('should process data correctly', () => {
        const input = {key: 'value'};
        const result = yourModule.processData(input);
        
        expect(result).toHaveProperty('processed');
        expect(result.processed).toBe(true);
    });

    it('should handle errors gracefully', () => {
        expect(() => {
            yourModule.processData(null);
        }).toThrow('Invalid input');
    });
});
```

### 4.3.3. Exemplo Real (tiny_justify):
```javascript
describe('TinyMCE Justify Plugin', () => {
    it('should register plugin correctly', () => {
        // Valida que plugin é registrado no TinyMCE
        expect(tinymce.PluginManager.get('justify')).toBeDefined();
    });
    
    it('should apply justify format to selection', () => {
        const editor = createMockEditor();
        editor.selection.setContent('<p>Test text</p>');
        
        // Execute justify command
        editor.execCommand('JustifyFull');
        
        const content = editor.getContent();
        expect(content).toContain('text-align: justify');
    });
});
```

# 5. Versionamento e Releases

## 5.1. Sistema de Versionamento Duplo

Moodle usa um sistema duplo de versionamento:

**1. `$plugin->version` (Timestamp)**:
```php
$plugin->version = 2026030401;  // YYYYMMDDHH
```
- Formato: Ano (4) + Mês (2) + Dia (2) + Hora/Incremento (2)
- Exemplos:
  - `2026030400` = 2026-03-04, primeira versão do dia
  - `2026030401` = 2026-03-04, segunda versão
  - `2026030422` = 2026-03-04, release final

**Propósito**: Determina ordem de instalação/upgrade no Moodle.

**2. `$plugin->release` (Semantic Versioning)**:
```php
$plugin->release = '1.0.22';  // X.Y.Z
```
- Formato: `MAJOR.MINOR.PATCH`
- Semântica:
  - `MAJOR`: Breaking changes
  - `MINOR`: New features, backward-compatible
  - `PATCH`: Bug fixes, backward-compatible

**Propósito**: Comunicação com usuários finais.

## 5.2. Sincronização de Versões

**Prática Recomendada** (validada em release.yml):

Últimos 2 dígitos de `version` devem corresponder aos últimos 2 dígitos de `release`:

```php
// ✅ CORRETO
$plugin->version  = 2026030422;
$plugin->release  = '1.0.22';  // 22 matches 22

// ❌ INCORRETO
$plugin->version  = 2026030423;
$plugin->release  = '1.0.22';  // 23 != 22
```

**Por quê?**: Garante rastreabilidade entre versão interna e externa.

## 5.3. Tags Git e Releases

**Convenção**:
```bash
# Tag name = $plugin->release (SEM prefixo 'v')
git tag -a 1.0.22 -m "Release 1.0.22"

# Não usar:
# git tag -a v1.0.22  # ❌ prefixo 'v' quebra automação
```

**release.yml valida**: `$plugin->release` == tag name

## 5.4. Conventional Commits

### 5.4.1. Formato:

User o modelo: `<type>(<scope>): <subject>`

### 5.4.2. Tipos Comuns:
```
feat: Nova funcionalidade
fix: Correção de bug
docs: Mudanças em documentação
style: Formatação (não afeta código)
refactor: Refatoração sem mudança funcional
test: Adicionar ou modificar testes
chore: Tarefas de manutenção (deps, CI, build)
perf: Melhorias de performance
ci: Mudanças em CI/CD
```

### 5.4.3. Exemplos Reais (tiny_justify):
```
feat: enhance alignment options with justify and nested menu integration
fix: update PostgreSQL version to 15 and enable fail-fast strategy in CI workflow
fix(coding-style): align plugin with Moodle contribution checklist
chore: bump version for cache invalidation
docs: update CONTRIBUTING.md with AVA/Docker workflow
```

### 5.4.4. Benefícios:
- Histórico git legível
- Changelogs automáticos
- Semantic versioning automático
- Facilita code review

## 5.5. Fluxo Completo de Release

```bash
# 1. Desenvolva e teste localmente
git checkout -b feature/new-feature
# ... code changes ...
git commit -m "feat: add new feature"

# 2. Merge para main via PR
# (CI testa automaticamente)
git push origin feature/new-feature
# Create PR → Review → Merge

# 3. Prepare release
git checkout main
git pull origin main

# Edit version.php
$plugin->version  = 2026030422;  # Increment
$plugin->release  = '1.0.22';    # Semantic increment

# Edit CHANGELOG.md
## [1.0.22] - 2026-03-04
### Added
- New feature description

# 4. Commit release preparation
git add version.php CHANGELOG.md
git commit -m "chore: bump version to 1.0.22"
git push origin main

# 5. Create and push tag (triggers release workflow)
git tag -a 1.0.22 -m "Release 1.0.22"
git push origin 1.0.22

# 6. Automatic: GitHub Actions does the rest
# - Validates versions match
# - Runs full CI test suite
# - Creates plugin ZIP
# - Creates GitHub Release
# - Uploads to Moodle Plugin Directory (if configured)
```

# 6. Git Workflow e Branching

## 6.1. Estratégia de Branching (Trunk-Based Development)

**Modelo Recomendado**: Trunk-Based Development com feature branches curtas.

### Estrutura de Branches:

```
main (stable, sempre deployable)
├── feature/new-feature (3-5 dias max)
├── bugfix/issue-42 (1-2 dias max)
└── docs/update-readme (1 dia max)
```

**Princípios**:
- ✅ `main` é sempre estável e deployable
- ✅ Features são branches de curta vida (máximo 5 dias)
- ✅ Merges apenas via Pull Requests com CI passando
- ✅ Branch protection rules aplicadas
- ✅ Squash commits antes de merge (história clara)

### Naming Convention:

```bash
# Features
feature/add-alignment-button
feature/improve-performance

# Bug fixes
bugfix/fix-xss-vulnerability
bugfix/issue-42-user-not-found

# Docs
docs/update-readme
docs/add-contributing-guide

# Chores
chore/update-dependencies
chore/configure-ci
```

## 6.2. GitHub Branch Protection Rules

**Configurar em Settings > Branches > Branch protection rules**:

1. ✅ **Require pull request reviews before merging**
   - Minimum 1 reviewer
   
2. ✅ **Require status checks to pass before merging**
   - Branches atualizado com `origin/main`
   - Select `moodle-plugin-ci` workflow
   
3. ✅ **Require code reviews from code owners**
   - Enable CODEOWNERS file
   
4. ✅ **Require conversation resolution before merging**

### Exemplo CODEOWNERS:

```
# .github/CODEOWNERS
* @kelsoncm
/lang/ @kelsoncm
/tests/ @kelsoncm
SECURITY.md @kelsoncm
```

# 7. .gitignore Padrão para Plugins Moodle

Criar arquivo `.gitignore` na raiz do plugin:

```bash
# Dependency management
/vendor/
/node_modules/
/composer.lock
package-lock.json
yarn.lock

# Build artifacts
/dist/
/build/
*.zip
*.tar.gz

# IDE
.vscode/
.idea/
.DS_Store
*.swp
*.swo
*~

# OS
Thumbs.db
.env
.env.local

# Testing
/coverage/
.phpunit.result.cache
/tests/behat/output/

# Moodle specific
/moodle/
/data/
db.sqlite
```

# 8. Code Review Best Practices

## 8.1. Para Autores de PR

**Antes de submeter**:
1. ✅ Testes passando localmente (`vendor/bin/phpunit`)
2. ✅ Linter sem erros (`phpcs`)
3. ✅ CHANGELOG.md atualizado
4. ✅ Documentação de código completa
5. ✅ Commits descritivos (Conventional Commits)
6. ✅ Sem código morto

**Na descrição do PR**:
- Descrição clara das mudanças
- Link para issues relacionadas
- Type of change (bug fix, feature, etc)
- Checklist de validação

## 8.2. Para Reviewers

**Focar em**:
- ✅ Segurança (SQL injection, XSS, capabilities)
- ✅ Performance (N+1 queries)
- ✅ Manutenibilidade (código claro)
- ✅ Testes (coverage adequado)
- ✅ Compatibilidade (versões suportadas)

# 9. Pre-Release Checklist

## 9.1. Antes de fazer uma release**:

- [ ] Branch `main` clean e atualizado
- [ ] Todos os PRs mergeados
- [ ] CHANGELOG.md completo
- [ ] `version.php` atualizado (version e release)
- [ ] README.md atualizado
- [ ] Testes passando
- [ ] Linters passando
- [ ] GitHub Actions CI/CD passando
- [ ] Secrets configurados (`MOODLE_DIRECTORY_TOKEN`)

## 9.2. Release Script Rápido

```bash
#!/bin/bash
VERSION=$1

# Validate
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Use X.Y.Z format"
  exit 1
fi

PATCH=$(echo $VERSION | cut -d. -f3)
PLUGIN_VERSION="$(date +%Y%m%d)${PATCH}"

sed -i "s/\\\$plugin->version = [0-9]*/\\\$plugin->version = $PLUGIN_VERSION/" version.php
sed -i "s/\\\$plugin->release = '[^']*'/\\\$plugin->release = '$VERSION'/" version.php

git add version.php CHANGELOG.md
git commit -m "chore: bump version to $VERSION"
git push origin main

git tag -a $VERSION -m "Release $VERSION"
git push origin $VERSION

echo "✅ Release $VERSION published!"
```

# 10. Referências

- [Moodle Plugin Development](https://moodledev.io/)
- [Moodle Coding Style](https://moodledev.io/general/development/policies/codingstyle)
- [Moodle Accessibility Guide](https://moodledev.io/general/development/policies/accessibility)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)


# 11. Backup/Restore

**O que é**: Sistema que permite exportar e restaurar dados do plugin em backups de cursos, atividades ou site.

**Quando é necessário**: Quando o plugin armazena dados que precisam ser preservados em backups.

## 11.1. Matriz de Recomendações por Tipo de Plugin

| Tipo | Necessidade | Quando | Exemplo |
|------|-------------|--------|---------|
| `mod_` | ⭐⭐⭐ Obrigatório | Sempre | Atividade de quiz custom |
| `block_` | ⭐⭐ Recomendado | Se tem dados do bloco | Bloco com configurações |
| `enrol_` | ⭐⭐ Recomendado | Se tem dados além do padrão | Inscrição customizada |
| `qtype_` | ⭐⭐ Recomendado | Se tem tabelas próprias | Tipo de questão custom |
| `format_` | ⭐ Recomendado | Se armazena dados | Formato de curso custom |
| `report_` | ⭐ Recomendado | Se grava dados persistentes | Relatório com cache |
| `tool_` | ⭐ Recomendado | Se tem configs estruturais | Ferramenta de configuração |
| `local_` | ⭐ Recomendado | Se tem dados de curso | Plugin local com dados |
| `theme_` | ❌ Desnecessário | Nunca | Temas são reinstalados |

## 11.2. Estrutura de Arquivos

```
plugin/
├── backup/
│   ├── moodle2/
│   │   ├── backup_plugintype_pluginname_activity.class.php
│   │   ├── backup_plugintype_pluginname_block.class.php
│   │   └── restore_plugintype_pluginname_activity.class.php
│   └── moodle2/
└── db/
    ├── install.php
    └── upgrade.php
```

## 11.3. Arquivo `backup_plugintype_pluginname_activity.class.php`

```php
<?php
/**
 * Backup activity class for your_plugin.
 *
 * @package    mod_your_plugin
 * @category   backup
 * @copyright  2026 Your Name
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

defined('MOODLE_INTERNAL') || die();

require_once($CFG->dirroot . '/mod/your_plugin/backup/moodle2/backup_your_plugin_activity.class.php');
require_once($CFG->dirroot . '/mod/your_plugin/backup/moodle2/backup_your_plugin_stepslib.php');
require_once($CFG->dirroot . '/mod/your_plugin/backup/moodle2/backup_your_plugin_settingslib.php');

class backup_mod_your_plugin_activity extends backup_activity_structure_step {

    protected function define_structure() {
        // Define backup's XML structure
        $plugin = new backup_nested_element('your_plugin', ['id'], [
            'name',
            'intro',
            'introformat',
            'version',
            'timecreated',
            'timemodified',
        ]);

        // Define subelements for related data
        $attempts = new backup_nested_element('attempts');
        $attempt = new backup_nested_element('attempt', ['id'], [
            'userid',
            'attemptno',
            'sumgrades',
            'timefinish',
        ]);

        // Build tree
        $plugin->add_child($attempts);
        $attempts->add_child($attempt);

        // Define sources
        $plugin->set_source_table('your_plugin', ['id' => backup::VAR_ACTIVITYID]);
        $attempt->set_source_table('your_plugin_attempts', ['your_pluginid' => backup::VAR_PARENTID]);

        // Define IDs
        $attempt->set_source_alias('userid', 'userid');

        return $plugin;
    }
}
```

## 11.4. Arquivo `restore_plugintype_pluginname_activity.class.php`

```php
<?php
/**
 * Restore activity class for your_plugin.
 *
 * @package    mod_your_plugin
 * @category   backup
 * @copyright  2026 Your Name
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

defined('MOODLE_INTERNAL') || die();

require_once($CFG->dirroot . '/mod/your_plugin/restore/moodle2/restore_your_plugin_activity.class.php');
require_once($CFG->dirroot . '/mod/your_plugin/restore/moodle2/restore_your_plugin_stepslib.php');
require_once($CFG->dirroot . '/mod/your_plugin/restore/moodle2/restore_your_plugin_settingslib.php');

class restore_mod_your_plugin_activity extends restore_activity_structure_step {

    protected function define_structure() {
        $paths = [];

        // Main activity element
        $paths[] = new restore_path_element('your_plugin', '/activity/your_plugin');
        
        // Attempts
        $paths[] = new restore_path_element('your_plugin_attempt', '/activity/your_plugin/attempts/attempt');

        return $paths;
    }

    protected function process_your_plugin($data) {
        global $DB;

        $data = (object)$data;
        $data->course = $this->get_courseid();

        $newid = $DB->insert_record('your_plugin', $data);
        $this->set_mapping('your_plugin', $data->id, $newid);
    }

    protected function process_your_plugin_attempt($data) {
        global $DB;

        $data = (object)$data;
        $data->your_pluginid = $this->get_new_parentid('your_plugin');
        $data->userid = $this->get_mappingid('user', $data->userid);

        $newid = $DB->insert_record('your_plugin_attempts', $data);
        $this->set_mapping('your_plugin_attempt', $data->id, $newid);
    }

    protected function after_execute() {
        // Adicione lógica pós-restauração aqui se necessário
    }
}
```

# 12. External Service (API WEB SERVICE)

**O que é**: Sistema que permite acessar funcionalidades do plugin através de APIs web (REST, XML-RPC, SOAP).

**Quando é necessário**: Quando o plugin deve ser integrado com sistemas externos ou aplicações mobile.

## 12.1. Estrutura de Arquivos

```
plugin/
├── db/
│   ├── services.php          # Define os serviços
│   └── external_functions.php # Implementa as funções
└── externallib.php           # Classes com a lógica
```

## 12.2. Arquivo `db/services.php`

Define quais funções são expostas como web service:

```php
<?php
/**
 * Web service definitions for your_plugin.
 *
 * @package    your_plugin
 * @copyright  2026 Your Name
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

defined('MOODLE_INTERNAL') || die();

$functions = [
    'your_plugin_get_items' => [
        'classname'    => 'your_plugin\\external\\api',
        'methodname'   => 'get_items',
        'classpath'    => 'your_plugin/external/api.php',
        'description'  => 'Returns a list of items',
        'type'         => 'read',
        'ajax'         => true,
        'capabilities' => 'moodle/course:view',
    ],

    'your_plugin_create_item' => [
        'classname'    => 'your_plugin\\external\\api',
        'methodname'   => 'create_item',
        'classpath'    => 'your_plugin/external/api.php',
        'description'  => 'Creates a new item',
        'type'         => 'write',
        'ajax'         => false,
        'capabilities' => 'your_plugin/manage:items',
    ],

    'your_plugin_delete_item' => [
        'classname'    => 'your_plugin\\external\\api',
        'methodname'   => 'delete_item',
        'classpath'    => 'your_plugin/external/api.php',
        'description'  => 'Deletes an item',
        'type'         => 'write',
        'ajax'         => false,
        'capabilities' => 'your_plugin/manage:items',
    ],
];
```

## 12.3. Arquivo `classes/external/api.php`

Implementa as funções web service:

```php
<?php
/**
 * Web service functions for your_plugin.
 *
 * @package    your_plugin
 * @copyright  2026 Your Name
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

namespace your_plugin\external;

defined('MOODLE_INTERNAL') || die();

require_once($CFG->libdir . '/externallib.php');

class api extends \external_api {

    /**
     * get_items parameters
     */
    public static function get_items_parameters() {
        return new \external_function_parameters([
            'courseid' => new \external_value(PARAM_INT, 'Course ID'),
            'limit'    => new \external_value(PARAM_INT, 'Items limit', VALUE_DEFAULT, 10),
            'offset'   => new \external_value(PARAM_INT, 'Items offset', VALUE_DEFAULT, 0),
        ]);
    }

    /**
     * get_items return value
     */
    public static function get_items_returns() {
        return new \external_single_structure([
            'items' => new \external_multiple_structure(
                new \external_single_structure([
                    'id'   => new \external_value(PARAM_INT, 'Item ID'),
                    'name' => new \external_value(PARAM_TEXT, 'Item name'),
                    'description' => new \external_value(PARAM_TEXT, 'Item description'),
                ])
            ),
            'total' => new \external_value(PARAM_INT, 'Total items count'),
        ]);
    }

    /**
     * Get items from course
     */
    public static function get_items($courseid, $limit = 10, $offset = 0) {
        global $DB;

        // Validate context and capability
        $context = \context_course::instance($courseid);
        self::validate_context($context);
        require_capability('moodle/course:view', $context);

        // Get items from database
        $items = $DB->get_records('your_plugin_items', 
            ['courseid' => $courseid],
            'timecreated DESC',
            '*',
            $offset,
            $limit
        );

        $total = $DB->count_records('your_plugin_items', ['courseid' => $courseid]);

        $result = [
            'items' => [],
            'total' => $total,
        ];

        foreach ($items as $item) {
            $result['items'][] = [
                'id'          => $item->id,
                'name'        => $item->name,
                'description' => $item->description,
            ];
        }

        return $result;
    }

    /**
     * create_item parameters
     */
    public static function create_item_parameters() {
        return new \external_function_parameters([
            'courseid'    => new \external_value(PARAM_INT, 'Course ID'),
            'name'        => new \external_value(PARAM_TEXT, 'Item name'),
            'description' => new \external_value(PARAM_TEXT, 'Item description'),
        ]);
    }

    /**
     * create_item return value
     */
    public static function create_item_returns() {
        return new \external_single_structure([
            'id'   => new \external_value(PARAM_INT, 'Item ID'),
            'name' => new \external_value(PARAM_TEXT, 'Item name'),
        ]);
    }

    /**
     * Create new item
     */
    public static function create_item($courseid, $name, $description) {
        global $DB;

        // Validate context and capability
        $context = \context_course::instance($courseid);
        self::validate_context($context);
        require_capability('your_plugin/manage:items', $context);

        // Validate input
        $name = clean_param($name, PARAM_TEXT);
        $description = clean_param($description, PARAM_TEXT);

        if (empty($name)) {
            throw new \invalid_parameter_exception('Name is required');
        }

        // Create item
        $item = new \stdClass();
        $item->courseid = $courseid;
        $item->name = $name;
        $item->description = $description;
        $item->timecreated = time();
        $item->timemodified = time();

        $itemid = $DB->insert_record('your_plugin_items', $item);

        return [
            'id'   => $itemid,
            'name' => $name,
        ];
    }

    /**
     * delete_item parameters
     */
    public static function delete_item_parameters() {
        return new \external_function_parameters([
            'itemid' => new \external_value(PARAM_INT, 'Item ID'),
        ]);
    }

    /**
     * delete_item return value
     */
    public static function delete_item_returns() {
        return new \external_value(PARAM_BOOL, 'Success');
    }

    /**
     * Delete item
     */
    public static function delete_item($itemid) {
        global $DB;

        // Get item and validate capability
        $item = $DB->get_record('your_plugin_items', ['id' => $itemid], '*', MUST_EXIST);
        
        $context = \context_course::instance($item->courseid);
        self::validate_context($context);
        require_capability('your_plugin/manage:items', $context);

        // Delete item
        $DB->delete_records('your_plugin_items', ['id' => $itemid]);

        return true;
    }
}
```

## 12.4. Ativar o Web Service

1. **Admin > Site administration > Plugins > Web services > Manage tokens**
   - Criar token para usuário com acesso ao plugin

2. **Admin > Site administration > Plugins > Web services > External services**
   - Habilitar serviços desejados

3. **Admin > Site administration > Development > Web service authentication > REST protocol**
   - Habilitar REST (ou XML-RPC, SOAP, etc)

## 12.5. Chamar Web Service (Exemplo REST)

```bash
curl -X POST \
  'http://moodle.example.com/webservice/rest/server.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "wstoken": "YOUR_TOKEN",
    "wsfunction": "your_plugin_get_items",
    "moodlewsrestformat": "json",
    "courseid": 1,
    "limit": 10
  }'
```

# 13. Tasks (Cron Jobs)

**O que são**: Procedimentos executados automaticamente em background pelo Moodle.

**Tipos**:
- **Ad hoc tasks**: Executadas uma única vez quando marcadas
- **Scheduled tasks**: Executadas em intervalos regulares
- **Backup tasks**: Executadas durante backup de curso/atividade

## 13.1. Arquivo `db/tasks.php`

Define as tasks do plugin:

```php
<?php
/**
 * Task definitions for your_plugin.
 *
 * @package    your_plugin
 * @copyright  2026 Your Name
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

defined('MOODLE_INTERNAL') || die();

$tasks = [
    // Scheduled task: executa a cada hora
    [
        'classname' => 'your_plugin\\task\\sync_data',
        'blocking'  => 0,
        'minute'    => '0',
        'hour'      => '*',
        'day'       => '*',
        'month'     => '*',
        'dayofweek' => '*',
    ],

    // Scheduled task: executa diariamente às 3:00 AM
    [
        'classname' => 'your_plugin\\task\\cleanup_old_records',
        'blocking'  => 0,
        'minute'    => '0',
        'hour'      => '3',
        'day'       => '*',
        'month'     => '*',
        'dayofweek' => '*',
    ],

    // Ad hoc task: pode ser executada manualmente a qualquer hora
    [
        'classname' => 'your_plugin\\task\\rebuild_cache',
        'blocking'  => 0,
    ],
];
```

## 13.2. Scheduled Task Class

File: `classes/task/sync_data.php`

```php
<?php
/**
 * Scheduled task to sync data.
 *
 * @package    your_plugin
 * @copyright  2026 Your Name
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

namespace your_plugin\task;

defined('MOODLE_INTERNAL') || die();

class sync_data extends \core\task\scheduled_task {

    public function get_name() {
        return get_string('task_sync_data', 'your_plugin');
    }

    public function execute() {
        global $DB;

        $this->output->writeln('Starting data sync...');

        try {
            // 1. Get external data
            $external_data = $this->fetch_external_data();

            // 2. Process and validate
            foreach ($external_data as $item) {
                $this->process_item($item);
            }

            // 3. Log success
            mtrace('Data sync completed successfully');

        } catch (\Exception $e) {
            mtrace('Error during data sync: ' . $e->getMessage());
            throw $e;
        }
    }

    private function fetch_external_data() {
        // Implementar lógica para obter dados externos
        // Retornar array de dados
        return [];
    }

    private function process_item($item) {
        global $DB;

        // Validar item
        if (empty($item->id)) {
            return;
        }

        // Verificar se já existe
        $record = $DB->get_record('your_plugin_items', ['external_id' => $item->id]);

        if ($record) {
            // Actualizar
            $record->name = $item->name;
            $record->timemodified = time();
            $DB->update_record('your_plugin_items', $record);
        } else {
            // Inserir novo
            $record = new \stdClass();
            $record->external_id = $item->id;
            $record->name = $item->name;
            $record->timecreated = time();
            $record->timemodified = time();
            $DB->insert_record('your_plugin_items', $record);
        }
    }
}
```

## 13.3. Ad Hoc Task Class

File: `classes/task/rebuild_cache.php`

```php
<?php
/**
 * Ad hoc task to rebuild cache.
 *
 * @package    your_plugin
 * @copyright  2026 Your Name
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

namespace your_plugin\task;

defined('MOODLE_INTERNAL') || die();

class rebuild_cache extends \core\task\adhoc_task {

    public function execute() {
        // Purgar cache
        $cache = \cache::make('your_plugin', 'items');
        $cache->purge();

        // Reconstruir cache a partir do banco
        global $DB;
        $items = $DB->get_records('your_plugin_items');

        foreach ($items as $item) {
            $cache->set($item->id, $item);
        }

        mtrace('Cache rebuilt successfully');
    }
}
```

## 13.4. Executar Ad Hoc Task Programaticamente

```php
<?php
// Agendar task ad hoc para executar assim que possível
$task = new \your_plugin\task\rebuild_cache();
\core\task\manager::queue_adhoc_task($task);

// Agendar task ad hoc com delay (5 minutos)
$task = new \your_plugin\task\rebuild_cache();
$task->set_next_run_time(time() + 300);
\core\task\manager::queue_adhoc_task($task);
```

## 13.5. Cleanup Task (Exemplo Prático)

File: `classes/task/cleanup_old_records.php`

```php
<?php
/**
 * Scheduled task to cleanup old records.
 *
 * @package    your_plugin
 * @copyright  2026 Your Name
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

namespace your_plugin\task;

defined('MOODLE_INTERNAL') || die();

class cleanup_old_records extends \core\task\scheduled_task {

    public function get_name() {
        return get_string('task_cleanup', 'your_plugin');
    }

    public function execute() {
        global $DB;

        // Remover registros com mais de 1 ano
        $oneyearago = time() - (365 * 24 * 60 * 60);
        
        $deleted = $DB->delete_records_select(
            'your_plugin_logs',
            'timecreated < ?',
            [$oneyearago]
        );

        mtrace("Deleted $deleted old records");
    }
}
```

# 14. Capabilities (Permissões)

**O que são**: Sistema de permissões granulares que controla o que cada usuário pode fazer no plugin.

**Onde definir**: `db/access.php`

## 14.1. Arquivo `db/access.php`

Define as capabilities do plugin:

```php
<?php
/**
 * Capabilities for your_plugin.
 *
 * @package    your_plugin
 * @copyright  2026 Your Name
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

defined('MOODLE_INTERNAL') || die();

$capabilities = [

    // Visualizar plugin
    'your_plugin/view' => [
        'captype'      => 'read',
        'contextlevel' => CONTEXT_COURSE,
        'archetypes'   => [
            'teacher'        => CAP_ALLOW,
            'editingteacher' => CAP_ALLOW,
            'student'        => CAP_ALLOW,
            'guest'          => CAP_PREVENT,
        ],
    ],

    // Gerenciar items
    'your_plugin/manage:items' => [
        'captype'      => 'write',
        'contextlevel' => CONTEXT_COURSE,
        'archetypes'   => [
            'teacher'        => CAP_ALLOW,
            'editingteacher' => CAP_ALLOW,
            'student'        => CAP_PREVENT,
        ],
    ],

    // Deletar items
    'your_plugin/delete:items' => [
        'captype'      => 'write',
        'contextlevel' => CONTEXT_COURSE,
        'archetypes'   => [
            'editingteacher' => CAP_ALLOW,
            'teacher'        => CAP_PREVENT,
        ],
        'clonepermissionsfrom' => 'moodle/course:update',
    ],

    // Visualizar relatórios
    'your_plugin/viewreports' => [
        'captype'      => 'read',
        'contextlevel' => CONTEXT_COURSE,
        'archetypes'   => [
            'editingteacher' => CAP_ALLOW,
            'teacher'        => CAP_ALLOW,
            'student'        => CAP_PREVENT,
        ],
    ],

    // Gerenciar plugin (config global)
    'your_plugin/manage' => [
        'captype'      => 'write',
        'contextlevel' => CONTEXT_SYSTEM,
        'archetypes'   => [
            'manager' => CAP_ALLOW,
        ],
        'clonepermissionsfrom' => 'moodle/site:config',
    ],
];
```

## 14.2. Usando Capabilities no Código

```php
<?php
// Verificar se usuário tem capability
$context = context_course::instance($courseid);

// Check requer (lança exception se não tem)
require_capability('your_plugin/view', $context);

// Check opcional (retorna bool)
if (has_capability('your_plugin/manage:items', $context)) {
    // Mostrar botão de gerenciar
}

// Get all users with capability em contexto
$users = get_users_by_capability($context, 'your_plugin/view');

// Verificar contra usuário específico
if (user_has_role_assignment($userid, $roleid, $contextid)) {
    // User tem role espeífica
}
```

## 14.3. Nomes Convention para Capabilities

```
your_plugin/<actions>

Exemplos:
- your_plugin/view                 (ler dados)
- your_plugin/create:items         (criar items)
- your_plugin/edit:items           (editar items)
- your_plugin/delete:items         (deletar items)
- your_plugin/manage:settings      (gerenciar configurações)
- your_plugin/download:reports     (download relatórios)
- your_plugin/viewhidden           (ver dados ocultos)
```

## 14.4. Context Levels

| Context | Nível | Uso |
|---------|-------|-----|
| `CONTEXT_SYSTEM` | Global | Permissões globais do site |
| `CONTEXT_COURSECAT` | Categoria | Permissões por categoria de curso |
| `CONTEXT_COURSE` | Curso | Permissões por curso |
| `CONTEXT_MODULE` | Atividade | Permissões por atividade/módulo |
| `CONTEXT_BLOCK` | Bloco | Permissões por bloco |
| `CONTEXT_USER` | Usuário | Permissões de usuário |

## 14.5. Captype (Tipo de Permission)

```
'captype' => 'read|write'

- read:  Apenas leitura de dados (visualizar, exportar)
- write: Modificação de dados (criar, editar, deletar)
```


# 15. Versão e Finalização

**Este guia é um documento vivo e deve ser atualizado regularmente.**

## 15.1. Checklist de Rastreabilidade

Antes de publicar uma versão do plugin, verifique:

- [ ] Todas as seções 1-14 foram implementadas (ou documentado por quê não)
- [ ] Cada seção tem exemplos práticos e código real
- [ ] Testes are cobrindo todas as funcionalidades principais
- [ ] Documentação está clara e amigável
- [ ] Security foi revisada por alguém externo
- [ ] CHANGELOG.md reflete todas as mudanças

## 15.2. Iteração Contínua

A cada release:
1. Revisar este guia
2. Documentar novas práticas aprendidas
3. Atualizar exemplos se necessário
4. Compartilhar aprendizados com a comunidade

---
**Última atualização**: 2026-03-04  
**Autor**: KelsonCM  
**Licença**: CC-BY-4.0