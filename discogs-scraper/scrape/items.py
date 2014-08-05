# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class DiscogsRecord(Item):
	title = Field()
	label = Field()
	catNum = Field()
	mediaCondition = Field()
	sleeveCondition = Field()
	sellerNotes = Field()
	label = Field()
	seller = Field()
	price = Field()
	shipping = Field()

class DiscogsSeller(Item):
	name = Field()
	numItems = Field()
	country = Field()

