# Note for the crawling process:

To compose a url using track id:
- add /track/{id} to the domain
- the track_id starts from `555813` to `18512629` (as of 11/23/2021)

example: https://www.musixmatch.com/track/555813

In case Tor is needed: https://www.khalidalnajjar.com/stealthy-crawling-using-scrapy-tor-and-privoxy/ 


## Variable fields
- In `page` variable [contains information about the music]:
    - `id`
    - `mbid`
    - `isrc`
    - `commontrackIsrcs`
    - `spotifyId` is used as follows: https://open.spotify.com/track/3SNczkrn6bUm6zZM8i5XDe
    - `commontrackSpotifyIds` contains all the ids linking to the same page
    - `soundcloudId`
    - `xboxmusicId`
    - `name` - Song name
    - `rating` - # [what's the min and max -- to be explored -- for now I see 100 as max]
    - `length` - Music length in second
    - `commontrackId`
    - `instrumental` - Binary feature
    - `explicit` - Binary feature
    - `hasLyrics` - Binary feature
    - `hasSubtitles` - Binary feature
    - `hasRichsync` - Binary feature
    - `hasTrackStructure`- Binary feature
    - `numFavourite`
    - `lyricsId`
    - `subtitleId`
    - `albumId`
    - `albumName`
    - `artistId`
    - `artistMbid`
    - `artistName`
    - `commontrackVanityId` - This id can be used to construct a url shown when access the page: https://www.musixmatch.com/lyrics/Ryokuoushoku-Shakai/Shout-Baby -> id="Ryokuoushoku-Shakai\\u002FShout-Baby"
    - `restricted` - Binary feature
    - `firstReleaseDate` - When the platform does not know the exact date it is shown as the start of the year -> 2018-01-01
    - `updatedTime`
    - `primaryGenres`- List
    - `secondaryGenres` - List

- In `artist` variable inside `page` [contains information about the artist]:


## Issue
Different track_id could point to the same page:
    For example, `https://www.musixmatch.com/track/1000005` and `https://www.musixmatch.com/track/129000666` both point to the same page: `https://www.musixmatch.com/lyrics/Capercaillie/D%C3%A8an-Cadalan-S%C3%A0mhach`.
    The correct track_id is the latter one `129000666` since it was shown in the chrome console while `1000005` was nowhere to be found.

Crawling for track_id from `1000000` to `1000010` ends up getting `[2182676, 2419676, 129000658, 129000663, 129000664, 129000666, 129000668, 129000670, 129000673, 129000674, 129000676] 
