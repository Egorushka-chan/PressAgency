import enum


class User:
    def __init__(self, login, rank):
        self.login = login
        self.rank = rank


class UserRank(enum.Enum):
    employee = 1
    admin = 2
    intern = 3
