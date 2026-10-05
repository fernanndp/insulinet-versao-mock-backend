"""add insulin type to insulin

Revision ID: 82c25376dc25
Revises: 502ed726affa
Create Date: 2026-10-04 20:59:35.551776

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "82c25376dc25"
down_revision: Union[str, Sequence[str], None] = "502ed726affa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    insulin_type = postgresql.ENUM(
        "REGULAR",
        "NPH",
        "GLARGINA",
        "LISPRO",
        name="insulin_type_mock",
        create_type=False,
    )

    op.add_column(
        "insulin",
        sa.Column(
            "insulin_type",
            insulin_type,
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "insulin",
        "insulin_type",
    )