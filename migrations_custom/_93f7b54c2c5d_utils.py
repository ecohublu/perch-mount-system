from alembic import op


ENUMS = ("contributiontype",)


def downgrade_ext():
    for name in ENUMS:
        op.execute(f"DROP TYPE IF EXISTS {name} CASCADE;")
