# -*- coding: utf-8 -*-

import logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from sqlalchemy.orm import sessionmaker
from orangespider.models import db_connect
from orangespider.models import ArticleRule
from orangespider.spiders.article_spider import ArticleSpider


if __name__ == '__main__':
    settings = get_project_settings()
    configure_logging(settings)
    db = db_connect()
    Session = sessionmaker(bind=db)
    session = Session()
    rules = session.query(ArticleRule).filter(ArticleRule.enable == 1).all()
    session.close()
    runner = CrawlerRunner(settings)

    for rule in rules:
        runner.crawl(ArticleSpider, rule=rule)
    # runner.crawl()
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    logging.info('Spider Finished!')
