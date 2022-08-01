# Grammy Data Collection
This repository contains python scripts to scrape `artist-level` data from artists nominated or awarded by Grammy.

As of April, 2022, we have collected `5,244` artists data stored in `grammyAwards.artists` collection. We used the artist names collected from Grammy to scrape the sidebar containing important information about the artist and the wikipedia page (See: [grammyGoogleSearch.py](https://github.com/voravich-ch/data-crawling-projects/blob/master/grammyAwards/grammyGoogleSearch/grammyGoogleSearch.py); [Sample Image](sample_image.png)).

## Directory Structure

```
        grammyAwards
        ├── README.md
        ├── sample_image.png
        ├── grammyGoogleSearch
        |   └── grammyGoogleSearch.py
        └── grammyCrawl
            ├── __init__.py
            ├── artistCrawl.py
            └── artistCrawl_deployment.py               
```

## File Description
- [artistCrawl.py](https://github.com/voravich-ch/data-crawling-projects/blob/master/grammyAwards/grammyCrawl/artistCrawl.py)  
This python script contains software that 
  1) Request payload from Grammy website via Selenium. 
  2) Extract relevant elements including artist name (`name`), number of wins (`wins`), number of nominations (`nominations`), and name of awards and nominations (`awards_and_nominations`).
  3) Write data to local storage / MongoDB.

- [artistCrawl_deployment.py](https://github.com/voravich-ch/data-crawling-projects/blob/master/grammyAwards/grammyCrawl/artistCrawl_deployment.py)  
This python script contains code deployed to collect data.

- [grammyGoogleSearch.py](https://github.com/voravich-ch/data-crawling-projects/blob/master/grammyAwards/grammyGoogleSearch/grammyGoogleSearch.py)  
This python script contains code to scrape and parse the sidebar and wikipedia page from Google.
