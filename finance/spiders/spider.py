import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import FinanceItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class FinanceSpider(scrapy.Spider):
	name = 'finance'
	start_urls = ['https://www.financefactors.com/news-articles']

	def parse(self, response):
		post_links = response.xpath('//h3/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//h3[@class="subheading"]/text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('(//div[@class="container content-block"])[1]//text()[not (ancestor::div[@class="section-heading"] or ancestor::figure)]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=FinanceItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
