# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from orangespider.models import db_connect, create_news_table, Article


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


class ArticleDataBasePipeline(object):
    """保存文章到数据库"""

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        pass

    def process_item(self, item, spider):
        a = Article(url=item["url"],
                    title=item["title"].encode("utf-8"),
                    publish_time=item["publish_time"].encode("utf-8"),
                    body=item["body"].encode("utf-8"),
                    source_site=item["source_site"].encode("utf-8"))
        with session_scope(self.Session) as session:
            session.add(a)

    def close_spider(self, spider):
        pass


class BookPipeline(object):

    collection_book = 'crawl.book'

    collection_book_chapter = 'crawl.book_chapter'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'crawl')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        book = item.get('book', None)
        chapter = item.get('chapter', None)
        _book = self.db[self.collection_book].find_one(dict(book))
        if _book:
            if not self.db[self.collection_book_chapter].find_one({'headline': chapter['headline']}):
                chapter['book_id'] = _book['_id']
                _chapter_id = self.db[self.collection_book_chapter].insert(
                    dict(chapter))
                self.db[self.collection_book].update(_book, {'$push': {'chapters':
                                                                       {'chapter_id': _chapter_id,
                                                                           'headline': chapter['headline']}
                                                                       }})
        else:
            self.db[self.collection_book].insert(dict(book))
        return item
