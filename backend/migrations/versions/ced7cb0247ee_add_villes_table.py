"""Add villes table

Revision ID: ced7cb0247ee
Revises: 67c7312c6bf7
Create Date: 2025-07-20 18:32:10.634538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ced7cb0247ee'
down_revision = '67c7312c6bf7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('villes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('communes', sa.String(length=100), nullable=True),
    sa.Column('code_postal', sa.Integer(), nullable=True),
    sa.Column('code_insee', sa.Integer(), nullable=True),
    sa.Column('departement', sa.Integer(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('zone_nv', sa.Integer(), nullable=True),
    sa.Column('distance_km_oiseau', sa.Float(), nullable=True),
    sa.Column('distance_km_routes', sa.Float(), nullable=True),
    sa.Column('temps_route_min', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('test_cle2',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('libelle', sa.String(length=30), nullable=True),
    sa.Column('niveau_qualification_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['niveau_qualification_id'], ['niveau_qualification.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('maintenance_logs')
    op.drop_table('_alembic_tmp_niveau_qualification')
    op.drop_table('import_logs')
    with op.batch_alter_table('niveau_qualification', schema=None) as batch_op:
        batch_op.alter_column('niveau',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('categorie',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    with op.batch_alter_table('salaries', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('salaries', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    with op.batch_alter_table('niveau_qualification', schema=None) as batch_op:
        batch_op.alter_column('categorie',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('niveau',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    op.create_table('import_logs',
    sa.Column('fichier_source', sa.VARCHAR(length=200), nullable=False),
    sa.Column('table_destination', sa.VARCHAR(length=100), nullable=False),
    sa.Column('lignes_totales', sa.INTEGER(), nullable=True),
    sa.Column('lignes_importees', sa.INTEGER(), nullable=True),
    sa.Column('lignes_erreurs', sa.INTEGER(), nullable=True),
    sa.Column('date_import', sa.DATETIME(), nullable=False),
    sa.Column('duree_import', sa.NUMERIC(precision=10, scale=2), nullable=True),
    sa.Column('statut', sa.VARCHAR(length=20), nullable=True),
    sa.Column('erreurs', sa.TEXT(), nullable=True),
    sa.Column('notes', sa.TEXT(), nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('_alembic_tmp_niveau_qualification',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('niveau', sa.VARCHAR(length=100), nullable=False),
    sa.Column('categorie', sa.VARCHAR(length=100), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('maintenance_logs',
    sa.Column('type_operation', sa.VARCHAR(length=50), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=False),
    sa.Column('fichier_source', sa.VARCHAR(length=200), nullable=True),
    sa.Column('fichier_destination', sa.VARCHAR(length=200), nullable=True),
    sa.Column('taille_fichier', sa.NUMERIC(precision=10, scale=2), nullable=True),
    sa.Column('duree_operation', sa.NUMERIC(precision=10, scale=2), nullable=True),
    sa.Column('statut', sa.VARCHAR(length=20), nullable=True),
    sa.Column('erreurs', sa.TEXT(), nullable=True),
    sa.Column('notes', sa.TEXT(), nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('test_cle2')
    op.drop_table('villes')
    # ### end Alembic commands ###
