# Spotify Data Collection
This repository contains python scripts to scrape `artist-level`, `album-level`, `track-level`, and `acoustic-attribute` data via [SpotifyAPI](https://developer.spotify.com/documentation/web-api/).

As of 2022, we have collected:
- `2,139,061` Artists – Stored in `spotify.artists` collection.
- `11,876,566` Albums – Stored in `spotify.albums` collection.
- `75,926,513` Tracks – Stored in `spotify.tracks` collection.
- `66,243,012` AcousticAttributes – Stored in `spotify.acousticAttributes` collection.

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
                                <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/accumulateSpotifyID.py#L36">Extract Spotify artists IDs</a>) 
                        </li>
                        <li> 1.3. Get Spotify artists IDs by searching the name of Grammy winners and nominees on GoogleSearch (See:
                                <a href="https://github.com/voravich-ch/data-crawling-projects/tree/master/grammyAwards/grammyCrawl">Grammy Crawler</a>;
                                <a href="https://github.com/voravich-ch/data-crawling-projects/tree/master/grammyAwards/grammyGoogleSearch">GoogleSearch (Grammy)</a>;
                                <a href="https://github.com/voravich-ch/data-crawling-projects/blob/master/spotify/accumulateSpotifyID.py#L54">Extract Spotify artists IDs</a>)
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

## Data Structure

### spotify.artists
Official documentation on schema: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-artist
Fields | Type | Further Detail 
--- | --- | ---
external_urls | DICTIONARY | Key: `spotify` – e.g. "https://open.spotify.com/artist/21GGkCJG1qIYnAe8rNUgvu"
followers | DICTIONARY | Keys: `href`, `total`
genres | LIST | List of genres
href | STRING | e.g. "https://api.spotify.com/v1/artists/21GGkCJG1qIYnAe8rNUgvu"
id | STRING | Artist ID – **`UNIQUE KEY to link with spotify.albums`**
images | LIST-OF-DICTIONARY | Keys: `url`, `height`, `width`
name | STRING | Artist name
popularity | Integer | Between 0 - 100
type | STRING | Only one value: "artist"
uri | STRING | Spotify URI

### spotify.albums
Official documentation on schema: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-album
Fields | Type | Further Detail 
--- | --- | ---
album_group | STRING | e.g. "https://open.spotify.com/artist/21GGkCJG1qIYnAe8rNUgvu"
album_type | STRING | Allowed values: "album", "single", "compilation"
artists | LIST-OF-DICTIONARY | Keys: `external_urls`, `href`, `id`, `name`, `type`, `uri` <br />**`Use key: "id" to link with spotify.artists`**
available_markets | LIST | List of two-letter country codes
external_urls | DICTIONARY | Key: `spotify` – e.g. "https://open.spotify.com/album/236dCo6AgE7pccxVFBA2GK"
href | STRING | e.g., "https://api.spotify.com/v1/albums/236dCo6AgE7pccxVFBA2GK"
id | STRING | Album ID
images | LIST-OF-DICTIONARY | Keys: `url`, `height`, `width`
name | Integer | Album name
release_date | STRING | Release date – e.g., "2007-03-30"
release_date_precision | STRING | Allowed values: "year", "month", "day"
total_tracks | INTEGER | Number of tracks in album
type | STRING | Only one value: "album"
uri | STRING | Spotify URI

### spotify.tracks
Official documentation on schema: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-track
Fields | Type | Further Detail 
--- | --- | ---
artists | LIST-OF-DICTIONARY | Keys: `external_urls`, `href`, `id`, `name`, `type`, `uri` <br />**`Use key: "id" to link with spotify.artists`**
available_markets | LIST | List of two-letter country codes
disc_number | INTEGER | Disc number (usually 1 unless album consists of more than one disc)
duration_ms | INTEGER | Track length in milliseconds
explicit | BOOLEAN | Whether or not track has explicit lyrics (`true` = yes it does; `false` = no it does not OR unknown)
external_urls | DICTIONARY | Key: `spotify` – e.g. "https://open.spotify.com/track/4lwwKz24FrysgtEQXcBGeF"
href | STRING | e.g., "https://api.spotify.com/v1/tracks/4lwwKz24FrysgtEQXcBGeF"
id | STRING | Track ID
is_local | BOOLEAN | Whether or not track is from a local file
name | Integer | Track name
preview_url | STRING | e.g., "https://p.scdn.co/mp3-preview/aa2027b428ba6d288320b4ff56469bccdadbe70a?cid=99ef327c108045b5a2769d12810a1c1a"
track_number | INTEGER | Number of track. If an album has several discs, track number is the number on the specified disc.
type | STRING | Only one value: "track"
uri | STRING | Spotify URI

### spotify.acousticAttributes
Official documentation on schema: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features
Fields | Type | Further Detail 
--- | --- | ---
danceability | FLOAT | Value between >=0 and <=1
energy | FLOAT | Value between >=0 and <=1
key | INTEGER | Value between >=-1 and <=11
loudness | FLOAT | In decibel (dB) – Value between >=-60 and <=0
mode | INTEGER | Major is represented by `1` and Minor is `0`
speechiness | FLOAT | Value between >=0 and <=1
acousticness | FLOAT | Value between >=0 and <=1
instrumentalness | FLOAT | Value between >=0 and <=1
liveness | FLOAT | Value between >=0 and <=1
valence | FLOAT | Value between >=0 and <=1
tempo | FLOAT | Average beats per minute (BPM)
type | STRING | Only one value: "audio_features"
id | STRING | Track ID **`to link with spotify.tracks`**
uri | STRING | Spotify URI
track_href | STRING | e.g., "https://api.spotify.com/v1/tracks/4lwwKz24FrysgtEQXcBGeF"
analysis_url | STRING| e.g., "https://api.spotify.com/v1/audio-analysis/4lwwKz24FrysgtEQXcBGeF"
duration_ms | INTEGER | Track length in milliseconds
time_signature | INTEGER | Value between >=3 and <=7 
