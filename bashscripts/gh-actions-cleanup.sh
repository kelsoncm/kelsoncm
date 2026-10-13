#!/usr/bin/env bash
set -Eeuo pipefail

export MSYS_NO_PATHCONV=1

usage() {
  cat <<'EOF'
Uso:
  ./gh-actions-cleanup.sh OWNER[/REPO] [logs|runs]

Exemplos:
  # Repositório específico:
  ./gh-actions-cleanup.sh cte-zl-ifrn/integration-avaintegration_metapackage
  ./gh-actions-cleanup.sh cte-zl-ifrn/integration-avaintegration_metapackage logs
  ./gh-actions-cleanup.sh cte-zl-ifrn/integration-avaintegration_metapackage runs

  # Todos os repositórios de uma organização/usuário:
  ./gh-actions-cleanup.sh cte-zl-ifrn
  ./gh-actions-cleanup.sh cte-zl-ifrn logs
  ./gh-actions-cleanup.sh cte-zl-ifrn runs

Padrão:
  runs  -> apaga todas as workflow runs

Requisitos:
  - gh autenticado com permissão de escrita no(s) repositório(s)
EOF
}

log() {
  printf '\n[%s] %s\n' "$(date +'%H:%M:%S')" "$*"
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Erro: comando obrigatório não encontrado: $1" >&2
    exit 1
  }
}

cleanup_repo() {
  local REPO="$1"
  local MODE="$2"

  log "Buscando workflow runs de $REPO"
  local RUN_IDS
  RUN_IDS="$(
    gh api \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      --paginate \
      "repos/$REPO/actions/runs?per_page=100" \
      --jq '.workflow_runs[]?.id' 2>/dev/null || true
  )"

  if [[ -z "$RUN_IDS" ]]; then
    log "Nenhuma workflow run encontrada em $REPO"
    return 0
  fi

  local TOTAL
  TOTAL="$(printf '%s\n' "$RUN_IDS" | grep -v '^$' | wc -l | tr -d ' ')"
  log "Encontradas $TOTAL workflow runs em $REPO"

  local COUNT=0
  while IFS= read -r RUN_ID; do
    [[ -z "$RUN_ID" ]] && continue
    COUNT=$((COUNT + 1))

    if [[ "$MODE" == "logs" ]]; then
      printf '\r[%s/%s] Apagando logs da run %s (%s)...' "$COUNT" "$TOTAL" "$RUN_ID" "$REPO"
      gh api \
        --silent \
        --method DELETE \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        "repos/$REPO/actions/runs/$RUN_ID/logs" \
        || printf '\nFalha ao apagar logs da run %s\n' "$RUN_ID" >&2
    else
      printf '\r[%s/%s] Apagando run %s (%s)...' "$COUNT" "$TOTAL" "$RUN_ID" "$REPO"
      gh api \
        --silent \
        --method DELETE \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        "repos/$REPO/actions/runs/$RUN_ID" \
        || printf '\nFalha ao apagar run %s\n' "$RUN_ID" >&2
    fi

    sleep 0.1
  done <<< "$RUN_IDS"

  printf '\n'
}

if [[ $# -lt 1 ]] || [[ "${1:-}" =~ ^(-h|--help)$ ]]; then
  usage
  exit 0
fi

TARGET="$1"
MODE="${2:-runs}"

if [[ "$MODE" != "logs" && "$MODE" != "runs" ]]; then
  echo "Erro: modo inválido: $MODE. Use 'logs' ou 'runs'." >&2
  exit 1
fi

require_cmd gh

log "Validando autenticação do GitHub CLI"
gh auth status >/dev/null

if [[ "$TARGET" == *"/"* ]]; then
  # Repositório único
  cleanup_repo "$TARGET" "$MODE"
else
  # Organização ou usuário: listar todos os repositórios
  log "Buscando repositórios da organização/proprietário $TARGET"
  REPOS_RAW="$(gh repo list "$TARGET" --limit 4000 --json nameWithOwner --jq '.[].nameWithOwner' || true)"
  if [[ -z "$REPOS_RAW" ]]; then
    log "Nenhum repositório encontrado para $TARGET ou erro na listagem"
    exit 0
  fi

  REPOS=()
  while IFS= read -r line; do
    [[ -n "$line" ]] && REPOS+=("$line")
  done <<< "$REPOS_RAW"

  TOTAL_REPOS=${#REPOS[@]}
  log "Encontrados $TOTAL_REPOS repositório(s) em $TARGET"

  REPO_INDEX=0
  for r in "${REPOS[@]}"; do
    REPO_INDEX=$((REPO_INDEX + 1))
    printf '\n==================================================\n'
    printf '[%s/%s] Repositório: %s\n' "$REPO_INDEX" "$TOTAL_REPOS" "$r"
    printf '==================================================\n'
    cleanup_repo "$r" "$MODE"
  done
fi

log "Concluído com sucesso"