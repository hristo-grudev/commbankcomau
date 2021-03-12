import scrapy

from scrapy.loader import ItemLoader

from ..items import CommbankcomauItem
from itemloaders.processors import TakeFirst


class CommbankcomauSpider(scrapy.Spider):
	name = 'commbankcomau'
	start_urls = ['https://www.commbank.com.au/newsroom.html?ei=CB-footer_newsroom']

	def parse(self, response):
		post_links = response.xpath('//h4/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="banner-content no-offer"]/h1/text()').get()
		description = response.xpath('//div[@class="article-text text"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="banner-content no-offer"]/p/text()').get()

		item = ItemLoader(item=CommbankcomauItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
