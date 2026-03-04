# Guia de boas práticas para desenvolvimento de plugins Moodle

Este documento consolida as melhores práticas para desenvolvimento de plugins Moodle profissionais, baseado na análise de projetos reais bem-sucedidos, especialmente o **tiny_justify** como caso de estudo. O objetivo é fornecer um roteiro completo para criar plugins de alta qualidade, manuteníveis e seguros desde o início do projeto.

---

# Índice
- [Guia de boas práticas para desenvolvimento de plugins Moodle](#guia-de-boas-práticas-para-desenvolvimento-de-plugins-moodle)
- [Índice](#índice)
- [1. Visão Geral](#1-visão-geral)
  - [1.1. Princípios Fundamentais](#11-princípios-fundamentais)
  - [1.2. Por Que Isso Importa?](#12-por-que-isso-importa)
- [2. Case Study: tiny\_justify](#2-case-study-tiny_justify)
  - [2.1. Contexto](#21-contexto)
  - [2.2. Timeline de Desenvolvimento Real](#22-timeline-de-desenvolvimento-real)
    - [2.2.1. Fase 1: Fundação completa](#221-fase-1-fundação-completa)
    - [2.2.2. Fase 2: Documentação](#222-fase-2-documentação)
    - [2.2.3. Fase 3: Evolução Contínua](#223-fase-3-evolução-contínua)
  - [2.3. `CHANGELOG.md`](#23-changelogmd)
  - [2.4. `CONTRIBUTING.md`](#24-contributingmd)
  - [2.5. `README.md`](#25-readmemd)
  - [2.6. `SECURITY.md`](#26-securitymd)
  - [2.7. `.github/dependabot.yml`](#27-githubdependabotyml)
  - [2.8. `.github/workflows/moodle-plugin-ci.yml`](#28-githubworkflowsmoodle-plugin-ciyml)
    - [2.8.1 Exemplo de matrix de testes](#281-exemplo-de-matrix-de-testes)
    - [2.8.2. Exemplo completo](#282-exemplo-completo)
  - [2.9. `.github/workflows/release.yml`](#29-githubworkflowsreleaseyml)
    - [2.9.1 Workflow Completo](#291-workflow-completo)
    - [2.9.2 \*\*Workflow de Release](#292-workflow-de-release)
- [3. Sistema de Testes](#3-sistema-de-testes)
  - [3.1. Behat Tests (Integration/E2E) ⭐ Essencial](#31-behat-tests-integratione2e--essencial)
  - [3.2. PHPUnit Tests (Unit/Component) 🔧 Recomendado](#32-phpunit-tests-unitcomponent--recomendado)
    - [3.2.1. Estrutura de Diretório:](#321-estrutura-de-diretório)
    - [3.2.2. Template Test Class:](#322-template-test-class)
    - [3.2.3. Running PHPUnit Locally:](#323-running-phpunit-locally)
    - [3.3. JavaScript/AMD Tests 🧪 Opcional](#33-javascriptamd-tests--opcional)
    - [3.3.1. Estrutura:](#331-estrutura)
    - [3.3.2. Template Test:](#332-template-test)
    - [3.3.3. Exemplo Real (tiny\_justify):](#333-exemplo-real-tiny_justify)
- [4. Versionamento e Releases](#4-versionamento-e-releases)
  - [4.1. Sistema de Versionamento Duplo](#41-sistema-de-versionamento-duplo)
  - [4.2. Sincronização de Versões](#42-sincronização-de-versões)
  - [4.3. Tags Git e Releases](#43-tags-git-e-releases)
  - [4.4. Conventional Commits](#44-conventional-commits)
    - [4.4.1. Formato:](#441-formato)
    - [4.4.2. Tipos Comuns:](#442-tipos-comuns)
    - [4.4.3. Exemplos Reais (tiny\_justify):](#443-exemplos-reais-tiny_justify)
    - [4.4.4. Benefícios:](#444-benefícios)
- [5. Fluxo Completo de Release](#5-fluxo-completo-de-release)

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


# 2. Case Study: tiny_justify

## 2.1. Contexto

O **tiny_justify** é um plugin TinyMCE para Moodle que adiciona botão de justificação de texto. Apesar de ser um plugin relativamente simples (~800 linhas de código), foi desenvolvido seguindo rigorosamente as melhores práticas da indústria.

## 2.2. Timeline de Desenvolvimento Real

Análise do histórico git revelou uma metodologia estruturada:

### 2.2.1. Fase 1: Fundação completa

**Em um único commit inicial, foram criados**:

| Categoria | Arquivos                                       |
| --------- | ---------------------------------------------- |
| CI/CD     | `.github/workflows/`, `.github/dependabot.yml` |
| Código    | `classes/`, `amd/src/`                         |
| Testes    | `tests/behat/`, `tests/javascript/`            |
| Database  | `db/install.php`, `db/upgrade.php`             |
| Lang      | `lang/en/`, `lang/pt_br/`                      |
| Config    | `version.php`, `styles.css`, `pix/`            |

**Lição Crítica**: Criar infraestrutura de CI/CD **no primeiro commit**, não depois.

### 2.2.2. Fase 2: Documentação

Adicionados em commit separado:
1. ✅ `README.md`
2. ✅ `SECURITY.md`
3. ✅ `CONTRIBUTING.md`
4. ✅ `CHANGELOG.md`
5. ✅ `LICENSE.md` - Necessariamente em GPLv3

**Lição**: Documentação crítica criadas no **no primeiro commit**, não como afterthought, e atualizadas a cada iteração.

### 2.2.3. Fase 3: Evolução Contínua

Após releases iniciais, 21 iterações de melhorias:
- Suporte a PHP 8.4 e Moodle 5.1
- Atualização PostgreSQL 15, MariaDB 10.11
- Validação automática de release
- Upload para Moodle Plugin Directory

**Lição**: CI permite iteração rápida e confiante.

## 2.3. `CHANGELOG.md`

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

## 2.4. `CONTRIBUTING.md`

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

## 2.5. `README.md`

1. Overview
2. Requirements
3. Installation
4. Configuration
5. Usage
6. License
7. Contributing
8. Support

## 2.6. `SECURITY.md`

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

1. Overview
2. How to Contribute
3. Supported Versions
4. Security Properties
   1. Capability Requirements
   2. Input Validation & Sanitization
   3. Context Isolation
   4. Data Access Control
   5. User data usage and protection
   6. etc...
5. Security Considerations
   1. Capability-Based Access
   2. SQL Injection Prevention
   3. Cross-Site Scripting (XSS) Prevention
   4. Cross-Site Request Forgery (CSRF) Protection
   5. etc...
6. Known Limitations
7. Reporting a Vulnerability
   1. Please DO NOT create a public GitHub issue for security vulnerabilities.
   2. Contact Information
      1. What to Include
         1. What to Include
            1. Description of the vulnerability
            2. Steps to reproduce (if applicable)
            3. Impact assessment (e.g., data exposure, privilege escalation)
            4. Affected versions
            5. Suggested remediation (optional)
   3. Response Timeline
   4. Severity Levels (Critical, High, Medium, Low)
8. Security Best Practices for Administrators
   1. Installation & Updates
      1. Install from official Moodle Plugin Directory or verified source
      2. Keep Moodle updated to the latest stable release
      3. Install security patches immediately upon availability
      4. Test updates in a staging environment first
    2. Configuration
       1. Audit which users have `viewparticipants` capability
       2. Restrict this capability to trusted roles only
       3. Monitor administrative logs for unusual filter queries
       4. Consider restricting custom profile fields visible to students
    3. Monitoring
       1. Check Moodle logs for failed access attempts
       2. Review participated user lists periodically
       3. Monitor database performance impact of filtering operations
 9. Development & Code Review
    1. **No Hardcoded Credentials**: Sensitive data is never stored in repository
    2. **Capability Checks**: Every user-facing action requires capability verification
    3. **Input Validation**: All user inputs are validated and sanitized
    4. **Prepared Statements**: All database queries use parameterized queries
    5. **Error Handling**: Errors are logged but not exposed to users
    6. **Code Review**: All changes undergo security review before merge
 10. Dependencies
     1.  **Moodle**: 4.5.0+
     2.  **PHP**: 8.1+
     3.  **Database**: PostgreSQL 15+, MariaDB 10.11+
     4.  **External libs**: (list)
 10. Test matrix
     1.  **Moodle**: 4.5.0, 4.5.0, 4.5.1
     2.  **PHP**: 8.1, 8.2, 8.3, 8.4
     3.  **Database**: PostgreSQL 15, MariaDB 10.11
 11. License
     1.  GPLv3
 12. Contact & Support
     1. **Repository**: This GitHub Repository
     2. **Bug Reports**: This GitHub Issues
     3. **Security Reports**: See "Reporting a Vulnerability" section above
 13. Final notes
     1.  **Last Updated**: 2026-03-04
     2.  **Status**: Active
     3.  **Maintainer**: [KelsonCM](https://github.com/kelsoncm/)

## 2.7. `.github/dependabot.yml`

**Por que é importante**: Mantém dependências seguras automaticamente.

**Configuração Básica**:
```yaml
version: 2
updates:
  - package-ecosystem: "composer"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

**Configuração Avançada**:
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


## 2.8. `.github/workflows/moodle-plugin-ci.yml`

**Objetivo**: Testar plugin contra múltiplas versões de Moodle, PHP e databases automaticamente.

### 2.8.1 Exemplo de matrix de testes

| PHP | Moodle 4.5 | Moodle 5.0 | Moodle 5.1 | Databases      |
| --- | ---------- | ---------- | ---------- | -------------- |
| 8.1 | ✅          | ❌          | ❌          | pgsql, mariadb |
| 8.2 | ✅          | ✅          | ✅          | pgsql, mariadb |
| 8.3 | ✅          | ✅          | ✅          | pgsql, mariadb |
| 8.4 | ❌          | ✅          | ✅          | pgsql, mariadb |

**Resultado**: ~20 combinações testadas automaticamente em cada push!

### 2.8.2. Exemplo completo

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

## 2.9. `.github/workflows/release.yml`

**Objetivo**: Automatizar criação de releases, empacotamento ZIP, e upload para GitHub Releases e para Moodle Plugin Directory.

**Validações Implementadas**:
1. ✅ `$plugin->version` últimos 2 dígitos == `$plugin->release` últimos 2 dígitos
2. ✅ `$plugin->release` == git tag name
3. ✅ ZIP contém estrutura correta de diretório
4. ✅ Upload confirma sucesso antes de marcar release

### 2.9.1 Workflow Completo

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
        run: |
          PLUGIN_NAME="your_plugin_name"
          mkdir -p /tmp/build/$PLUGIN_NAME

          rsync -a \
            --exclude='.git' \
            --exclude='.github' \
            --exclude='node_modules' \
            --exclude='.gitignore' \
            . /tmp/build/$PLUGIN_NAME/

          cd /tmp/build
          zip -r "$GITHUB_WORKSPACE/$PLUGIN_NAME-${{ steps.version.outputs.number }}.zip" $PLUGIN_NAME/

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: ${{ env.PLUGIN_NAME }}-${{ steps.version.outputs.number }}.zip
          generate_release_notes: true

      - name: Upload to Moodle Plugin Directory
        if: ${{ env.HAS_MOODLE_TOKEN == 'true' }}
        env:
          HAS_MOODLE_TOKEN: ${{ secrets.MOODLE_DIRECTORY_TOKEN != '' }}
          MOODLE_DIRECTORY_TOKEN: ${{ secrets.MOODLE_DIRECTORY_TOKEN }}
        run: |
          RESPONSE=$(curl -s -w "\n%{http_code}" \
            -F data=@"$GITHUB_WORKSPACE/$PLUGIN_NAME-${{ steps.version.outputs.number }}.zip" \
            "https://moodle.org/webservice/upload.php?token=$MOODLE_DIRECTORY_TOKEN")

          HTTP_CODE=$(echo "$RESPONSE" | tail -1)
          BODY=$(echo "$RESPONSE" | sed '$d')

          echo "HTTP status: $HTTP_CODE"
          echo "Response: $BODY"

          if [ "$HTTP_CODE" -ne 200 ] || echo "$BODY" | grep -q '"error"'; then
            echo "::error::Failed to upload to Moodle Plugin Directory"
            exit 1
          fi
```

### 2.9.2 **Workflow de Release

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


# 3. Sistema de Testes

## 3.1. Behat Tests (Integration/E2E) ⭐ Essencial

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

## 3.2. PHPUnit Tests (Unit/Component) 🔧 Recomendado

**O que são**: Testes unitários de classes e funções PHP isoladamente.

### 3.2.1. Estrutura de Diretório:
```
tests/
├── your_class_test.php
├── another_class_test.php
└── fixtures/
    └── test_data.xml
```

### 3.2.2. Template Test Class:
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

### 3.2.3. Running PHPUnit Locally:
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

### 3.3. JavaScript/AMD Tests 🧪 Opcional

**Quando é necessário**: Se seu plugin tem módulos AMD com lógica complexa.

### 3.3.1. Estrutura:
```
tests/
└── javascript/
    ├── your_module_test.js
    └── index.js
```

### 3.3.2. Template Test:
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

### 3.3.3. Exemplo Real (tiny_justify):
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

# 4. Versionamento e Releases

## 4.1. Sistema de Versionamento Duplo

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

## 4.2. Sincronização de Versões

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

## 4.3. Tags Git e Releases

**Convenção**:
```bash
# Tag name = $plugin->release (SEM prefixo 'v')
git tag -a 1.0.22 -m "Release 1.0.22"

# Não usar:
# git tag -a v1.0.22  # ❌ prefixo 'v' quebra automação
```

**release.yml valida**: `$plugin->release` == tag name

## 4.4. Conventional Commits

### 4.4.1. Formato:

User o modelo: `<type>(<scope>): <subject>`

### 4.4.2. Tipos Comuns:
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

### 4.4.3. Exemplos Reais (tiny_justify):
```
feat: enhance alignment options with justify and nested menu integration
fix: update PostgreSQL version to 15 and enable fail-fast strategy in CI workflow
fix(coding-style): align plugin with Moodle contribution checklist
chore: bump version for cache invalidation
docs: update CONTRIBUTING.md with AVA/Docker workflow
```

### 4.4.4. Benefícios:
- Histórico git legível
- Changelogs automáticos
- Semantic versioning automático
- Facilita code review

# 5. Fluxo Completo de Release

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
