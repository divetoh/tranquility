#
# Upgrade DB to last revision
#

set -a
source ../.env.local
set +a

alembic upgrade head
