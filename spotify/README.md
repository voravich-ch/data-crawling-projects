# Spotify Data Collection
This repository contains python scripts to scrape `artist-level`, `album-level`, `track-level`, and `acoustic-attribute` data via [SpotifyAPI](https://developer.spotify.com/documentation/web-api/).

As of 2022, we have collected:
- `2,139,061` Artists – Stored in `spotify.artists` collection.
- `11,876,566` Albums – Stored in `spotify.albums` collection.
- `TBC` Tracks – Stored in `spotify.tracks` collection.

## Directory Structure

```
        dataCollection
        ├── README.md
        ├── accumulateSpotifyID.py
        └── spotifyCrawl
            ├── aboutArtist
            │     ├── __init__.py
            │     ├── aboutCrawl.py
            │     └── aboutCrawl_deployment.py
            ├── googleSearch
            │     └── artistSearchFromMusicBrainz.py
            └── spotifyCrawl
                  ├── __init__.py
                  ├── spotifyCrawl.py
                  └── spotifyCrawl_deployment.py
                  
```

## Framework
<ul>
        <h4> 1. Collect Spotify artist IDs from multiple sources</h4>
                <ul>
                        <li> 1.1. Get Spotify artists IDs from Musicbrainz database (See: 
                                <a href="https://musicbrainz.org/doc/MusicBrainz_Database">MusicBrainz Database</a>; 
                                <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/accumulateSpotifyID.py#L20">Extract Spotify artists IDs</a>)
                        </li>
                        <li> 1.2. For artists without Spotify IDs, we find their IDs by searching their names on GoogleSearch (See:
                                <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/googleSearch/artistSearchFromMusicBrainz.py">GoogleSearch (MusicBrainz)</a>;
                                <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/accumulateSpotifyID.py.py#L36">Extract Spotify artists IDs</a>) 
                        </li>
                        <li> 1.3. Get Spotify artists IDs by searching the name of Grammy winners and nominees on GoogleSearch (See:
                                <a href="https://github.com/voravich-ch/data-crawling-projects/tree/master/grammyAwards/grammyCrawl">Grammy Crawler</a>;
                                <a href="https://github.com/voravich-ch/data-crawling-projects/tree/master/grammyAwards/grammyGoogleSearch">GoogleSearch (Grammy)</a>;
                                <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/accumulateSpotifyID.py.py#L54">Extract Spotify artists IDs</a>)
                        </li>
                        <li> 1.4. Get Spotify artists IDs from related artists section in the SpotifyAbout page of Grammy winners and nominees (See:
                                <a href="https://github.com/voravich-ch/data-crawling-projects/tree/master/spotify/aboutArtist">Spotify AboutPage Crawler</a>;
                                <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/accumulateSpotifyID.py#L73">Extract Spotify artists IDs</a>)
                        </li>
                        <li> 1.5. Get Spotify artists IDs from the track IDs collected from Musixmatch (See:
                                <a href="https://github.com/voravich-ch/data-crawling-projects/tree/master/musixmatch/musixmatchCrawl">Musixmatch Crawler</a>;
                                <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/accumulateSpotifyID.py#L90">Extract Spotify artists IDs</a>)
                        </li>
                </ul>
        <h4> 2. Collect artist-level data using Spotify artist IDs </h4> 
                <ul><li> (See: 
                        <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/spotifyCrawl/spotifyCrawl_deployment.py#L25">Deployment code</a>;
                        <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/spotifyCrawl/spotifyCrawl.py#L17">SpotifyScraper</a>)
                </li></ul>
        <h4> 3. Collect album data using Spotify artist IDs </h4>
                <ul><li> (See: 
                        <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/spotifyCrawl/spotifyCrawl_deployment.py#L34">Deployment code</a>;
                        <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/spotifyCrawl/spotifyCrawl.py#L23">SpotifyScraper</a>)
                </li></ul>
        <h4> 4. Collect track data using Spotify album IDs </h4>
                <ul><li> (See: 
                        <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/spotifyCrawl/spotifyCrawl_deployment.py#L41">Deployment code</a>;
                        <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/spotifyCrawl/spotifyCrawl.py#L29">SpotifyScraper</a>)
                </li></ul>
        <h4> 5. Collect acoustic attribute using Spotify track IDs </h4>
                <ul><li> (See: 
                        <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/spotifyCrawl/spotifyCrawl_deployment.py#L50">Deployment code</a>;
                        <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/spotifyCrawl/spotifyCrawl.py#L35">SpotifyScraper</a>)
                </li></ul>
</ul>
