FROM python:3.10.6-alpine AS BUILDER
LABEL stage=BUILDER
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10.6-alpine
RUN addgroup apprunner && adduser apprunner -D -H -G apprunner
USER apprunner
WORKDIR /app
COPY --from=BUILDER /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --chown=apprunner:apprunner ./binance ./binance

ENV PYTHONPATH="${PYTHONPATH}:/app/binance" \
    REDIS_SERVER_ADDRESS=127.0.0.1 \
    REDIS_SERVER_PORT=6379 \
    TRADE_TRANSFORMATIONS_KEY=binance:transformation:mv:trade \
    AUTH_URL=https://api.binance.com/api/v3/userDataStream \
    AUTH_INFO_KEY=binance:auth:info \
    MISSING_KEY=binance:mv:missing \
    TRADE_KEY=binance:trade \
    POSITION_KEY=binance:position \
    TRADE_HISTORY_LIMIT=100 \
    POSITION_HISTORY_LIMIT=100

CMD ["python", "binance/__main__.py"]
