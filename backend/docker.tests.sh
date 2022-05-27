#
# Start uvicorn server inside docker container
#

echo "Checking database connection."

if python3 ./tool.await_db.py cleanup -eq 0
then
    echo "Success: Database avaliable."
else
    echo "Failed: Database not avaliable."
    exit 1
fi

echo "Upgrading database revision."
alembic upgrade head

echo "Start tests."
pytest app/tests
