from automation import TaskManager
import time
import glob
import os

# Saves a crawl output DB to the Desktop
db_loc  = os.path.expanduser('~/Desktop/facebook.sqlite')

browser_params = TaskManager.load_default_params(1)
browser_params[0]['proxy'] = False

# load a list of usernames, one per line
with open('fbusers.txt','r') as f:
    users = set(f.read().strip().split('\n'))

# don't double crawl
outdir = glob.glob('../data/fbfriends/*')
crawled = set()
for fname in outdir:
    crawled.add(fname.split('/')[-1][0:-8])
users = users.difference(crawled)

print "len of users to crawl: " + str(len(users))

manager = TaskManager.TaskManager(db_loc, browser_params, 1)

manager.get('http://www.facebook.com')
manager.fblogin()
time.sleep(1)
for user in users:
    manager.get('https://www.facebook.com/' + user + '/friends')
    time.sleep(5)
    manager.extract_friends(user, overwrite_timeout=300)

manager.close()
