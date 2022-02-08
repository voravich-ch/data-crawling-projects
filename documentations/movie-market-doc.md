# Table of Contents

- [IMDb](#imdb)
  - [IMDb Data](#imdb-data)
  - [Sample Data](#imdb-sample-data)
  - [Movie Information](#imdb-movie-information)
  - [Critic Url](#imdb-critic-url)
  - [Critic Content](#imdb-critic-content)
  - [User Review](#imdb-user-review)
  - [Director & Cast](#imdb-director--cast)
  - [Metacritic Url](#imdb-metacritic-url)
- [Metacritic](#metacritic)
  - [Movie Url](#metacritic-movie-url)
  - [Movie Information](#metacritic-movie-information)
  - [User Score](#metacritic-user-score)
  - [User Review](#metacritic-user-review)
  - [Critic Score](#metacritic-critic-score)
  - [Critic Review](#metacritic-critic-review)
  - [Critic Review Content](#metacritic-critic-review-content)
- [Rotten Tomatoes](#rotten-tomatoes)
  - [Movie Url](#rotten-tomatoes-movie-url)
  - [Movie Information](#rotten-tomatoes-movie-information)
  - [Critic Review](#rotten-tomatoes-critic-review)
  - [Critic Review Content](#rotten-tomatoes-critic-review-content)


## IMDb

### IMDb Data

Directory location: `imdb/data/imdb_dump`

For IMDb data documentation, please see [Documentation](https://www.imdb.com/interfaces/).

### IMDb Sample Data

File location: `imdb/data/sample.json`

Fields | Type | Description 
--- | --- | ---
tconst | STRING | `Primary Key`: Alphanumeric unique identifier of the title
title | STRING | Movie title
genres | STRING | Movie genres (Comma-separated string)

### IMDb Movie Information

File location: `imdb/data/imdb_movie_info.jl`

Fields | Type | Description 
--- | --- | ---
imdb_tconst | STRING | `Foreign Key`: Alphanumeric unique identifier of the title
imdb_rating | FLOAT | Average movie rating
imdb_n_rating | INTEGER | Total number of ratings
imdb_movie_desc | STRING | Movie short description
imdb_user_n_review | INTEGER | Total number of user reviews
imdb_cr_n_review | INTEGER | Total number of critic reviews
imdb_budget | INTEGER | Production budget (in USD)
imdb_gross_us | INTEGER | Total box office gross in the US (in USD)
imdb_release_date | STRING | Release date (e.g., "12 October 1907 (USA)")
url | STRING | Scraped URL
date | DATETIME  | Crawl date
spider | STRING | Spider name

### IMDb Critic Url

File location: `imdb/data/imdb_critic_url.jl`

Fields | Type | Description 
--- | --- | ---
imdb_tconst | STRING | `Foreign Key`: Alphanumeric unique identifier of the title
imdb_cr_url | STRING | `Primary Key`: URL directed the to critic review
imdb_cr | STRING | Critic name
url | STRING | Scraped URL
date | DATETIME | Crawl date
spider | STRING | Spider name

### IMDb Critic Content

File location: `imdb/data/imdb_critic_content.jl`

Fields | Type | Description 
--- | --- | ---
imdb_cr_review | STRING | Critic review content
url | STRING | `Foreign Key`: Scraped URL
date | DATETIME | Crawl date
spider | STRING | Spider name

### IMDb User Review

File location: `imdb/data/imdb_user_review.jl`

Fields | Type | Description 
--- | --- | ---
imdb_tconst | STRING | `Foreign Key`: Alphanumeric unique identifier of the title
imdb_user | STRING | Reviewer username
imdb_user_review_topic | STRING | Review topic
imdb_user_review | STRING | Review content
imdb_user_review_date | STRING | Review date
imdb_user_rating | INTEGER | Rating given by a user
imdb_n_helpful_vote | INTEGER | Number of helpful votes received
imdb_t_vote | INTEGER | Total number of votes received
url | STRING | Scraped URL
date | DATETIME | Crawl date
spider | STRING | Spider name

### IMDb Director & Cast

File location: `imdb/data/imdb_director_cast.jl`

Fields | Type | Description
--- | --- | ---
imdb_tconst | STRING | `Foreign Key`: Alphanumeric unique identifier of the title
imdb_director | LIST | Director(s) involved in the movie
imdb_cast | LIST | Cast(s) involved in the movie
url | STRING | Scraped URL
date | DATETIME | Crawl date
spider | STRING | Spider name

### IMDb Metacritic URL

File location: `imdb/data/imdb_mt_url.jl`

Fields | Type | Description
--- | --- | ---
imdb_tconst | STRING | `Foreign Key`: Alphanumeric unique identifier of the title
imdb_mt_url | STRING | Url link to a movie page in metacritic
url | STRING | Scraped URL
date | DATETIME | Crawl date
spider | STRING | Spider name

## Metacritic

### Metacritic Movie URL
File location: `metacritic/data/mt_movie_url.jl`

Fields | Type | Description 
--- | --- | ---
mt_tconst | STRING | `Primary Key`: URL extension which specifies a movie
mt_url | STRING | URL to the movie page
url | STRING | Scraped URL
date | DATETIME | Crawl date
spider | STRING | Spider name

### Metacritic Movie Information
File location: `metacritic/data/mt_movie_info.jl`

Fields | Type | Description 
--- | --- | ---
mt_tconst | STRING | `Foreign Key`: URL extension which specifies a movie
mt_movie_name | STRING | Movie name
mt_genre | LIST | Genre(s)
mt_movie_desc | STRING | Movie brief description
mt_distributor | STRING | Movie distributor name
mt_release_date | STRING | Movie release date (e.g., "March 11, 1972")
mt_user_n_review | INTEGER | Number of user reviews
mt_cr_n_review | INTEGER | Number of critic reviews
url | STRING | Scraped URL
date | DATETIME | Crawl date
spider | STRING | Spider name

### Metacritic User Score
File location: `metacritic/data/mt_user_score.jl`

Fields | Type | Description 
--- | --- | ---
mt_tconst | STRING | `Foreign Key`: URL extension which specifies a movie
mt_user_score | STRING | Movie average score by users [0-10] (Supposed to be FLOAT)
mt_user_n_score | INTEGER | Number of users giving score
mt_user_n_pos | INTEGER | Number of users giving positive score [7-10]
mt_user_n_neg | INTEGER | Number of users giving negative score [0-3]
mt_user_n_mixed | INTEGER | Number of users giving mixed score [4-6]
url | STRING | Scraped URL
date | DATETIME | Crawl date
spider | STRING | Spider name

### Metacritic User Review
File location: `metacritic/data/mt_user_review.jl`

Fields | Type | Description 
--- | --- | ---
mt_tconst | STRING | `Foreign Key`: URL extension which specifies a movie
mt_user | STRING | Reviewer username
mt_user_review_score | INTEGER | Review score [0-10]
mt_user_review_date | STRING | Review date (e.g., "March 11, 1972")
mt_user_review | STRING | Review content
url | STRING | Scraped URL
date | DATETIME | Crawl date
spider | STRING | Spider name

### Metacritic Critic Score
File location: `metacritic/data/mt_cr_score.jl`

Fields | Type | Description 
--- | --- | ---
mt_tconst | STRING | `Foreign Key`: URL extension which specifies a movie
mt_cr_score | INTEGER | Movie average score by critics [0-100]
mt_cr_n_score | INTEGER | Number of critics giving score
mt_cr_n_pos | INTEGER | Number of critics giving positive score [60-100]
mt_cr_n_neg | INTEGER | Number of critics giving negative score [0-39]
mt_cr_n_mixed | INTEGER | Number of critics giving mixed score [40-59]
url | STRING | Scraped URL
date | DATETIME | Crawl date
spider | STRING | Spider name

### Metacritic Critic Review
File location: `metacritic/data/mt_cr_review.jl`

Fields | Type | Description 
--- | --- | ---
mt_tconst | STRING | `Foreign Key`: URL extension which specifies a movie
mt_cr | LIST | Critic name(s)
mt_cr_review_score | INTEGER | Review score [0-100]
mt_cr_review | STRING | Review summary
mt_cr_review_full_url | STRING | URL to the original review website
mt_cr_review_date | STRING | Review date (e.g., "March 11, 1972")
url | STRING | Scraped URL
date | DATETIME | Crawl date
spider | STRING | Spider name

### Metacritic Critic Review Content
File location: `metacritic/data/mt_cr_review_content.jl`

- IN PROGRESS

## Rotten Tomatoes

### Rotten Tomatoes Movie URL
File location: `rottenTomatoes/data/rt_movie_url.jl`

Fields | Type | Description 
--- | --- | ---
rt_tconst | STRING | `Primary Key`: URL extension which specifies a movie
rt_url | STRING | URL to the movie page
url | STRING | Scraped URL
date | DATETIME | Crawl date
spider | STRING | Spider name

### Rotten Tomatoes Movie Information
File location: `rottenTomatoes/data/rt_movie_info.jl`

Fields | Type | Description 
--- | --- | ---
rt_tconst | STRING | `Foreign Key`: URL extension which specifies a movie
rt_title | STRING | Movie title
rt_user_rating | INTEGER | Average movie rating by users
rt_cr_rating | INTEGER | Average movie rating by critics
rt_movie_desc | STRING | Movie short description
rt_genre | LIST | Genre(s)
rt_director | LIST | Director(s) involved in the movie
rt_producer | LIST | Producer(s) involved in the movie
rt_writer | LIST | Writer(s) involved in the movie
rt_release_date_th | STRING | Release date: Theaters (e.g., "Mar 11, 1972")
rt_release_date_st | STRING | Release date: Streaming (e.g., "Mar 11, 1972")
rt_gross_us | STRING | Total gross in the US (e.g., "$57.9M")
rt_production | LIST | Production name(s)
url | STRING | Scraped URL
date | DATETIME | Crawl date
spider | STRING | Spider name

### Rotten Tomatoes Critic Review
File location: `rottenTomatoes/data/rt_cr_review.jl`

Fields | Type | Description 
--- | --- | ---
rt_tconst | STRING | `Foreign Key`: URL extension which specifies a movie
rt_cr | STRING | Critic name
rt_pub | STRING | Publication name
rt_fresh | BIT | Fresh: 1; Rotten: Null
rt_top | BIT | Top Critic: 1; Critic: Null
rt_cr_review | STRING | Review summary
rt_cr_review_full_url | STRING | 	URL to the original review website
rt_cr_review_date | STRING | Review date (e.g., "March 11, 1972")
url | STRING | Scraped URL
date | DATETIME | Crawl date
spider | STRING | Spider name

### Rotten Tomatoes Critic Review Content
File location: `rottenTomatoes/data/rt_cr_review_content.jl`

- IN PROGRESS
