{
    while IFS=: read -r usuario _ uid _ _ _ shell; do
        [[ "$uid" =~ ^[0-9]+$ ]] || continue
        (( uid >= min_uid )) || continue
        [[ "$shell" != */nologin && "$shell" != */false ]] || continue

        if ! registro=$(getent shadow "$usuario"); then
            printf '4\t%-24s %-11s %-15s %s\n' \
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

        printf '%s\t%-24s %-11s %-15s %s\n' \
            "$ordem" "$usuario" "$conta" "$estado_senha" "$ultimo_login"
    done < /etc/passwd
} | sort -t $'\t' -k1,1n -k2,2 | cut -f2-
