# -*- coding: utf-8 -*-

import logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from sqlalchemy.orm import sessionmaker
from orangespider.models import db_connect
from orangespider.models import ArticleRule, BookRule
from orangespider.spiders.article_spider import ArticleSpider
from orangespider.spiders.book_spider import BookSpider


if __name__ == '__main__':
    settings = get_project_settings()
    configure_logging(settings)
    db = db_connect()
    Session = sessionmaker(bind=db)
    session = Session()
    # Load ArticleRule
    article_rules = session.query(ArticleRule).filter(
        ArticleRule.enable == 1).all()
    # Load BookRule
    book_rules = session.query(BookRule).filter(BookRule.enable == 1).all()
    session.close()
    runner = CrawlerRunner(settings)

    # init ArticleSpider
    # for article_rule in article_rules:
    #     runner.crawl(ArticleSpider, rule=article_rule)

    # init BookSpider
    for book_rule in book_rules:
        runner.crawl(BookSpider, rule=book_rule)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    logging.info('Spider Finished!')
