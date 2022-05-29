import scrapy


class FemalespiderSpider(scrapy.Spider):
    name = 'femalespider'
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
        next_page_female= response.urljoin(response.css('div.smallcell a::attr(href)').getall()[10])
        yield scrapy.Request(next_page_female, callback=self.gender_parse)

    def gender_parse(self,response):
        vote10f, vote9f, vote8f, vote7f, vote6f, vote5f, vote4f, vote3f, vote2f, vote1f = response.css("div.leftAligned::text").getall()[1:11]
        rate_female = response.css("table div.bigcell::text").getall()[10]
        rate_1f = response.css("table div.bigcell::text").getall()[11]
        rate_2f = response.css("table div.bigcell::text").getall()[12]
        rate_3f = response.css("table div.bigcell::text").getall()[13]
        rate_4f = response.css("table div.bigcell::text").getall()[14]
        number_female = response.css("table div.smallcell a::text").getall()[10][21:-17]
        number_1f = response.css("table div.smallcell a::text").getall()[11][21:-17]
        number_2f = response.css("table div.smallcell a::text").getall()[12][21:-17]
        number_3f = response.css("table div.smallcell a::text").getall()[13][21:-17]
        number_4f = response.css("table div.smallcell a::text").getall()[14][21:-17]
        yield {
            "Name" : response.css("div.parent h3 a::text").get(),
            "Year" : response.css("div.parent h3 span.nobr::text").get()[-19:-15],
            "User_Type": response.url.split("/")[-1][-7:],
            "Rating" : float(response.css("div.allText::text").getall()[2][-24:-21]),
            "vote10f" : int(vote10f.replace(',','')),
            "vote9f" : int(vote9f.replace(',','')),
            "vote8f" : int(vote8f.replace(',','')),
            "vote7f" : int(vote7f.replace(',','')),
            "vote6f" : int(vote6f.replace(',','')),
            "vote5f" : int(vote5f.replace(',','')),
            "vote4f" : int(vote4f.replace(',','')),
            "vote3f" : int(vote3f.replace(',','')),
            "vote2f" : int(vote2f.replace(',','')),
            "vote1f" : int(vote1f.replace(',','')),
            "Rate_Female" : float(rate_female),
            "Rate_<18f" : float(rate_1f),
            "Rate_18-29f" : float(rate_2f),
            "Rate_30-44f" : float(rate_3f),
            "Rate_45+f" : float(rate_4f),
            "Number_Female" : int(number_female.replace(',','')),
            "Number_<18f" : int(number_1f.replace(',','')),
            "Number_18-29f" : int(number_2f.replace(',','')),
            "Number_30-44f" : int(number_3f.replace(',','')),
            "Number_45+f" : int(number_4f.replace(',',''))
        }