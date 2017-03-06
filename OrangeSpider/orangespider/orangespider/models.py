# -*- encoding: utf-8 -*-
"""
定义数据库模型
"""
import datetime
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from settings import DATABASE


Base = declarative_base()


def db_connect():
    return create_engine(URL(**DATABASE))


def create_news_table(engine):
    Base.metadata.create_all(engine)


def _get_date():
    return datetime.datetime.now()


class ArticleRule(Base):
    """自定义文章爬取规则"""
    __tablename__ = 'article_rule'

    id = Column(Integer, primary_key=True)
    # 规则名称
    name = Column(String(30))
    # 运行的域名列表，逗号隔开
    allow_domains = Column(String(200))
    # 开始URL列表，逗号隔开
    start_urls = Column(String(200))
    # 下一页的xpath
    next_page = Column(String(200))
    # 文章链接正则表达式(子串)
    allow_url = Column(String(200))
    # 文章链接提取区域xpath
    extract_from = Column(String(200))
    # 文章标题xpath
    title_xpath = Column(String(200))
    # 文章内容xpath
    body_xpath = Column(Text)
    # 发布时间xpath
    publish_time_xpath = Column(String(50))
    # 文章来源
    source_site = Column(String(100))
    # 规则是否生效
    enable = Column(Integer)


class Article(Base):
    """文章类"""
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    url = Column(String(100))
    title = Column(String(100))
    body = Column(Text)
    publish_time = Column(String(30))
    source_site = Column(String(30))
