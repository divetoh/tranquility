#
# Make new DB revision
#
# Usage: ./alembic_revision.sh "Revision message"
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

alembic revision --autogenerate -m "$1"
