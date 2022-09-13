# Automata Binance Account Data Stream

## Docker
* `docker build . -t persuadertechnology/automata-account-data-stream:binance-0.1 && docker image prune --filter label=stage=BUILDER`

## Publishing to Docker Repository
todo: automate this...
1. `docker push persuadertechnology/automata-account-data-stream:binance-0.1`

## Publishing Prerequisites
Need to log in to via docker cli i.e. `docker login -u`

### IDE
1. Go to `Run`
2. Choose `Edit configurations...`
3. In `Paramaters:` 
   ```
   wss://stream.binance.com:9443/stream?streams={} 
   --options 
     REDIS_SERVER_ADDRESS=192.168.1.90 
     REDIS_SERVER_PORT=6379 
     TRADE_TRANSFORMATIONS_KEY=binance:trade:transformations  
     AUTH_URL=https://api.binance.com/api/v3/userDataStream 
     AUTH_INFO_KEY=binance:auth:info 
     MISSING_KEY=binance:missing 
     TRADE_KEY=binance:trade 
     POSITION_KEY=binance:position 
     TRADE_HISTORY_LIMIT=100 
     POSITION_HISTORY_LIMIT=100 
     PROCESS_KEY={}:process:status:{}  
     PROCESS_RUN_PROFILE_KEY={}:process:run-profile:{}  
   ```

## Environments

### Test
wss://testnet.binance.vision

### Live
wss://stream.binance.com:9443
