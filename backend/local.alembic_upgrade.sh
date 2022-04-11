#
# Upgrade DB to last revision
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

if [ -f "./.venv/bin/activate" ]; then
    echo "Activate venv."
    source ./.venv/bin/activate
else
    echo "No venv found, use system python installation."
fi

alembic upgrade head
