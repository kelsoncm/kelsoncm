#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  cat <<'EOF'
Uso:
  ./gh-actions-cleanup.sh OWNER/REPO [logs|runs]

Exemplos:
  ./gh-actions-cleanup.sh cte-zl-ifrn/integration-avaintegration_metapackage
  ./gh-actions-cleanup.sh cte-zl-ifrn/integration-avaintegration_metapackage logs
  ./gh-actions-cleanup.sh cte-zl-ifrn/integration-avaintegration_metapackage runs

Padrão:
  runs  -> apaga todas as workflow runs

Requisitos:
  - gh autenticado com permissão de escrita no repositório
  - jq instalado
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

if [[ $# -lt 1 ]] || [[ "${1:-}" =~ ^(-h|--help)$ ]]; then
  usage
  exit 0
fi

REPO="$1"
MODE="${2:-runs}"

if [[ "$MODE" != "logs" && "$MODE" != "runs" ]]; then
  echo "Erro: modo inválido: $MODE. Use 'logs' ou 'runs'." >&2
  exit 1
fi

require_cmd gh
require_cmd jq

log "Validando autenticação do GitHub CLI"
gh auth status >/dev/null

log "Buscando workflow runs de $REPO"
RUN_IDS="$(
  gh api \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    --paginate \
    "/repos/$REPO/actions/runs?per_page=100" \
  | jq -r '.workflow_runs[]?.id'
)"

if [[ -z "$RUN_IDS" ]]; then
  log "Nenhuma workflow run encontrada em $REPO"
  exit 0
fi

TOTAL="$(printf '%s\n' "$RUN_IDS" | wc -l | tr -d ' ')"
log "Encontradas $TOTAL workflow runs"

COUNT=0
while IFS= read -r RUN_ID; do
  [[ -z "$RUN_ID" ]] && continue
  COUNT=$((COUNT + 1))

  if [[ "$MODE" == "logs" ]]; then
    printf '\r[%s/%s] Apagando logs da run %s...' "$COUNT" "$TOTAL" "$RUN_ID"
    gh api \
      --silent \
      --method DELETE \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      "/repos/$REPO/actions/runs/$RUN_ID/logs" \
      || printf '\nFalha ao apagar logs da run %s\n' "$RUN_ID" >&2
  else
    printf '\r[%s/%s] Apagando run %s...' "$COUNT" "$TOTAL" "$RUN_ID"
    gh api \
      --silent \
      --method DELETE \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      "/repos/$REPO/actions/runs/$RUN_ID" \
      || printf '\nFalha ao apagar run %s\n' "$RUN_ID" >&2
  fi

  sleep 0.1
done <<< "$RUN_IDS"

printf '\n'
log "Concluído"