# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from orangespider.models import db_connect, create_news_table
from orangespider.models import Article, Book, BookChapter
from orangespider.items import ArticleItem, BookItem, BookChapterItem


@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class ArticlePipeline(object):
    """保存文章到数据库"""

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        pass

    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
            a = Article(url=item['url'],
                        title=item['title'].encode('utf-8'),
                        publish_time=item['publish_time'].encode('utf-8'),
                        body=item['body'].encode('utf-8'),
                        source_site=item['source_site'].encode('utf-8'))
            with session_scope(self.Session) as session:
                session.add(a)

    def close_spider(self, spider):
        pass


class BookPipeline(object):
    """保存书籍到数据库"""

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            b = Book(url=item['url'],
                     title=item['title'].encode('utf-8'),
                     intro=item['intro'].encode('utf-8'),
                     author=item['author'].encode('utf-8'))
            with session_scope(self.Session) as session:
                session.add(b)
        elif isinstance(item, BookChapterItem):
            bc = BookChapter(
                title=item['title'].encode('utf-8'),
                body=item['body'].encode('utf-8'))
            with session_scope(self.Session) as session:
                session.add(bc)
        return item
