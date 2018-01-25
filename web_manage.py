#coding=utf8

import Queue
import threading
import os
import urllib2

threads = 10

# target = 'http://wordpress-yang-wordpress.a3c1.starter-us-west-1.openshiftapps.com'
# directory ='/opt/app-root/src'

target = 'http://192.168.3.25:8000/learn_django/'
directory ='/Users/a1/Desktop/杨洋/OpenShift/testDjango/my_django/learn_django/templates'
filters = ['.jpg','.gif','.png','.css']


os.chdir(directory)

web_paths = Queue.Queue()

for r,d,f in os.walk('.'):
    for files in f:
        remote_path = '%s%s' %(r,files)
        if remote_path.startswith('.'):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)

def test_remote():
    print web_paths
    while not web_paths.empty():
        path = web_paths.get()

        url = '%s%s' % (target, path)

        print 'url: '+url
        print ''
        request = urllib2.Request(url)

        try:
            response = urllib2.urlopen(request)
            content  = response.read()

            print '[%d] => %s' %(response.code, path)
            response.close()
        except urllib2.HTTPError as error:
            print 'Failed %s' % error.code
            pass
for i in range(threads):
    print 'Spawning thread : %d' %i
    t = threading.Thread(target=test_remote)
    t.start()
