"""Add foreign key constraint to test_cle2

Revision ID: e189113ea343
Revises: cf925e256a76
Create Date: 2025-07-19 08:43:29.417626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e189113ea343'
down_revision = 'cf925e256a76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('test_audit_table', schema=None) as batch_op:
        batch_op.alter_column(
            'nom',
            existing_type=sa.VARCHAR(length=100),
            nullable=True
        )
        batch_op.alter_column(
            'prix',
            existing_type=sa.NUMERIC(precision=10, scale=2),
            type_=sa.Float(),
            existing_nullable=True
        )

    with op.batch_alter_table('test_cle2', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'fk_test_cle2_niveau_qualification',
            'niveau_qualification',
            ['niveau_qualification_id'],
            ['id'],
            ondelete='SET NULL'
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('test_cle2', schema=None) as batch_op:
        batch_op.drop_constraint('fk_test_cle2_niveau_qualification', type_='foreignkey')

    with op.batch_alter_table('test_audit_table', schema=None) as batch_op:
        batch_op.alter_column(
            'prix',
            existing_type=sa.Float(),
            type_=sa.NUMERIC(precision=10, scale=2),
            existing_nullable=True
        )
        batch_op.alter_column(
            'nom',
            existing_type=sa.VARCHAR(length=100),
            nullable=False
        )

    # ### end Alembic commands ###
