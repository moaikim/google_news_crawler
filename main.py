import time
import argparse

import google_news_cron

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('Mode', type=str, choices=['once','interval','cron'], default='once', help="Choose how you want to run the code")
    parser.add_argument('Country', type=str, choices=['en','ko'], help="which country will you search for news?")
    parser.add_argument('Keyword', type=str, help="Enter keywords to crawl")

    args = parser.parse_args()
    try:
        gooleNewsCron = google_news_cron.GoogleNewsCron()
        gooleNewsCron.run(args.Mode, args.Country, args.Keyword)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        gooleNewsCron.stop()

if __name__=="__main__":
    main()
