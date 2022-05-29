# IMDB-Scraping-An-Examination-of-Factors-Affecting-Movie-Rating

All spiders can be found in IMDB-Scraping-An-Examination-of-Factors-Affecting-Movie-Rating/horror_film/horror_film/spiders/

We scraped data from IMDb, mainly focusing on the 730 top rated horror movies with more than 25000 ratings (updated on Dec 19th), available at https://www.imdb.com/search/title/?genres=horror&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=2JQFC48GYRC816ZNGW0F&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_12. 

We scraped their release years, ratings, genres, countries of origin, budgets, box office and also the reviewers’ portraits from IMDb, parse the data and form visualized figures.

7 spiders and 7 .csv files are generated accordingly:
1. HorrormovieMainpageSpider.py ----- mainpage.csv
2. RankNum.py ----- ranking.csv
3. AllRate.py ----- allrate.csv
4. age_group.py ----- agegroup.csv
5. malespider.py ----- malespider.csv
6. femalespider.py ----- femalespider.csv
7. budget.py ----- budget.csv
