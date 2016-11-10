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
        print(flat_comments)
        for comment in flat_comments:
            commenter = comment.author
            if comment.body == "ImpersonatorBot!":
                user = r.get_redditor(commenter)
                comments = ''

                for comment in user.get_comments(limit=400):
                    comments = comments + ' ' + comment.body

                text_model = markovify.Text(comments)
                sentence = text_model.make_sentence()

                comment.reply(sentence)

                already_done.add(comment.id)
    time.sleep(500)
