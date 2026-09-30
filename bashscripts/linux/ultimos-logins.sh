#!/usr/bin/env bash

# Use:
# curl -fsSL 'https://raw.githubusercontent.com/kelsoncm/kelsoncm/refs/heads/main/bashscripts/linux/ultimos-logins.sh' | sudo bash

set -euo pipefail

min_uid=$(awk '$1 == "UID_MIN" { print $2; exit }' /etc/login.defs)
min_uid=${min_uid:-1000}

while IFS=: read -r usuario _ uid _ _ _ shell; do
    if (( uid >= min_uid )) && [[ "$shell" != */nologin && "$shell" != */false ]]; then
        lastlog -u "$usuario" | tail -n +2
    fi
done < /etc/passwd
