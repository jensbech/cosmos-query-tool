CLI tool to query cosmosdb containers, e.g. `cosmos-query -q "SELECT * from c`

- Required for building: `python` `pip` `az` `make`
- Required for running: `COSMOS_ACCOUNT` `COSMOS_DATABASE` `COSMOS_CONTAINER` `COSMOS_DB_KEY` or supply them as arguments.
- How to get `COSMOS_DB_KEY`: `az cosmosdb keys list --name "account" --resource-group "rg" --query "primaryMasterKey" -o tsv`
- Build binary: `make dist` => `dist/cosmos-query`
