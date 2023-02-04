# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/tv/1421-modern-family']

    def parse(self, response):
        next_page = response.css("p.new_button a::attr(href)").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse_full_credits)
    
    def parse_full_credits(self, response):
        for cast in response.css("ol.people.credits a::attr(href)").getall():
            if "/person/" in cast:
                yield response.follow(cast, callback=self.parse_actor_page)

    def parse_actor_page(self, response):
        actor_name = response.css("h2.title a::text").get()

        for movie_name in response.css("a.tooltip bdi::text").getall():
            yield {"actor" : actor_name, "movie_or_TV_name" :movie_name}