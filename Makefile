ifeq ($(strip $(shell curl -s -H Metadata:true --noproxy "*" -m 5 "http://169.254.169.254/metadata/instance?api-version=2021-02-01")),)
	# We are running locally
	key_vault_access_token=$(shell az account get-access-token --resource=https://vault.azure.net | jq -r ".accessToken")
else
	# We are running in Azure
	key_vault_access_token=$(shell curl 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://vault.azure.net' -H Metadata:true | jq -r ".access_token")
endif

define ENV_VARS
	OPENAI_API_KEY=$(shell curl 'https://kvi4dlzaihub01.vault.azure.net/secrets/azure-openai-key?api-version=2016-10-01' -H "Authorization: Bearer ${key_vault_access_token}" | jq -r ".value") \
    STORAGE_ACCOUNT_URL="https://prodadlmlops1.blob.core.windows.net"
endef

build:
	${ENV_VARS} docker compose build


