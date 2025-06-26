# Cosmos Query CLI

- Run queries against containers from the command line.
- Required for building: `python` `pip` `az` `make`
- Required for running: `COSMOS_ACCOUNT` `COSMOS_DATABASE` `COSMOS_CONTAINER` `COSMOS_DB_KEY` or supply them as arguments when running the binary.
- Help: `cosmos-query -h`
- How to get `COSMOS_DB_KEY`: `az cosmosdb keys list --name "account" --resource-group "rg" --query "primaryMasterKey" -o tsv`
- Build binary: `make dist` => `dist/cosmos-query`
