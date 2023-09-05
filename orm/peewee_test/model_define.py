import os
from datetime import datetime
from typing import Optional

import peewee

from log.logger import init_logger

db = peewee.MySQLDatabase(
    'peewee_test',
    host=os.getenv('MYSQL_HOST'),
    port=int(os.getenv('MYSQL_PORT')),  # type: ignore
    user=os.getenv('MYSQL_USER'),
    passwd=os.getenv('MYSQL_PASS'),
)


class User(peewee.Model):
    id = peewee.BigAutoField(primary_key=True)
    username = peewee.CharField(max_length=200)

    class Meta:
        database = db


class Tweet(peewee.Model):
    user = peewee.ForeignKeyField(User, backref='tweets')
    message = peewee.TextField()
    created_date = peewee.DateTimeField(
        default=datetime.now, formats='%Y-%m-%d %H:%M:%S'
    )
    is_published = peewee.BooleanField(default=True)
    updated_date = peewee.DateTimeField(
        default=datetime.now, formats='%Y-%m-%d %H:%M:%S'
    )

    class Meta:
        database = db


def search_user(username: str) -> Optional[User]:
    try:
        user = User.get(User.username == username)
        return user
    except peewee.DoesNotExist:
        return None


def main():
    # 0. 初始化日志模块
    logger = init_logger(
        # other_modulle='peewee', # log other module
        log_file_name=os.path.basename(__file__).rstrip('.py'),
    )

    # 1. create table
    db.connect()
    db.create_tables([User, Tweet])
    db.close()

    # 2. insert data
    # lily = User(username='lily')
    # lily.save()

    # User.create(username='lucy')
    # User.create(username='lucy1')
    # User.create(username='lucy2')
    # User.create(username='lucy3')
    # User.create(username='lucy4')
    # User.create(username='lucy5')
    # User.create(username='lucy6')
    # User.create(username='lucy7')
    # User.create(username='lucy8')

    # 3. query data

    # 3.1 get all data
    users = User.select()  # 1. 仅组装sql语句，不执行；2. 返回的是一个可迭代对象 peewee.ModelSelect
    for u in users:
        logger.debug(u.username)

    # 3.2 get one data
    logger.debug('-' * 50)
    usernames = ('lily', 'lucy', 'tom')
    for u in usernames:
        user = search_user(u)
        if user:
            logger.debug(user.username)
        else:
            logger.debug(f'{u} is not exist')

    # 3.3 get some data
    logger.debug('-' * 50)
    users = User.select().where(User.username.in_(usernames))
    for u in users:
        logger.debug(u.username)

    # 4. update data
    logger.debug('-' * 50)
    # 4.1 use save()
    lily = User(id=5, username='lilyoooo')
    rows = lily.save()
    logger.debug(f'rows: {rows}')

    # 4.2 use update()
    u = User.update(username='Throdora').where(
        User.id == 3
    )  # 1. 仅组装sql语句，不执行；2. 返回的是一个 peewee.ModelUpdate
    rows = u.execute()  # 执行sql语句
    logger.debug(f'rows: {rows}')

    # 5. delete data
    logger.debug('-' * 50)
    # 5.1 use delete_instance()
    lucy3 = User.get(User.username == 'lucy3')
    rows = lucy3.delete_instance()
    logger.debug(f'rows: {rows}')

    # 5.2 use delete()
    query = User.delete().where(
        User.username == 'lucy4'
    )  # 1. 仅组装sql语句，不执行；2. 返回的是一个 peewee.ModelDelete
    rows = query.execute()
    logger.debug(f'rows: {rows}')
