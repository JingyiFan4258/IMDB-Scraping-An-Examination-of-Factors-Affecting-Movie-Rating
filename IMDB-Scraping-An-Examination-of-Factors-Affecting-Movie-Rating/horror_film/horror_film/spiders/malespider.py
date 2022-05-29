import scrapy


class MalespiderSpider(scrapy.Spider):
    name = 'malespider'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=horror&sort=user_rating,desc&ref_=adv_prv']

    def parse(self, response):
        for movie_page_link in response.css("div.lister-item-content h3 a::attr(href)"):
            next_page1 = response.urljoin(movie_page_link.get())
            yield scrapy.Request(next_page1, callback=self.movie_parse)

        next_page = response.css("div.desc a.next-page::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def movie_parse(self, response):
        for rating_link in response.css("div.RatingBarButtonBase__ContentWrap-sc-15v8ssr-0.jQXoLQ.rating-bar__base-button a::attr(href)"):
            next_page2 = response.urljoin(rating_link.get())
            yield scrapy.Request(next_page2, callback=self.rating_parse)

    def rating_parse(self,response):
        next_page_male= response.urljoin(response.css('div.smallcell a::attr(href)').getall()[5])
        yield scrapy.Request(next_page_male, callback=self.gender_parse)

    def gender_parse(self,response):
        vote10m, vote9m, vote8m, vote7m, vote6m, vote5m, vote4m, vote3m, vote2m, vote1m = response.css("div.leftAligned::text").getall()[1:11]
        rate_male = response.css("table div.bigcell::text").getall()[5]
        rate_1m = response.css("table div.bigcell::text").getall()[6]
        rate_2m = response.css("table div.bigcell::text").getall()[7]
        rate_3m = response.css("table div.bigcell::text").getall()[8]
        rate_4m = response.css("table div.bigcell::text").getall()[9]
        number_male = response.css("table div.smallcell a::text").getall()[5][21:-17]
        number_1m = response.css("table div.smallcell a::text").getall()[6][21:-17]
        number_2m = response.css("table div.smallcell a::text").getall()[7][21:-17]
        number_3m = response.css("table div.smallcell a::text").getall()[8][21:-17]
        number_4m = response.css("table div.smallcell a::text").getall()[9][21:-17]
        yield {
            "Name" : response.css("div.parent h3 a::text").get(),
            "Year" : response.css("div.parent h3 span.nobr::text").get()[-19:-15],
            "User_Type": response.url.split("/")[-1][-5:],
            "Rating" : float(response.css("div.allText::text").getall()[2][-24:-21]),
            "vote10m" : int(vote10m.replace(',','')),
            "vote9m" : int(vote9m.replace(',','')),
            "vote8m" : int(vote8m.replace(',','')),
            "vote7m" : int(vote7m.replace(',','')),
            "vote6m" : int(vote6m.replace(',','')),
            "vote5m" : int(vote5m.replace(',','')),
            "vote4m" : int(vote4m.replace(',','')),
            "vote3m" : int(vote3m.replace(',','')),
            "vote2m" : int(vote2m.replace(',','')),
            "vote1m" : int(vote1m.replace(',','')),
            "Rate_Male" : float(rate_male),
            "Rate_<18m" : float(rate_1m),
            "Rate_18-29m" : float(rate_2m),
            "Rate_30-44m" : float(rate_3m),
            "Rate_45+m" : float(rate_4m),
            "Number_Male" : int(number_male.replace(',','')),
            "Number_<18m" : int(number_1m.replace(',','')),
            "Number_18-29m" : int(number_2m.replace(',','')),
            "Number_30-44m" : int(number_3m.replace(',','')),
            "Number_45+m" : int(number_4m.replace(',',''))
        }