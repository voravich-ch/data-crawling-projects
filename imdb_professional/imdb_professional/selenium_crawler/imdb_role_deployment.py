from imdb_role_crawler import ImdbRoleCrawler
import pymongo
from tqdm import tqdm

def main():
    # Initialise ImdbRoleCrawler
    crawler = ImdbRoleCrawler()

    # Start Selenium session
    crawler.start_session()

    # Get urls
    mongo_uri = 'mongodb://127.0.0.1:27018'
    client = pymongo.MongoClient(mongo_uri)
    collection = client['imdbProfessional']['imdb_cast_id']
    cursor = collection.find({}, projection = {"_id": 0, "cast_id": 1})
    urls = [f"https://www.imdb.com/name/{cast_id['cast_id']}" for cast_id in cursor]

    # Specify mongo collection for data storage
    collection = client['imdbProfessional']['imdb_role']

    # Start crawling
    for url in tqdm(urls):
        crawler.get_role_data(url, collection)
    
    # Close Selenium session
    crawler.end_session()

if __name__ == '__main__':
    main()
