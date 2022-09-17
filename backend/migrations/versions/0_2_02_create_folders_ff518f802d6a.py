"""0.2.02 Create folders

Revision ID: ff518f802d6a
Revises: a9dc3ed4b0e7
Create Date: 2022-09-05 17:14:18.261502

"""
from alembic import op
import sqlalchemy as sa
import json

# revision identifiers, used by Alembic.
revision = 'ff518f802d6a'
down_revision = 'a9dc3ed4b0e7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('folder',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('parent', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('foldertype', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['parent'], ['folder.uid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['user.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_folder_parent'), 'folder', ['parent'], unique=False)
    op.create_index(op.f('ix_folder_uid'), 'folder', ['uid'], unique=False)
    op.create_index(op.f('ix_folder_user'), 'folder', ['user'], unique=False)
    op.add_column('jsondoc', sa.Column('folder', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_jsondoc_folder'), 'jsondoc', ['folder'], unique=False)
    op.create_foreign_key(None, 'jsondoc', 'folder', ['folder'], ['uid'], ondelete='CASCADE')
    op.add_column('markdown', sa.Column('folder', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_markdown_folder'), 'markdown', ['folder'], unique=False)
    op.create_foreign_key(None, 'markdown', 'folder', ['folder'], ['uid'], ondelete='CASCADE')

    # I love the smell of raw SQL in the morning
    
    # Create folder structure from user data
    conn = op.get_bind()
    users = conn.execute(sa.text("SELECT uid, coretasklist FROM \"user\"")).all()
    for user, coretasklist in users:
        query = f"INSERT INTO folder (\"user\", name, foldertype) VALUES \
                    ({user}, '.inbox', 32), ({user}, '.system', 64), ({user}, '.activity', 65) \
                    RETURNING uid"
        fid_inbox, fid_system, fid_act = conn.scalars(sa.text(query)).all()

        # Organizing activities folders
        query = f"SELECT uid, jsondoc FROM jsondoc WHERE \"user\"={user} AND doctype='activity'"
        activities = conn.execute(sa.text(query)).all()
        workspaces = {}
        for uid, act_doc in activities:
            query = f"INSERT INTO folder (\"user\", name, foldertype, parent) \
                    (SELECT {user}, name, 1, {fid_act} FROM jsondoc WHERE uid={uid}) \
                    RETURNING uid"
            fld_act_id = conn.scalars(sa.text(query)).one()
            query = f"UPDATE jsondoc SET folder={fld_act_id} WHERE uid={uid}"
            conn.execute(sa.text(query))
            try:
                for i in json.loads(act_doc)["workspaces"]:
                    workspaces[i] = fld_act_id
            except:
                print(f"Can't parse activity {uid}")
        
        # Organizing workspace folders
        for uid, act_fld_id in workspaces.items():
            query = f"INSERT INTO folder (\"user\", name, foldertype, parent) \
                    (SELECT {user}, name, 1, {act_fld_id} FROM jsondoc WHERE uid={uid} AND \
                    \"user\"={user} AND doctype='workspace') RETURNING uid"
            fld_wsp_id = conn.scalars(sa.text(query)).first()
            if not fld_wsp_id:
                continue
            query = f"UPDATE jsondoc SET folder={fld_wsp_id} WHERE uid={uid}"
            conn.execute(sa.text(query))

            # Move markdown and tasklist to workspace folder
            try:
                query = f"SELECT jsondoc FROM jsondoc WHERE uid={uid}"                
                workspace = json.loads(conn.scalars(sa.text(query)).one())
                if workspace["type"] != "column":
                    continue
                for col in workspace["content"]:
                    for row in col["content"]:
                        if row["type"] == "tasklist":
                            query = f"UPDATE jsondoc SET folder={fld_wsp_id} WHERE uid={int(row['uid'])} AND \
                                    \"user\"={user} AND doctype='tasklist'"
                            conn.execute(sa.text(query))
                        elif row["type"] == "markdown":
                            query = f"UPDATE markdown SET folder={fld_wsp_id} WHERE uid={int(row['uid'])} AND \
                                    \"user\"={user}"
                            conn.execute(sa.text(query))
            except:
                print(f"Can't parse workspace {uid}")
        
        # Move all other jsondoc and markdown to .inbox
        query = f"UPDATE jsondoc SET folder={fid_inbox} WHERE \"user\"={user} AND folder IS NULL"
        conn.execute(sa.text(query))
        query = f"UPDATE markdown SET folder={fid_inbox} WHERE \"user\"={user} AND folder IS NULL"
        conn.execute(sa.text(query))

        # Move coretasklist to .system
        query = f"UPDATE jsondoc SET folder={fid_system} WHERE \"user\"={user} AND uid={coretasklist}"
        conn.execute(sa.text(query))

def downgrade():
    op.drop_constraint('markdown_folder_fkey', 'markdown', type_='foreignkey')
    op.drop_index(op.f('ix_markdown_folder'), table_name='markdown')
    op.drop_column('markdown', 'folder')
    op.drop_constraint('jsondoc_folder_fkey', 'jsondoc', type_='foreignkey')
    op.drop_index(op.f('ix_jsondoc_folder'), table_name='jsondoc')
    op.drop_column('jsondoc', 'folder')
    op.drop_index(op.f('ix_folder_user'), table_name='folder')
    op.drop_index(op.f('ix_folder_uid'), table_name='folder')
    op.drop_index(op.f('ix_folder_parent'), table_name='folder')
    op.drop_table('folder')
