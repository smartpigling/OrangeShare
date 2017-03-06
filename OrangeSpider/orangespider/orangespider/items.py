# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    publish_time = scrapy.Field()
    source_site = scrapy.Field()


class BookItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    link = scrapy.Field()  # 链接
    intro = scrapy.Field()  # 简介
    author = scrapy.Field()  # 作者
    originate = scrapy.Field()  # 来源
    created_time = scrapy.Field()  # 创建时间
    category = scrapy.Field()  # 分类


class BookChapterItem(scrapy.Item):
    book_id = scrapy.Field()
    headline = scrapy.Field()  # 章节标题
    content = scrapy.Field()  # 章节内容
    updated_time = scrapy.Field()  # 更新时间
