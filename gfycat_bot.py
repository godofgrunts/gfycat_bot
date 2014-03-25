from random import randint
import uuid
import urllib
import requests
import time
import datetime
import pickle
import praw #Python Reddit API Wrapper https://github.com/praw-dev/praw

user_agent = ("gif_2_gfy_bot 2.0 by /u/lol_gog")

data_file = 'already.dat'

r = praw.Reddit(user_agent=user_agent)
r.login('USERNAME','PASSWORD') #CHANGE THIS FOR YOUR BOT
print('Logged in')

already_done = [] #this hold the submission ids for all the post that are done.

gif =['.gif']
newGfy='http://gfycat.com/'
reddits = ['type', 'your', 'approved_subreddits', 'here']
arraycount = len(reddits)

def urlCreator(x):
	gfy='http://upload.gfycat.com/transcode/' #gfy+uid+fetch+gifUrl
	fetch='?fetchUrl='
	uidHex = (uuid.uuid4()).hex #This generates a psuedo-random alphanumeric string
	random = randint(5,10) #gfycat requires the submission to have a unique 5-10 alphanumeric string
	uid = uidHex[0:random]
	return(gfy+uid+fetch+x)

def postGfy(submissions):

	is_gif = any(string in submissions.url for string in gif)
	if submissions.id not in already_done and is_gif:
			msg = '[GIF FOUND]--->%s' % submissions.short_link
			print(msg) #Going to leave this one up.
			ts = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
			print(ts)
			postUrl=submissions.short_link
			gifUrl=submissions.url
			print("Sleeping for 30 seconds to please the gfycat gods...")
			time.sleep(30)
			gfyUrl=urlCreator(gifUrl)
			j = urllib.request.urlopen(gfyUrl).read()
			jstr = str(j)
			array = jstr.split("\"")
			newUrl = newGfy+array[3]
			try:
				r.submit('SUBREDDIT YOU ARE SUBMITTING TO', submissions.id, url=newUrl)
			except praw.errors.AlreadySubmitted:
				print("URL already submitted... Moving on.")
			already_done.append(submissions.id)
			outfile = open(data_file ,"wb")
			pickle.dump(already_done, outfile) #dump already_done to file
			outfile.close()

def searchSubreddit(subs): #reddit[y]
	sub = r.get_subreddit(subs)
	print('Starting Process for %s hot...' % sub)
	for hot in sub.get_hot():
		postGfy(hot)
	print('Starting Process for %s new...' % sub)
	for new in sub.get_new():
		postGfy(new)


def main():
	try:
		with open(data_file, 'at', encoding='utf8') as f:
			already_done = pickle.load(f) #load already_done
			f.close()
	except IOError as e:
		pass # it's ok if it doesn't exist
	while True:
		for reddit in reddits:
			searchSubreddit(reddit)
		time.sleep(10)


main()
