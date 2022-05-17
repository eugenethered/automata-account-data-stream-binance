    # Automata Binance Account Data Stream

## Packaging
`python3 -m build`

## Dependencies (IDE Terminal)
`pip install persuader-technology-automata-core persuader-technology-automata-data.stream persuader-technology-automata-trade-repository`

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
   ```

## Environments

### Test
wss://testnet.binance.vision

### Live
wss://stream.binance.com:9443
