# -*- encoding: utf-8 -*-
"""
Topic: 书籍爬取
Desc :
"""
import logging
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from orangespider.utils import filter_tags, parse_text
from orangespider.items import BookItem, BookChapterItem


class BookSpider(CrawlSpider):
    name = 'book'

    custom_settings = {
        'ITEM_PIPELINES': {'orangespider.pipelines.BookPipeline': 5}
    }

    def __init__(self, rule):
        self.rule = rule
        self.name = rule.name
        self.allowed_domains = rule.allow_domains.split(',')
        self.start_urls = rule.start_urls.split(',')
        rule_list = []
        # # 添加`下一章`的规则
        # if rule.next_page:
        #     rule_list.append(Rule(LinkExtractor(
        #         allow=(),
        #         restrict_xpaths=[rule.next_page]),
        #         callback=self.parse_chapter, follow=True))
        # 添加抽取书籍链接的规则
        rule_list.append(Rule(LinkExtractor(
            allow=[rule.allow_book_url],
            restrict_xpaths=[rule.extract_book_from]),
            callback=self.parse_book, follow=True))

        # # 添加抽取章节链接的规则
        # rule_list.append(Rule(LinkExtractor(
        #     allow=[rule.allow_chapter_url],
        #     restrict_xpaths=[rule.extract_chapter_from]),
        #     callback=self.parse_chapter, follow=True))

        self.rules = tuple(rule_list)
        super(BookSpider, self).__init__()

    def parse_book(self, response):
        self.log('Hi, this is an book page! %s' % response.url)
        book = BookItem()
        book['url'] = response.url
        book['title'] = response.xpath(
            self.rule.book_title_xpath).extract_first()
        book['intro'] = response.xpath(
            self.rule.book_intro_xpath).extract_first()
        book['author'] = response.xpath(
            self.rule.book_author_xpath).extract_first()
        book['category'] = response.xpath(
            self.rule.book_category_xpath).extract_first()
        book['source_site'] = self.rule.source_site

        _links = LinkExtractor(allow=(self.rule.allow_chapter_url,), restrict_xpaths=(
            self.rule.extract_chapter_from,)).extract_links(response)

        return Request(_links[0].url, callback=self.parse_chapter, meta={'book': book})

    def url_match(self, url): return url.startswith(
        '//') and 'https:%s' % url or url

    def parse_chapter(self, response):
        self.log('Hi, this is an chapter page! %s' % response.url)
        book = response.meta['book']

        chapter = BookChapterItem()
        chapter['url'] = response.url
        chapter['title'] = response.xpath(
            self.rule.chapter_title_xpath).extract_first()
        chapter['body'] = response.xpath(
            self.rule.chapter_body_xpath).extract_first()
        chapter['publish_time'] = response.xpath(
            self.rule.publish_time_xpath).extract_first()
        yield chapter

        next_page = response.css(
            'div.chapter-control.dib-wrap > a[id*=j_chapterNext]::attr(href)').extract_first()
        if next_page is not None:
            next_page = self.url_match(response.urljoin(next_page))
            yield Request(next_page, callback=self.parse_chapter, meta=response.meta)
