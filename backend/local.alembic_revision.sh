#
# Make new DB revision
#
# Usage: ./alembic_revision.sh "Revision message"
#

set -a
source ../.env.local
set +a

alembic revision --autogenerate -m "$1"
