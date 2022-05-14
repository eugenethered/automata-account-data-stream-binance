#!/bin/bash
# Refresh account Listen Key

# 1. Set the API Key
API_KEY="[YOUR-API-KEY]"

# 2. Set existing Listen Key
LISTEN_KEY="[EXISTING-LISTEN-KEY]"

# 3. PUT request
BINANCE_BASE_URL="https://api.binance.com/api/v3/userDataStream"

echo -e "\nListen Key API\n"

URL=${BINANCE_BASE_URL}

curl -H "X-MBX-APIKEY: ${API_KEY}" -X PUT $URL -d "listenKey=${LISTEN_KEY}"

echo -e "\n\nURL: $URL\n"
