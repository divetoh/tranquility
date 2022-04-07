#
# Start uvicorn server inside docker container
#

echo "Checking database connection."

if python3 ./tool.await_db.py -eq 0
then
    echo "Success: Database avaliable."
else
    echo "Failed: Database not avaliable."
    exit 1
fi

echo "Upgrading database revision."
alembic upgrade head

python3 ./tool.init_db.py

echo "Starting uvicorn."
uvicorn app.main:app --reload --workers 5 --host 0.0.0.0 --port 5001
