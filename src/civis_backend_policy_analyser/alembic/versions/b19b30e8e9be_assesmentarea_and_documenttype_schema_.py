"""AssesmentArea and DocumentType schema updated to include relationship

Revision ID: b19b30e8e9be
Revises: 76733c59ca0e
Create Date: 2025-06-08 18:29:44.567661

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b19b30e8e9be'
down_revision: Union[str, None] = '76733c59ca0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document_type_assessment_area',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('doc_type_id', sa.Integer(), nullable=True),
    sa.Column('assessment_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_on', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['assessment_id'], ['assessment_area.assessment_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['doc_type_id'], ['document_type.doc_type_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('doc_type_id', 'assessment_id', name='_doc_type_assessment_uc')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('document_type_assessment_area')
    # ### end Alembic commands ###
