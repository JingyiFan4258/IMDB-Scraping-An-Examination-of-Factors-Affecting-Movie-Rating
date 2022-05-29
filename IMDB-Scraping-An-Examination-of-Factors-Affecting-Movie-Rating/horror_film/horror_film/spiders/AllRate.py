import scrapy


class AllrateSpider(scrapy.Spider):
    name = 'AllRate'
    allowed_domains = ['imdb.com']
    start_urls = ['http://www.imdb.com/search/title/?genres=horror&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=WTHCD67ZPQETK1RG102F&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_12']

    def parse(self, response):
        for movie_page_link in response.css("div.lister-item-content h3 a::attr(href)").getall():
            next_movie_page = response.urljoin(movie_page_link)
            yield scrapy.Request(next_movie_page, callback=self.jump_rating)

        next_page = response.css("div.desc a.next-page::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
    def jump_rating(self, response):
        to_join = response.css("div.RatingBarButtonBase__ContentWrap-sc-15v8ssr-0.jQXoLQ.rating-bar__base-button a::attr(href)").get()
        rating_page = response.urljoin(to_join)
        yield scrapy.Request(rating_page, callback=self.parse_rating)
  
    def parse_rating(self, response):
        vote10, vote9, vote8, vote7, vote6, vote5, vote4, vote3, vote2, vote1 = response.css("div.leftAligned::text").getall()[1:11]
        yield {
            "Name" : response.css("div.parent h3 a::text").get(),
            "Year" : response.css("div.parent h3 span.nobr::text").get()[-19:-15],
            "Rating" : float(response.css("div.ipl-rating-star span.ipl-rating-star__rating::text").get()),
            "User_Type" : "IMDb Users",
            "vote10" : int(vote10.replace(",", "")),
            "vote9" : int(vote9.replace(",", "")),
            "vote8" : int(vote8.replace(",", "")),
            "vote7" : int(vote7.replace(",", "")),
            "vote6" : int(vote6.replace(",", "")),
            "vote5" : int(vote5.replace(",", "")),
            "vote4" : int(vote4.replace(",", "")),
            "vote3" : int(vote3.replace(",", "")),
            "vote2" : int(vote2.replace(",", "")),
            "vote1" : int(vote1.replace(",", "")),
        }
