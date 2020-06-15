import logging

import datetime
from uuid import uuid4

import peewee as pw
from passlib.hash import argon2

logger = logging.getLogger(__name__)

database_proxy = pw.DatabaseProxy()
db = None


def generate_uuid():
    return uuid4().hex


def utcnow():
    return datetime.datetime.utcnow()


def database_init(database: str) -> pw.Database:
    global db
    _db = pw.SqliteDatabase(database, pragmas=(
        ('cache_size', -1024 * 64),
        ('journal_mode', 'wal'),
        ('foreign_keys', 1)))
    db = _db
    database_proxy.initialize(db)
    db.connect()
    db.create_tables([
        Account,
    ])
    return db


class Model(pw.Model):
    uuid = pw.CharField(
        index=True,
        unique=True,
        primary_key=True,
        default=generate_uuid)
    created_at = pw.DateTimeField(default=utcnow)
    modified_at = pw.DateTimeField()

    def save(self, *args, **kwargs):
        self.modified_at = utcnow()
        super().save(*args, **kwargs)

    class Meta:
        database = database_proxy


class Account(Model):
    name = pw.CharField(index=True, unique=True)
    password = pw.CharField()
    last_login = pw.DateTimeField(default=utcnow)

    @staticmethod
    def register(name: str, password: str) -> 'Account':
        hashed_password = argon2.hash(password)
        account = Account.create(name=name, password=hashed_password)
        logger.info(f'Account created: {account.name}')
        return account

    @staticmethod
    def login(name: str, password: str) -> 'Account':
        account = Account.get_or_none(name=name)
        if not account:
            raise KeyError(f'Acount with name {name!r} not found.')
        if argon2.verify(password, account.password):
            account.last_login = utcnow()
            return account
        raise ValueError(f'Password for account {name!r} did not match.')

    @staticmethod
    def destroy(name: str) -> None:
        account = Account.get(name=name)
        account.delete_instance()


class Topic(Model):
    name = pw.CharField(index=True, unique=True)
    content = pw.TextField()


class RelatedTopic(Model):
    topic = pw.ForeignKeyField(Topic)
    related = pw.ForeignKeyField(Topic)
