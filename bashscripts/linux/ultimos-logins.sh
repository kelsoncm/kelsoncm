#!/usr/bin/env bash
set -euo pipefail

if (( EUID != 0 )); then
    echo "Execute com sudo para consultar os dados das contas." >&2
    exit 1
fi

min_uid=$(awk '$1 == "UID_MIN" { print $2; exit }' /etc/login.defs)
min_uid=${min_uid:-1000}
hoje=$(( $(date -u +%s) / 86400 ))

printf '%-24s %-11s %-15s %s\n' \
    "USUÁRIO" "CONTA" "SENHA" "ÚLTIMO LOGIN"

while IFS=: read -r usuario _ uid _ _ _ shell; do
    [[ "$uid" =~ ^[0-9]+$ ]] || continue
    (( uid >= min_uid )) || continue
    [[ "$shell" != */nologin && "$shell" != */false ]] || continue

    if ! registro=$(getent shadow "$usuario"); then
        printf '%-24s %-11s %-15s %s\n' \
            "$usuario" "DESCONHECIDA" "DESCONHECIDA" "—"
        continue
    fi

    IFS=: read -r _ senha _ _ _ _ _ expira _ <<< "$registro"

    conta="ATIVA"
    if [[ -n "$expira" && "$expira" =~ ^[0-9]+$ ]] &&
       (( expira <= hoje )); then
        conta="EXPIRADA"
    fi

    case "$senha" in
        '!'*|'*'*) estado_senha="BLOQUEADA" ;;
        '')       estado_senha="SEM SENHA" ;;
        *)        estado_senha="UTILIZÁVEL" ;;
    esac

    if ! ultimo_login=$(lastlog -u "$usuario" | tail -n +2); then
        ultimo_login="ERRO NA CONSULTA"
    fi
    [[ -n "$ultimo_login" ]] || ultimo_login="SEM REGISTRO"

    printf '%-24s %-11s %-15s %s\n' \
        "$usuario" "$conta" "$estado_senha" "$ultimo_login"
done < /etc/passwd
