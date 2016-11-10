import os
import time
import markovify
import praw

r = praw.Reddit(user_agent='reddit impersonator 1.0')

# reddit login
r.login(os.environ['REDDIT_USER'], os.environ['REDDIT_PASS'])

# holds previously-commented on calls
already_done = []

while True:

    for submission in r.get_subreddit('test').get_hot(limit=10):
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        for comment in flat_comments:

            commentCheck = comment.body.split()

            call = commentCheck[0]

            if (comment.id in already_done):
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
                        comment.reply(sentence + '\n\n' + '/u/' + author + '\n\n' + ' \n\n ******* \n\n' + '(beep boop. I\'m a bot. Let /u/CommodoreObvious know if something is wonky)')
                        already_done.append(comment.id)
                        print ('posted: ' + comment.id)

                    else:
                        already_done.insert(0, comment.id)
                        print ('something went wrong: ' + comment.id)

                else:
                    comment.reply('Please provide a username for me to impersonate! Like this: `ImpersonatorBot! PresidentObama`' + '\n\n ******* \n\n' + '(beep boop. I\'m a bot. Let /u/CommodoreObvious know if something is wonky)')
                    already_done.append(comment.id)
