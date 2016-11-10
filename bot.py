import os
import time

import praw

# reddit really wants you to use a unique user agent string.
# see https://github.com/reddit/reddit/wiki/API#rules
r = praw.Reddit(user_agent='reddit impersonator 0.1')
# login isn't strictly needed here since we're not
# posting, commenting, etc.
# you'll need to set the REDDIT_USER and REDDIT_PASS
# environment variables before you run this bot
r.login(os.environ['REDDIT_USER'], os.environ['REDDIT_PASS'])

while True:
    for submission in r.get_subreddit('ImpersonatorBot').get_hot(limit=5):
        print(submission)
    time.sleep(15)
