import sqlalchemy as sa


def get_engine():
    return sa.create_engine("sqlite:///db/bcr.db")
