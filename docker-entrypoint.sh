#!/usr/bin/env sh

export $(cat src/db/conf/cache | xargs)
./wait-for-it.sh --timeout=0 -s "$REDIS_HOST":"$REDIS_PORT"

export $(cat src/db/conf/db | xargs)
./wait-for-it.sh --timeout=0 -s "$POSTGRES_HOST":"$POSTGRES_PORT"

alembic revision --autogenerate -m 'database init'
alembic upgrade head

python3 src/cli/main.py --write

python3 src/core/main.py