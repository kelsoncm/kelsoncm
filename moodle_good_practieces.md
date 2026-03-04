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

--- 

**Última atualização**: 2026-03-04  
**Autor**: KelsonCM  
**Licença**: CC-BY-4.0