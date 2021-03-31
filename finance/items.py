import scrapy


class FinanceItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
