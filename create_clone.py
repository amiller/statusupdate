import subprocess
import random
import string
import os
import simplejson as json
from userpw import ENV_USER, ENV_PASS


def run_cmd(cmd):
    subprocess.call(cmd.split())


def wget_cmd(cmd):
    return "wget --delete-after --user=%s --password=%s http://soc1024.com:2082"\
           "/frontend/na4/%s" % (ENV_USER, ENV_PASS, cmd)


def add_mysql_user(user, pw):
    cmd = "sql/sqluseradded.html?user=%s&pass=%s" % (user, pw)
    run_cmd(wget_cmd(cmd))


def add_mysql_db(db):
    cmd = "sql/sqladded.html?db=%s" % db
    run_cmd(wget_cmd(cmd))


def link_mysql_user(user, db):
    cmd = "sql/sqlusertodbadded.html?user=%s&db=%s&ALL=ALL" % (user, db)
    run_cmd(wget_cmd(cmd))


def add_ftp_user(user, pw, directory):
    cmd = "ftp/doaddftp.html?login=%s&password=%s&homedir=%s" % (user, pw, directory)
    run_cmd(wget_cmd(cmd))


def del_db(dbname):
    cmd = "sql/dodeldb.html?db=%s" % dbname
    run_cmd(wget_cmd(cmd))

    
def del_ftp(user):
    cmd = "ftp/dodelftp.html?login=%s" % user
    run_cmd(wget_cmd(cmd))


def del_dbuser(dbuser):
    cmd = "sql/deluser.html?user=%s" % dbuser
    run_cmd(wget_cmd(cmd))


def random_str(num=8):
    chrs = string.lowercase + string.digits
    return ''.join([random.choice(chrs) for i in range(num)])


def add_folder(foldername=None):

    # Generate a random new user name and pass
    user = random_str(7)
    pw = random_str(8)
    if foldername is None:
        foldername = user

    # Save the json to the control directory
    d = dict(user='soc1024c_'+user,
             pw=pw,
             db='soc1024c_'+user,
             foldername=foldername)

    # Create the folder, store the config
    fullname = '/home/soc1024c/statusupdate/www/odesk/%s' % foldername
    os.mkdir(fullname)
    with open('%s/config.json' % (fullname),'w') as f:
        json.dump(d, f)


    
    # Create the database and link the user
    add_mysql_user(user, pw)
    add_mysql_db(user)
    user = 'soc1024c_' + user
    link_mysql_user(user, user)
    add_ftp_user(user, pw, fullname)


import argparse

def go():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?')
    parser.add_argument('-new', action='store_true')
    parser.add_argument('-rm', action='store_true')
    args = parser.parse_args()
    print args
    if args.rm:
        if not args.name:
            parser.print_help()
            return
        fullname = '/home/soc1024c/statusupdate/www/odesk/%s' % args.name
        with open('%s/config.json' % fullname,'r') as f:
            config = json.load(f)
        del_db(config['db'])
        del_dbuser(config['user'])
        del_ftp(config['user'])
        print "Removing directory %s" % fullname
        run_cmd("rm -r %s" % fullname)
    elif args.new:
        if not args.name:
            add_folder()
        else:
            add_folder(args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    go()
