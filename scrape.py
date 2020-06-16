import os
from dotenv import load_dotenv
import praw
import requests
import time
import datetime
from peewee import SqliteDatabase, Model, TextField

load_dotenv()

REDDIT_ID = os.getenv("REDDIT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDDIT_SUBREDDIT = os.getenv("REDDIT_SUBREDDIT")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
DATABASE_PATH = os.getenv("DATABASE_PATH")

BASE_URL = "https://old.reddit.com"
DATE_FORMAT = "%m/%d/%Y %I:%M %p"
FOOTER_TEXT = "reddit-to-discord v0.3.0 - jon"

db = SqliteDatabase(DATABASE_PATH)


class Post(Model):
    class Meta:
        database = db

    post_id = TextField()


reddit = praw.Reddit(client_id=REDDIT_ID,
                     client_secret=REDDIT_SECRET, user_agent=REDDIT_USER_AGENT)


def scrape():
    for submission in reversed(list(reddit.subreddit(REDDIT_SUBREDDIT).new(limit=10))):

        try:
            already_found = Post.get(post_id=submission.id)
            print('found', already_found)
            continue
        except:
            p = Post()
            p.post_id = submission.id
            p.save()

        title = submission.title
        posted = submission.author.name
        timestamp = datetime.datetime.utcfromtimestamp(submission.created_utc)
        timestamp -= datetime.timedelta(hours=5)  # Eastern Time

        if submission.is_self:
            body = submission.selftext

            if len(body) > 2000:
                body = body[:2000] + '...'

            _json = {
                "embeds": [{
                    "title": title,
                    "url": BASE_URL + submission.permalink,
                    "description": submission.selftext,
                    "footer": {
                        "text": FOOTER_TEXT
                    },
                    "fields": [
                        {
                            "name": "Submitted By:",
                            "value": f"[{posted}](https://old.reddit.com/user/{posted})",
                            "inline": True,
                        },
                        {
                            "name": "Timestamp",
                            "value": timestamp.strftime(DATE_FORMAT),
                            "inline": True,
                        }
                    ]
                }]
            }
            requests.post(DISCORD_WEBHOOK, json=_json)

        else:
            _json = {
                "embeds": [{
                    "title": title,
                    "url": BASE_URL + submission.permalink,
                    "footer": {
                        "text": FOOTER_TEXT
                    },
                    "image": {
                        "url": submission.thumbnail,
                        "width": submission.thumbnail_width,
                        "height": submission.thumbnail_height,
                    },
                    "fields": [
                        {
                            "name": "Link",
                            "value": submission.url
                        },
                        {
                            "name": "Submitted By:",
                            "value": f"[{posted}](https://old.reddit.com/user/{posted})",
                            "inline": True,
                        },
                        {
                            "name": "Timestamp",
                            "value": timestamp.strftime(DATE_FORMAT),
                            "inline": True,
                        },
                        {
                            "name": "Thumbnail",
                            "value": ':arrow_down:',
                        }
                    ]
                }]
            }
            requests.post(DISCORD_WEBHOOK, json=_json)
        time.sleep(1)


if __name__ == '__main__':
    db.create_tables([Post], safe=True)
    scrape()
