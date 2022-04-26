#
# Start uvicorn server
#
set -a
source ../.env.local
set +a

if [ -f "./.venv/bin/activate" ]; then
    echo "Activate venv."
    source ./.venv/bin/activate
fi

python3 ./tool.delete_demo_users.py
