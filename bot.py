import os
import time

import markovify

import praw

import psycopg2
import urlparse

# database connection
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor()

# reddit api wrapper connection
r = praw.Reddit(user_agent='reddit impersonator 1.0')

# reddit login
r.login(os.environ['REDDIT_USER'], os.environ['REDDIT_PASS'])

# holds previously-commented on calls
cur.execute("SELECT * FROM posts")
records = cur.fetchall()

# bot signature
signature = '^^beep ^^boop. ^^I\'m ^^a ^^bot.  ^^Let ^^/u/CommodoreObvious ^^know ^^if ^^something ^^is ^^wonky'

while True:

    # grab previously-commented-on posts
    cur.execute("SELECT * FROM posts")
    records = cur.fetchall()

    for submission in r.get_subreddit('impersonatorbot').get_hot(limit=10):
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        for comment in flat_comments:

            commentCheck = comment.body.split()

            call = commentCheck[0]

            if (comment.id,) in records:
                continue

            elif call == "ImpersonatorBot!":

                if len(commentCheck) > 1:

                    author = commentCheck[1]

                    user = r.get_redditor(author)
                    comments = ''

                    for historicalComment in user.get_comments(limit=100):
                        comments = comments + ' ' + historicalComment.body

                    comments = comments.encode('ascii', 'ignore')

                    text_model = markovify.Text(comments)
                    sentence = text_model.make_sentence()

                    if sentence == None:
                        print ('markovify failed, will try again')

                    elif sentence:
                        # add reply
                        comment.reply(sentence + '\n\n ******* \n\n' + signature)

                        # post to db
                        data = [comment.id]
                        SQL = ("INSERT INTO posts (id) VALUES (%s);")
                        cur.execute(SQL, data)
                        conn.commit()

                        # grab previously-commented-on posts
                        cur.execute("SELECT * FROM posts")
                        records = cur.fetchall()

                        print ('posted: ' + comment.id)

                    else:
                        # post to db
                        data = [comment.id]
                        SQL = ("INSERT INTO posts (id) VALUES (%s);")
                        cur.execute(SQL, data)
                        conn.commit()

                        # grab previously-commented-on posts
                        cur.execute("SELECT * FROM posts")
                        records = cur.fetchall()

                        print ('something went wrong: ' + comment.id)

                else:
                    comment.reply('Please provide a username for me to impersonate! Like this: `ImpersonatorBot! PresidentObama`' + '\n\n ******* \n\n' + signature)

                    # post to db
                    data = [comment.id]
                    SQL = ("INSERT INTO posts (id) VALUES (%s);")
                    cur.execute(SQL, data)
                    conn.commit()

                    # grab previously-commented-on posts
                    cur.execute("SELECT * FROM posts")
                    records = cur.fetchall()
