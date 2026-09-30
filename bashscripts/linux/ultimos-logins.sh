#!/usr/bin/env bash
set -euo pipefail

if (( EUID != 0 )); then
    echo "Execute com sudo: sudo bash ultimos-logins.sh" >&2
    exit 1
fi

if ! command -v lastlog >/dev/null 2>&1; then
    echo "Erro: o comando lastlog não está disponível." >&2
    exit 1
fi

min_uid=$(awk '$1 == "UID_MIN" { print $2; exit }' /etc/login.defs)
min_uid=${min_uid:-1000}
hoje=$(( $(date -u +%s) / 86400 ))

printf '%-24s %-13s %-15s %s\n' \
    "USUÁRIO" "CONTA" "SENHA" "ÚLTIMO LOGIN"

{
    while IFS=: read -r usuario _ uid _ _ _ shell; do
        [[ "$uid" =~ ^[0-9]+$ ]] || continue
        (( uid >= min_uid )) || continue
        [[ "$shell" != */nologin && "$shell" != */false ]] || continue

        if ! registro=$(getent shadow "$usuario"); then
            printf '4\t%s\t%s\t%s\t%s\n' \
                "$usuario" "DESCONHECIDA" "DESCONHECIDA" "—"
            continue
        fi

        senha=$(printf '%s\n' "$registro" | cut -d: -f2)
        expira=$(printf '%s\n' "$registro" | cut -d: -f8)

        conta="ATIVA"
        if [[ "$expira" =~ ^[0-9]+$ ]] && (( expira <= hoje )); then
            conta="EXPIRADA"
        fi

        case "$senha" in
            '!'*|'*'*)
                estado_senha="BLOQUEADA"
                ordem=1
                ;;
            '')
                estado_senha="SEM SENHA"
                ordem=2
                ;;
            *)
                estado_senha="UTILIZÁVEL"
                ordem=3
                ;;
        esac

        if ! ultimo_login=$(lastlog -u "$usuario" | tail -n +2); then
            ultimo_login="ERRO NA CONSULTA"
        fi
        [[ -n "$ultimo_login" ]] || ultimo_login="SEM REGISTRO"

        printf '%s\t%s\t%s\t%s\t%s\n' \
            "$ordem" "$usuario" "$conta" "$estado_senha" "$ultimo_login"
    done < /etc/passwd
} |
    sort -t $'\t' -k1,1n -k2,2 |
    awk -F '\t' '{
        printf "%-24s %-13s %-15s %s\n", $2, $3, $4, $5
    }'
