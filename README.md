# reddit-to-discord

A simple Python script to post Reddit posts to a Discord channel. Makes a few assumptions around format and timezone.

## Setup
1. Create a .env file with the following values:

| Variable Name     | Example Value                           | Description                                 |
|-------------------|-----------------------------------------|---------------------------------------------|
| REDDIT_ID         | my_reddit_client_id                     | Reddit API Client ID                        |
| REDDIT_SECRET     | my_reddit_client_secret                 | Reddit API Client Secret                    |
| REDDIT_USERNAME   | grandrapidsdiscord                      | Reddit username                             |
| REDDIT_PASSWORD   | not_a_password                          | Reddit password                             |
| REDDIT_USER_AGENT | python:reddit-to-discord:0.3.1 (by jon) | User agent to identify the bot as           |
| REDDIT_SUBREDDIT  | grandrapids                             | Subreddit to scrape                         |
| DISCORD_WEBHOOK   | https://discordapp.com/whatever         | Discord webhook URL to post reddit posts to |
| DATABASE_PATH     | subreddit.sqlite                        | Path to sqlite database file                |

2. Create a python virtualenv
```bash
python3 -m virtualenv
. venv/bin/activate
pip install -r requirements.txt
```

3. Run the script

`python scrape.py`

4. Create a crontab entry to run the script on a regular basis. I use the following entry to run every 5 minutes:

`*/5 * * * * /opt/reddit-to-discord/venv/bin/python3 /opt/reddit-to-discord/scrape.py >/dev/null 2>&1`