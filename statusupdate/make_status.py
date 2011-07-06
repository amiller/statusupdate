import db_statusupdate as db
import random
import sys

pos_trans = dict(
    VERBING='VBG',
    VERBED='VBD',
    ADJECTIVE='JJ',
    PERSON='NP',
    NAME='NP',
    NOUNS='NNS',
    NOUN='NN',
    LOCATION='NN',
    PLACE='NN',
    VERB='VB'
)

def random_word(part='NN'):
    c = db.cursor()
    c.execute("SELECT id FROM words WHERE part='%s' ORDER BY id DESC LIMIT 1" % part)
    mid, = c.fetchone()
    c.execute("SELECT word FROM words WHERE part='%s' and id >= %d LIMIT 1" % \
              (part, random.randint(1, mid)))
    word, = c.fetchone()
    return word


def random_template():
    templates = """
The next time I see NAME I'm going to give them a piece of my NOUN.
PERSON and I went to the LOCATION yesterday! We had such A/AN ADJECTIVE time\
 VERBING all the NOUNS.
I VERBED so hard that I almost VERBED my NOUN.
Let's all get ADJECTIVE and go VERB our NOUNS.
I think I figured out what I want on my NOUN: \"I'll VERB you in PLACE, I \
 guess.\"
I know lots of really good words, but the only one that is apt to describe my\
 new NOUN is: ADJECTIVE.
My relatives came over and they totally VERBED when they saw all of my NOUNS!
My NOUN is VERBING ADJECTIVE.
I just VERBED in my NOUN.
    """.strip().split('\n')

    t = random.choice(templates)

    for k,v in sorted(pos_trans.items(),key=lambda x:x[1])[::-1]:
        while t.rfind(k) >= 0:
            word = random_word(v)
            t = t.replace(k, word, 1)
    return t

def random_person():
    c = db.cursor()
    c.execute("SELECT id FROM people ORDER BY id DESC LIMIT 1")
    mid, = c.fetchone()
    c.execute("SELECT name,pic_url FROM people WHERE id > %d LIMIT 1" % \
              (random.randint(1,mid),))
    person = c.fetchone()
    return person

def random_update():
    t = random_template()

if __name__ == "__main__":
    print random_template()
    print random_person()
