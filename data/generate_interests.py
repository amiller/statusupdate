import simplejson as json
import random


def generate_interests():
    with open('names.txt','r') as f:
        names = [_.strip() for _ in f.readlines()]

    with open('interests.txt','r') as f:
        interests = [[_.strip() for _ in i.split('|')]
                      for i in f.readlines()]

    names_interests = [{
        'name': name,
        'interests': random.sample(interests, 3)
        } for name in names]

    print names_interests

    with open('names_interests.txt', 'w') as f:
        json.dump(names_interests, f)

if __name__ == '__main__':
    print "Run this with ipython and use generate_interests()"
            
            
