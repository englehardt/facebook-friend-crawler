from automation import TaskManager
import time
import glob
import sys
import os

FB_USERNAME = ''
FB_PASSWORD = ''

USERS = set()
USERS.add('')

if not os.path.exists(os.path.join(os.path.dirname(__file__),'../data')):
    os.mkdir(os.path.join(os.path.dirname(__file__),'../data'))
db_loc  = os.path.join(os.path.dirname(__file__),'../data/facebook.sqlite')

browser_params = TaskManager.load_default_params(1)
browser_params[0]['proxy'] = False

# don't double crawl
outdir = glob.glob('../data/fbfriends/*')
crawled = set()
for fname in outdir:
    crawled.add(fname.split('/')[-1][0:-8])
users = USERS.difference(crawled)

print "len of users to crawl: " + str(len(users))

if len(users) == 0:
    print "No users to crawl, exiting..."
    sys.exit(0)

manager = TaskManager.TaskManager(db_loc, browser_params, 1)

for user in users:
    manager.get('https://www.facebook.com/' + user + '/friends')
    time.sleep(5)
    manager.extract_friends(user, FB_USERNAME, FB_PASSWORD, overwrite_timeout=300)

manager.close()
