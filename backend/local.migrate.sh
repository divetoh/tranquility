#
# Start uvicorn server
#
set -a
source ../.env.local
set +a

if [ -f "./.venv/bin/activate" ]; then
    echo "Activate venv."
    source ./.venv/bin/activate
else
    echo "No venv found, use system python installation."
fi

pip install --no-cache-dir --upgrade -r requirements.txt

alembic upgrade head

python3 ./tool.migrate_db.py
