import os
import time
import markovify
import praw

r = praw.Reddit(user_agent='reddit impersonator 1.0')

# reddit login
r.login(os.environ['REDDIT_USER'], os.environ['REDDIT_PASS'])
already_done = []

while True:
    # holds previously-commented on calls

    for submission in r.get_subreddit('test').get_hot(limit=10):
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        for comment in flat_comments:

            commentCheck = comment.body.split()

            call = commentCheck[0]

            if (comment.id in already_done):
                continue

            elif call == "ImpersonatorBot!":
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
                    comment.reply(sentence + '*****' + 'beep boop. I\'m a bot.')
                    already_done.append(comment.id)
                    print ('posted: ' + comment.id)

                else:
                    already_done.insert(0, comment.id)
                    print ('something went wrong: ' + comment.id)
