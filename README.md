# Cosmos Query CLI

```bash
cosmos-query -a myaccount -d mydb -c mycont -q "SELECT * FROM c" | jq
```

### Environment

```bash
export COSMOS_ACCOUNT="your-account"
export COSMOS_DATABASE="your-database"
export COSMOS_CONTAINER="your-container"
export COSMOS_DB_KEY="your-key"
```

### Get Cosmos DB Key

```bash
az cosmosdb keys list --name "account" --resource-group "rg" --query "primaryMasterKey" -o tsv
```
