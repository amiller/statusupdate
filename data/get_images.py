import urllib
import re

def get_images():
    with open('names.txt','r') as f:
        names = f.readlines()

    for name in names[:]:
        name = name.strip().replace(' ','+')
        params = urllib.urlencode(dict(name=name))
        src = urllib.urlopen('http://turnyournameintoaface.com/?', params)

        m = re.search('<img src="(face/.*\.png)"', src.read())
        im = urllib.urlopen('http://turnyournameintoaface.com/%s' % m.group(1))

        with open('faces/%s.png' % name,'wb') as f:
            f.write(im.read())

        print name, m.group(1)

if __name__ == '__main__':
    print 'Run this with ipython, and call get_images()'
