#
# Initialize venv, install (update) requirements.
#
set -a
source ../.env.local
set +a

if [ ! -f "./.venv/bin/activate" ]; then
    echo "* Check python version"
    if python3 -c 'import sys; assert sys.version_info >= (3,9)' > /dev/null 2> /dev/null; then
      PYTHON='python3'
      echo "* Using: python3"
    elif python3.9 -c 'import sys; assert sys.version_info >= (3,9)' > /dev/null 2> /dev/null; then
      PYTHON='python3.9'
      echo "* Using: python3.9"
    elif python3.10 -c 'import sys; assert sys.version_info >= (3,9)' > /dev/null 2> /dev/null; then
      PYTHON='python3.10'
      echo "* Using: python3.10"
    else
      echo "! Error: Can't find python 3.9 or later."
    fi

    echo "* Create venv."
    $PYTHON -m venv .venv
    if [ $? -ne 0 ]; then
      echo "! Error: Failed to create venv. Check venv package installation."
      exit 1
    fi
fi

echo "* Activate venv."
source ./.venv/bin/activate

echo "* Install requirements."
pip install wheel
pip install --no-cache-dir --upgrade -r requirements.txt

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

python3 ./tool.init_db.py
