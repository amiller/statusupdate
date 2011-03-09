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
)

def random_word(part='NN'):
    c = db.conn.cursor()
    cmd = """
        SELECT word FROM words T
        JOIN (SELECT MAX(id) AS mid FROM words
              WHERE part='{part}') AS TT
        ON T.id >= CEIL(RAND()*TT.mid)
        AND part = '{part}'
        LIMIT 1;""".format(part=part)
    c.execute(cmd)
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

    db.conn.cursor()    
    for k,v in sorted(pos_trans.items(),key=lambda x:x[1])[::-1]:
        while t.rfind(k) >= 0:
            word = random_word(v)
            t = t.replace(k, word, 1)
    return t


if __name__ == "__main__":
    print random_template()
