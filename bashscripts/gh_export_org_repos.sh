#!/usr/bin/env bash
#
# Script para percorrer todas as organizações do usuário autenticado no gh CLI,
# listar todos os repositórios públicos de cada organização e exportar um CSV
# contendo: organização, projeto, descrição da organização e descrição do repositório.
#

OUTPUT_FILE="${1:-repos_organizacoes.csv}"

echo "Buscando organizações..."
orgs=$(gh api user/orgs --paginate)

if [ -z "$orgs" ]; then
  echo "Nenhuma organização encontrada ou erro ao consultar a API do GitHub."
  exit 1
fi

total_orgs=$(echo "$orgs" | jq -s 'add | length')
echo "Encontradas $total_orgs organizações."

# Cabeçalho do CSV
echo '"organizacao","projeto","descricao_organizacao","descricao_repositorio"' > "$OUTPUT_FILE"

echo "$orgs" | jq -c '.[]' | while read -r org; do
  login=$(echo "$org" | jq -r '.login')
  org_desc=$(echo "$org" | jq -r '.description // ""')
  
  echo "Processando organização: $login..."
  
  repos=$(gh repo list "$login" --visibility public --limit 1000 --json name,description)
  
  if [ -n "$repos" ] && [ "$repos" != "[]" ]; then
    count=$(echo "$repos" | jq '. | length')
    echo "  -> Encontrados $count repositórios públicos."
    
    echo "$repos" | jq -c '.[]' | while read -r repo; do
      repo_name=$(echo "$repo" | jq -r '.name')
      repo_desc=$(echo "$repo" | jq -r '.description // ""')
      
      jq -n --arg org "$login" --arg repo "$repo_name" --arg org_desc "$org_desc" --arg repo_desc "$repo_desc" \
        '[$org, $repo, $org_desc, $repo_desc] | @csv' -r >> "$OUTPUT_FILE"
    done
  else
    echo "  -> Nenhum repositório público encontrado."
  fi
done

echo "Sucesso! Exportação concluída em '$OUTPUT_FILE'."
