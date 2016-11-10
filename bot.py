import os
import time
import markovify
import praw

r = praw.Reddit(user_agent='reddit impersonator 0.1')

r.login(os.environ['REDDIT_USER'], os.environ['REDDIT_PASS'])

while True:
    for submission in r.get_subreddit('test').get_hot(limit=5):
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        already_done = set()
        for comment in flat_comments:

            commentCheck = comment.body.split()

            call = commentCheck[0]

            if call == "ImpersonatorBot!":
                author = commentCheck[1]

                user = r.get_redditor(author)
                comments = ''

                for historicalComment in user.get_comments(limit=400):
                    comments = comments + ' ' + historicalComment.body

                comments = comments.encode('ascii', 'ignore')

                text_model = markovify.Text(comments)
                sentence = text_model.make_sentence()

                if len(sentence):
                    comment.reply(sentence)

                already_done.add(comment.id)
    time.sleep(15)
