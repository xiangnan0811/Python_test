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


class BaseModel(peewee.Model):
    created_date = peewee.DateTimeField(
        default=datetime.now, formats='%Y-%m-%d %H:%M:%S'
    )
    updated_date = peewee.DateTimeField(
        default=datetime.now, formats='%Y-%m-%d %H:%M:%S'
    )
    class Meta:
        database = db


class User(BaseModel):
    username = peewee.CharField(max_length=200)


class Tweet(BaseModel):
    content = peewee.TextField()
    timestamp = peewee.DateTimeField(default=datetime.now)
    user = peewee.ForeignKeyField(User, backref='tweets')


class Favorite(BaseModel):
    user = peewee.ForeignKeyField(User, backref='favorites')
    tweet = peewee.ForeignKeyField(Tweet, backref='favorites')


def populate_test_data():
    # db.create_tables([User, Tweet, Favorite])

    data = (
        ('huey', ('meow', 'hiss', 'purr')),
        ('mickey', ('woof', 'whine')),
        ('zaizee', ()))
    for username, tweets in data:
        user = User.create(username=username)
        for tweet in tweets:
            Tweet.create(user=user, content=tweet)

    # Populate a few favorites for our users, such that:
    favorite_data = (
        ('huey', ['whine']),
        ('mickey', ['purr']),
        ('zaizee', ['meow', 'purr']))
    for username, favorites in favorite_data:
        user = User.get(User.username == username)
        for content in favorites:
            tweet = Tweet.get(Tweet.content == content)
            Favorite.create(user=user, tweet=tweet)


def main():
    # 0. 初始化日志模块
    logger = init_logger(
        # other_modulle='peewee', # log other module
        log_file_name=os.path.basename(__file__).rstrip('.py'),
    )
    # 1. create table
    # db.connect()
    # db.create_tables([User, Tweet, Favorite])

    # 2. populate test data
    # populate_test_data()

    # 3. tweet join user
    # select 中如果不加查询字段,则只返回Tweet表中的数据, 可以通过Tweet.user.username来访问User表中的数据, 但是会多次查询数据库
    # select 中可以增加多个表的字段, 但是需要注意, 如果多个表中有相同的字段, 则需要指定别名,后续无需再次查user表
    # join 中可以通过 on 参数来灵活指定关联条件
    # query = Tweet.select().join(User).where(User.username == 'huey')
    query = Tweet.select(Tweet, User).join(User).where(User.username == 'huey')
    logger.info(f'query: {query}')
    for tweet in query:
        logger.info(f'tweet: {tweet.content}, user: {tweet.user.username}')
    
    # 4. user join tweet
    tweets = User.get(User.username == 'huey').tweets
    for tweet in tweets:
        logger.info(f'tweet: {tweet.content}, user: {tweet.user.username}')
    