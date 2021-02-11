import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from helaba.items import Article


class HelSpider(scrapy.Spider):
    name = 'hel'
    start_urls = ['https://www.helaba.com/de/informationen-fuer/medien-und-oeffentlichkeit/']

    def parse(self, response):
        links = response.xpath('//div[@class="listEntryLink"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//p[@class="subline"]/text()').get()
        if date:
            date = datetime.strptime(date.strip(), '%d.%m.%Y')
            date = date.strftime('%Y/%m/%d')

        content = response.xpath('//div[@class="col col1"]/div[@class="colInner"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[2:]).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
