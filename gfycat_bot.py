from random import randint
import uuid
import urllib
import requests
import time
import praw #Python Reddit API Wrapper https://github.com/praw-dev/praw

user_agent = ("gif_2_gfy_bot 1.0 by /u/lol_gog")
r = praw.Reddit(user_agent=user_agent)
r.login('USERNAME','PASSWORD') #CHANGE THIS FOR YOUR BOT
print('Logged in')

already_done = [] #this hold the submission ids for all the post that are done.
gif =['.gif']
newGfy='http://gfycat.com/'
reddits = r.get_subreddit('SUBREDDIT')#TYPE IN YOUR APPROVED SUBREDDITS


def urlCreator(x):
	gfy='http://upload.gfycat.com/transcode/' #gfy+uid+fetch+gifUrl
	fetch='?fetchUrl='
	uidHex = (uuid.uuid4()).hex #This generates a psuedo-random alphanumeric string
	random = randint(5,10) #gfycat requires the submission to have a unique 5-10 alphanumeric string
	uid = uidHex[0:random]
	return(gfy+uid+fetch+x)



while True:
	for submissions in reddits.get_hot():
		#print(vars(comments))
		is_gif = any(string in submissions.url for string in gif)
		if submissions.id not in already_done and is_gif:
				msg = '[GIF FOUND]--->%s' % submissions.short_link
				print(msg)
				postUrl=submissions.short_link
				gifUrl=submissions.url
				gfyUrl=urlCreator(gifUrl)
				print(gfyUrl)
				j = urllib.request.urlopen(gfyUrl).read()
				jstr = str(j)
				array = jstr.split("\"")
				newUrl = newGfy+array[3]
				print(newUrl)                              
				post = r.get_submission(submission_id=submissions.id)
				post.add_comment(newUrl+'\n\nThis post has been uploaded to gfycat.com! To learn more, check out gfycat.com/about')
				already_done.append(submissions.id)
				print(already_done)
        time.sleep(60) #No need to run it so often I think.


	

