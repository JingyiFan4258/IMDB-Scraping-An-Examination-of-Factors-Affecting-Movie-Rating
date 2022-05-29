import scrapy


class RanknumSpider(scrapy.Spider):
    name = 'RankNum'
    allowed_domains = ['imdb.com']
    start_urls = ['http://www.imdb.com/search/title/?genres=horror&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=WTHCD67ZPQETK1RG102F&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_12/']

    def parse(self, response):
        for rank in response.css("span.lister-item-index.unbold.text-primary::text").getall():
            i = response.css("span.lister-item-index.unbold.text-primary::text").getall().index(rank)
            data = {
                "Rank":int(rank[:-1]),
                "Name":response.css("h3.lister-item-header a::text").getall()[i],
                "Year":response.css("h3.lister-item-header span.lister-item-year.text-muted.unbold::text").getall()[i][-5:-1]
                }
            yield data
        
        next_page = response.css("div.desc a.next-page::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)