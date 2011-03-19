import simplejson as json
import MySQLdb
from nltk.corpus import brown
import nltk
from itertools import islice
import subprocess
import os
import simplejson


def add_words():
    def get_words(corp=brown, pos='NN'):
        return (word for word,_pos in corp.tagged_words() if _pos==pos)

    def consume(iterator, n):
        next(islice(iterator, n, n), None)
            
    parts = """VBG VBD JJ NN NNS NP VB""".split()
    
    c = conn.cursor()
    for pos in parts:
        print pos
        iterator = get_words(pos=pos)
        while True:
            words = [_ for _ in islice(iterator, 0, 20)]
            if len(words) == 0: break
            str = "INSERT INTO words (word,part) VALUES %s" % \
              ','.join(["('%s','%s')" % (conn.escape_string(word),pos)
                        for word in words])
            c.execute(str)


def add_people():
    global names_interests
    with open('/home/soc1024c/statusupdate/data/names_interests.txt','r') as f:
        names_interests = json.load(f)
    c = conn.cursor()

    for n in names_interests:
        name = n['name'].replace(' ','+')
        url = 'http://soc1024.com/statusupdate/faces/%s.png' % name
        c.execute("INSERT INTO people (name, pic_url) \
                   VALUES ('%s','%s')" % (name, url))
        c.execute("INSERT INTO people_interests (name, interest) \
                   VALUES %s" % \
                  ','.join(["('%s', '%s')" % (name,_[0]) for _ in n['interests']])) 
    

def add_interests():
    with open('/home/soc1024c/statusupdate/data/interests.txt','r') as f:
        interests = [[_.strip() for _ in i.split('|')]
                      for i in f.readlines()]
    c = conn.cursor()
    for i in interests:
        cmd = ("INSERT INTO interests (interest, desc) \
                   VALUES ('%s','%s')" % (i[0], i[1]))
        print cmd
        c.execute(cmd)



def folder_init():
    clear_database()
    create_database()
    copy_templates()
    add_people()
    add_interests()
    

def copy_templates():
    # Copy all the template files, especially phpmyadmin
    subprocess.call('cp -r ~/statusupdate/template/* .', shell=True)
    subprocess.call('ln -s ~/statusupdate/webpy .', shell=True)

    # Replace the server information in the template
    with open('phpmyadmin/config.inc.php','r') as f:
        template = f.read()
    with open('phpmyadmin/config.inc.php','w') as f:
        f.write(template.format(DBUSER=config['user'],
                                PASSWORD=config['pw'],
                                DATABASE=config['db']))


def clear_database():
    c = conn.cursor()
    for table in ['words','interests','word_interests','people',
                  'people_interests', 'status_templates']:
        try:
            c.execute("""DROP TABLE %s""" % table)
        except MySQLdb.OperationalError:
            print "Couldn't delete, tables %s probably doesn't exist" % table
    
    
def create_database():
    tables = ["""CREATE TABLE IF NOT EXISTS `word_interests` (
    `word` varchar(64) NOT NULL,
    `interest` varchar(128) NOT NULL,
    PRIMARY KEY  (`word`,`interest`)
    ) ENGINE=MyISAM  DEFAULT CHARSET=utf8;""",

    """CREATE TABLE IF NOT EXISTS `words` (
    `part` varchar(16) NOT NULL,
    `id` int(11) NOT NULL auto_increment,
    `word` varchar(64) NOT NULL,
    PRIMARY KEY  (`part`,`id`),
    KEY  (`word`)
    ) ENGINE=MyISAM  DEFAULT CHARSET=utf8;""",

    """CREATE TABLE IF NOT EXISTS `interests` (
    `interest` varchar(128) NOT NULL,
    `desc` varchar(128) NOT NULL,
    PRIMARY KEY  (`interest`)
    ) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0 ;""",

    """CREATE TABLE IF NOT EXISTS `status_templates` (
    `id` int(11) NOT NULL auto_increment,
    `template` text NOT NULL,
    PRIMARY KEY  (`id`)
    ) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0 ;""",

    """CREATE TABLE IF NOT EXISTS `people` (
    `name` varchar(64) NOT NULL,
    `pic_url` varchar(255) NOT NULL,
    `profile` text NOT NULL,
    PRIMARY KEY  (`name`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8;""",

    """CREATE TABLE IF NOT EXISTS `people_interests` (
    `name` varchar(64) NOT NULL,
    `interest` varchar(128) NOT NULL,
    PRIMARY KEY  (`name`,`interest`),
    KEY (`interest`)
    ) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0 ;"""]

    
    c = conn.cursor()              
    for table in tables:
        print table[:64].split('\n')[0]
        c.execute(table)


import argparse
def go():
    parser = argparse.ArgumentParser()
    parser.add_argument('-init', action='store_true')
    parser.add_argument('-addwords', action='store_true')
    parser.add_argument('name', default='master', nargs='?')
    args = parser.parse_args()
    if not (args.init or args.addwords):
        parser.print_help()

    os.chdir('www/odesk/%s' % args.name)
        
    # Read the config properties from the json in the current directory
    global config, conn
    with open('config.json','r') as f:
        config = json.load(f)

    conn = MySQLdb.connect(user=config['user'],passwd=config['pw'],db=config['db'])

    if args.init:
        folder_init()
    elif args.addwords:
        add_words()


if __name__ == "__main__":
    go()
