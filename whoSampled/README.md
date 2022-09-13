# WhoSampled Data Collection

This repository contains python scripts to scrape information regarding sampled music from WhoSampled.

As of September 2022, we collected data from 870,602 songs.

## Directory Structure

```
        whoSampled
        ├── README.md
        ├── sitemapCrawl
        │    ├── 01_get_url.py
        │    ├── 02_get_track_url.py
        │    └── zyte-smartproxy-ca.crt
        └── whoSampledCrawl
            ├── whoSampledCrawl
            │    ├── spiders
            │    |     ├── __init__.py
            │    |     ├── first-step-whoSampled.py
            │    |     └── second-step-whoSampled.py
            │    ├── __init__.py
            │    ├── items.py
            │    ├── middlewares.py
            │    ├── pipelines.py
            │    └── settings.py
            ├── merge_whoSampled.py
            └── scrapy.cfg
                  
```

## Data Collection Process
1. Start from the [sitemapCrawl](https://github.com/simoneSantoni/music-market/tree/master/whoSampled/sitemapCrawl) folder:  
&emsp; 1.1. Run [01_get_url.py](https://github.com/simoneSantoni/music-market/blob/master/whoSampled/sitemapCrawl/01_get_url.py): This script scrapes all links (`*.xml.gz`) from WhoSampled's sitemap.  
&emsp; 1.2. Run [02_get_track_url.py](https://github.com/simoneSantoni/music-market/blob/master/whoSampled/sitemapCrawl/02_get_track_url.py): This script downloads all gunzip files concerning `tracks`, extracts the gunzip, and writes data to MongoDB.
2. Use [whoSampledCrawl](https://github.com/simoneSantoni/music-market/tree/master/whoSampled/whoSampledCrawl/whoSampledCrawl) folder which contains scrapy crawlers to scrape whoSampled data:  
&emsp; 2.1. Run spider: [first-step-whoSampled.py](https://github.com/simoneSantoni/music-market/blob/master/whoSampled/whoSampledCrawl/whoSampledCrawl/spiders/first-step-whoSampled.py) to crawl track-level pages – e.g., [Bound 2 by Kanye West](https://www.whosampled.com/Kanye-West/Bound-2/).  
&emsp; 2.2. Run spider: [second-step-whoSampled.py](https://github.com/simoneSantoni/music-market/blob/master/whoSampled/whoSampledCrawl/whoSampledCrawl/spiders/second-step-whoSampled.py) to crawl all samples and sampled data – e.g., [Sampled page](https://www.whosampled.com/Kanye-West/Bound-2/sampled/) (Notice a [track-level page](https://www.whosampled.com/Kanye-West/Bound-2/) only shows a maximum of three samples or sampled).
3. Run [merge_whoSampled.py](https://github.com/simoneSantoni/music-market/blob/master/whoSampled/whoSampledCrawl/merge_whoSampled.py) to clean, merge data from the two spiders, and insert data to MongoDB.

## Data Structure

Overall, there are data of 870,602 songs stored in `whoSampled.whoSampled` collection. The data structure is as follows:

Fields | Type | Description 
--- | --- | ---
song_name | STRING | Song's name
artists | LIST-OF-DICTIONARY | Artist names and corresponding links
artists_raw_text | STRING | Artist names accounted for whether main artist or featuring
album_name | DICTIONARY | Album name and corresponding link
release_year | INTEGER | Release year
producers | LIST-OF-DICTIONARY | Producer names and corresponding links
genre | DICTIONARY | Genre and corresponding link
tags | LIST-OF-DICTIONARY | Tags and corresponding links
n_sample | INTEGER | Number of songs sampled by the focal song
n_sampled | INTEGER | Number of songs the focal song was sampled
samples | LIST-OF-DICTIONARY | Sample info including `track_name`, `track_link`, `track_sample_link`, `main_artist_name`, `main_artist_link`, `artists`, `year`, `sample_element`, `track_genre`
sampled | LIST-OF-DICTIONARY | Sampled info including `track_name`, `track_link`, `track_sample_link`, `main_artist_name`, `main_artist_link`, `artists`, `year`, `sample_element`, `track_genre`
response_url | STRING | Scraped URL
crawl_date | DATETIME | Crawl date
spider | STRING | Spider name
