import simplejson as json
import MySQLdb
from nltk.corpus import brown
import nltk
from itertools import islice
import subprocess


# Read the config properties from the json in the current directory
with open('config.json','r') as f:
    config = json.load(f)

conn = MySQLdb.connect(user=config['user'],passwd=config['pw'],db=config['db'])


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

def folder_init():
    #clear_database()
    create_database()
    #add_words()
    copy_templates()


def copy_templates():
    # Copy all the template files, especially phpmyadmin
    subprocess.call('cp -r ~/statusupdate/odesk/template/* .', shell=True)
    subprocess.call('ln -s ~/statusupdate/www/webpy .', shell=True)

    # Replace the server information in the template
    with open('phpmyadmin/config.inc.php','r') as f:
        template = f.read()
    with open('phpmyadmin/config.inc.php','w') as f:
        f.write(template.format(DBUSER=config['user'],
                                PASSWORD=config['pw'],
                                DATABASE=config['db']))


def clear_database():
    c = conn.cursor()
    for table in ['words','interests','word_interests','people','people_interests']:
        try:
            c.execute("""DROP TABLE %s""" % table)
        except MySQLdb.OperationalError:
            print "Couldn't delete, tables %s probably doesn't exist" % table
    
    
def create_database():
    tables = ["""CREATE TABLE IF NOT EXISTS `word_interests` (
    `id` int(11) NOT NULL auto_increment,
    `word` varchar(64) NOT NULL,
    `interest` varchar(255) NOT NULL,
    PRIMARY KEY  (`id`)
    ) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=23 ;""",

    """CREATE TABLE IF NOT EXISTS `words` (
    `id` int(11) NOT NULL auto_increment,
    `word` varchar(64) NOT NULL,
    `part` varchar(16) NOT NULL,
    PRIMARY KEY  (`id`)
    ) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=57129 ;""",

    """CREATE TABLE IF NOT EXISTS `interests` (
    `id` int(11) NOT NULL auto_increment,
    `interest` varchar(255) NOT NULL,
    PRIMARY KEY  (`id`)
    ) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=48 ;""",

    """CREATE TABLE IF NOT EXISTS `status_templates` (
    `id` int(11) NOT NULL auto_increment,
    `template` text NOT NULL,
    PRIMARY KEY  (`id`)
    ) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=24 ;""",

    """CREATE TABLE IF NOT EXISTS `people` (
    `id` bigint(20) NOT NULL,
    `firstname` varchar(64) NOT NULL,
    `lastname` varchar(64) NOT NULL,
    `pic_url` varchar(255) NOT NULL,
    `profile` text NOT NULL,
    PRIMARY KEY  (`id`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8;""",

    """CREATE TABLE IF NOT EXISTS `people_interests` (
    `id` int(11) NOT NULL auto_increment,
    `person_id` bigint(20) NOT NULL,
    `interest` varchar(255) NOT NULL,
    PRIMARY KEY  (`id`)
    ) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;"""]

    
    c = conn.cursor()              
    for table in tables:
        print table[:64].split('\n')[0]
        c.execute(table)
