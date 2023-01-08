import scrapy
from sreality_5.items import SrealityItem

# too many urls. Defaultly, if Playwright library runs for >30s it shuts down and prints
# TimeoutError: Timeout 30000ms exceeded.
# I had to rewrite its source code in
# "/opt/anaconda3/envs/scrapy-env/lib/python3.11/site-packages/playwright/async_api/_generated.py", line 8913,
# and change it from 'timeout=timeout' to 'timeout=0 so that it can run many sreality urls.
        
# Apparently, this can be also changed using: "browser_context.set_default_navigation_timeout()" as stated in the file referenced above.

### URLS LIST SOLUTION
##################
class FlatSpider(scrapy.Spider):
    name = "flat_spider"

    def start_requests(self):
        urls = []
        for i in range(1,2):
            urls.append("https://www.sreality.cz/en/search/for-sale/apartments?page=" + str(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={"playwright": True})

    def parse(self, response):
        properties = response.css('div.property.ng-scope')

        flat_item = SrealityItem()

        for flat in properties:
            name = flat.css('span.name.ng-binding::text').get()
            location = flat.css('span.locality.ng-binding::text').get()
            img_url = flat.css('img').attrib['src']

            print("PRINTING APARTMENT NAME, ADDRESS AND IMAGE URL")
            print(name)
            print(location)
            print(img_url)

            flat_item["name"] = name
            flat_item["location"] = location
            flat_item["img_url"] = img_url
            yield flat_item


# ### FOLLOW SOLUTION
# # ####################
# from scrapy_playwright.page import PageMethod

# class FlatSpider(scrapy.Spider):
#     name = "flat_spider"

#     # nicely written start_requests
#     def start_requests(self):
#         url = 'https://www.sreality.cz/en/search/for-sale/apartments'

#         # yield scrapy.Request(url=url, callback=self.parse,
#         # meta={  "playwright": True,
#         #         "playwright_include_page": True,
#         #         "playwright_page_methods": [PageMethod('wait_for_selector', 'a.btn-paging-pn.icof.icon-arr-right.paging-next')],
#         #         "errback": self.errback,
#         #         "properties_count": 0,
#         #         "parse_count": 0})

#         yield scrapy.Request(url=url, callback=self.parse,
#         meta={  "playwright": True,
#                     "properties_count": 0,
#                     "parse_count": 0
#                  })


#     def parse(self, response):
#         parse_count = response.meta["parse_count"]
#         parse_count += 1
#         print("ENTERING PARSE N." + str(parse_count))
#         properties = response.css('div.property.ng-scope')
#         properties_count = response.meta["properties_count"]

#         for flat in properties:
#             title = flat.css('span.name.ng-binding::text').get()
#             img_url = flat.css('img').attrib['src']

#             properties_count += 1
#             yield {title: img_url}

#         next_page = response.css('a.btn-paging-pn.icof.icon-arr-right.paging-next').attrib['href']
#         if (properties_count < 100) and (next_page is not None):

#             yield response.follow(url=next_page, callback=self.parse,
#             meta={  "playwright": True,
#                     "properties_count": properties_count,
#                     "parse_count": parse_count
#                  })
            
#             # yield response.follow(url=next_page, callback=self.parse,
#             # meta={  "playwright": True,
#             #         "playwright_include_page": True,
#             #         "playwright_page_methods": [PageMethod('wait_for_selector', 'a.btn-paging-pn.icof.icon-arr-right.paging-next')],
#             #         "errback": self.errback,
#             #         "properties_count": properties_count,
#             #         "parse_count": parse_count})

#         print("LEAVING PARSE N." + str(parse_count))        # I don't understad why this is not all printed out in the end when all the recursions surface out

    # async def errback(self, failure):
    #     page = failure.request.meta["playwright_page"]
    #     await page.close()