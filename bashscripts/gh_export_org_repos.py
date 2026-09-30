#!/usr/bin/env python3
"""
Script para percorrer todas as organizações do usuário autenticado no gh CLI,
listar todos os repositórios públicos de cada organização e exportar um CSV
contendo: organização, projeto, descrição da organização e descrição do repositório.
"""

import csv
import json
import subprocess
import sys

def main():
    output_file = sys.argv[1] if len(sys.argv) > 1 else "repos_organizacoes.csv"

    print("Buscando organizações...")
    cmd_orgs = ["gh", "api", "user/orgs", "--paginate"]
    res_orgs = subprocess.run(cmd_orgs, capture_output=True, text=True, encoding="utf-8", check=True)
    orgs = json.loads(res_orgs.stdout)

    print(f"Encontradas {len(orgs)} organizações.")
    rows = []

    for i, org in enumerate(orgs, 1):
        org_name = org.get("login", "")
        org_desc = org.get("description", "") or ""
        print(f"[{i}/{len(orgs)}] Processando organização: {org_name}...")

        cmd_repos = [
            "gh", "repo", "list", org_name,
            "--visibility", "public",
            "--limit", "1000",
            "--json", "name,description"
        ]
        res_repos = subprocess.run(cmd_repos, capture_output=True, text=True, encoding="utf-8", check=False)
        if res_repos.returncode != 0:
            print(f"  -> Erro ao acessar repositórios de {org_name}: {res_repos.stderr.strip()}", file=sys.stderr)
            continue

        try:
            repos = json.loads(res_repos.stdout)
        except json.JSONDecodeError:
            print(f"  -> Erro ao decodificar JSON dos repositórios de {org_name}", file=sys.stderr)
            continue

        print(f"  -> Encontrados {len(repos)} repositórios públicos.")
        for repo in repos:
            repo_name = repo.get("name", "")
            repo_desc = repo.get("description", "") or ""

            rows.append({
                "organizacao": org_name,
                "projeto": repo_name,
                "descricao_organizacao": org_desc,
                "descricao_repositorio": repo_desc
            })

    with open(output_file, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["organizacao", "projeto", "descricao_organizacao", "descricao_repositorio"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSucesso! Total de {len(rows)} repositórios exportados para '{output_file}'.")

if __name__ == "__main__":
    main()
