"""Add Asset.Update_at function/trigger

Revision ID: f59c5bd62842
Revises: 2a5898cfa787
Create Date: 2023-01-12 11:23:25.266977

"""
from alembic import op
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger

# import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "f59c5bd62842"
down_revision = "2a5898cfa787"
branch_labels = None
depends_on = None

schema = "public"
table_name = "asset"

update_at_auto_f59c5bd62842 = PGFunction(
    schema=schema,
    signature="updated_at_auto()",
    definition="""
        RETURNS TRIGGER LANGUAGE plpgsql AS $$
        BEGIN
          NEW.updated_at = NOW();
          RETURN NEW;
        END;
        $$;
    """,
)

asset_update_at_3d49ca673bb5 = PGTrigger(
    schema=schema,
    signature=f"tr_{table_name}_updated_at",
    on_entity=f"{schema}.{table_name}",
    definition=f"""
        BEFORE UPDATE ON {schema}.{table_name}
        FOR EACH ROW EXECUTE PROCEDURE {schema}.updated_at_auto()
    """,
)


def upgrade() -> None:
    op.create_entity(update_at_auto_f59c5bd62842)
    op.create_entity(asset_update_at_3d49ca673bb5)


def downgrade() -> None:
    op.drop_entity(asset_update_at_3d49ca673bb5)
    op.drop_entity(update_at_auto_f59c5bd62842)
