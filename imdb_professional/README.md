**IMDB Professional Project**

The python scripts in this repository scrape information from IMDb with regards to the roles a professional played and awards a professional received. 
The data scraping tools used in this project include Scrapy and Selenium. Scrapy was used to collect award information and Selenium was used to collect role information.   

**Database structuring**:
  - Create a new database: `imdbProfessional `
  - Create 3 new collections:
      - `imdb_cast_id`: A temporary collection to store cast ids from the movie title pages (could be removed after finished the project)
      - `imdb_role`: Containing the following data
          - cast_id (string) - nm1500155
          - cast_name (string) - Robert Pattinson
          - movie_id (string) - tt1877830
          - movie_name (string) - The Batman
          - movie_year (string) - 2020
          - roles (list) - [Bruce Wayne, The Batman]
      - `imdb_award`: Containing the following data
          - cast_id (string) - nm1500155
          - cast_name (string) - Robert Pattinson
          - awarding_entity (string) - ACCEC Awards
          - award_year (string) - 2022
          - award_url (string) - https://www.imdb.com/event/ev0001511/2022/1
          - award_outcome (string) - Winner
          - award_category (string) - ACCEC Award
          - award_title (string) - Favorite Movie
          - movie_detail (list) - [{“movie_id”: “tt1877830”, 
                                    “movie_name”: “The Batman”,
                                    “movie_year”: “2020”}]
                                    
