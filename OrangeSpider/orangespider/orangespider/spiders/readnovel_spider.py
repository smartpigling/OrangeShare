# -*- coding: utf-8 -*-

#scrapy runspider readnovel_spider.py -o readnovel.json
from orangespider.items import BookItem, BookChapterItem
import scrapy

class ReadNovelSpider(scrapy.Spider):
    '''
        小说阅读网
    '''
    name = 'readnovel'
    start_urls = [
        'https://www.readnovel.com/',
    ]

    url_match = lambda self, url : url.startswith('//') and 'https:%s' % url or url

    def parse(self, response):
        for item in response.css('div.book-rank-list > ul > li'):
            book = BookItem()
            book['title'] = item.css('a::text').extract_first()
            book['link'] = self.url_match(item.css('a::attr(href)').extract_first())
            yield scrapy.Request(book['link'], callback=self.parse_transition, meta={'book': book})

    def parse_transition(self, response):
        read_url = self.url_match(response.css('a.pink-btn.J-getJumpUrl::attr(href)').extract_first())
        return scrapy.Request(read_url, callback=self.parse_book, meta=response.meta)

    def parse_book(self, response):
        book = response.meta['book']
        for item in response.css('div.main-text-wrap'):
            chapter = BookChapterItem()
            chapter['headline'] = item.css('h3.j_chapterName::text').extract_first()
            chapter['content'] = item.css('div.read-content.j_readContent').extract_first()
            yield {'book': book, 'chapter': chapter}

        next_page = response.css('div.chapter-control.dib-wrap > a[id*=j_chapterNext]::attr(href)').extract_first()
        if next_page is not None:
            next_page = self.url_match(response.urljoin(next_page))
            yield scrapy.Request(next_page, callback=self.parse_book, meta=response.meta)
