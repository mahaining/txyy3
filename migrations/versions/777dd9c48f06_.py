"""empty message

Revision ID: 777dd9c48f06
Revises: 598cfa6dcffc
Create Date: 2018-03-15 16:10:06.691754

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '777dd9c48f06'
down_revision = '598cfa6dcffc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('health_recor')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('health_recor',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('user_id', mysql.VARCHAR(collation='utf8_bin', length=100), nullable=False),
    sa.Column('mobile', mysql.VARCHAR(collation='utf8_bin', length=200), nullable=False),
    sa.Column('real_name', mysql.VARCHAR(collation='utf8_bin', length=200), nullable=False),
    sa.Column('id_card', mysql.VARCHAR(collation='utf8_bin', length=100), nullable=False),
    sa.Column('age', mysql.VARCHAR(collation='utf8_bin', length=100), nullable=False),
    sa.Column('sex', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('weight', mysql.VARCHAR(collation='utf8_bin', length=200), nullable=False),
    sa.Column('height', mysql.VARCHAR(collation='utf8_bin', length=100), nullable=False),
    sa.Column('remark', mysql.VARCHAR(collation='utf8_bin', length=250), nullable=False),
    sa.Column('consultant_id', mysql.VARCHAR(collation='utf8_bin', length=250), nullable=False),
    sa.Column('create_at', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('update_at', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('outer_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('outer_consultant_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8_bin',
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
