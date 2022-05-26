#
# Start uvicorn server
#
set -a
source ../.env.test.local
set +a

if [ -f "./.venv/bin/activate" ]; then
    echo "Activate venv."
    source ./.venv/bin/activate
else
    echo "No venv found, use system python installation."
fi

echo "* Check database connection."

if python3 ./tool.await_db.py -eq 0
then
    echo "* Success: Database avaliable."
else
    echo "* Failed: Database not avaliable."
    exit 1
fi

echo "* Upgrade database to last revision."
alembic upgrade head

pytest app/tests "${@}"
