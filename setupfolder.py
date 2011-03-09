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


def random_str(num=8):
    chrs = string.lowercase + string.digits
    return ''.join([random.choice(chrs) for i in range(num)])


def add_folder(foldername=None):

    # Generate a random new user name and pass
    user = random_str(7)
    pw = random_str(8)
    if foldername is None:
        foldername = user

    fullname = '/home/soc1024c/statusupdate/www/odesk/%s' % foldername
    
    # Save the json to the control directory
    d = dict(user='soc1024c_'+user,
             pw=pw,
             db='soc1024c_'+user,
             foldername=foldername)
    with open('configs/%s.json' % foldername,'w') as f:
        json.dump(d, f)
    
    # Create the database and link the user
    add_mysql_user(user, pw)
    add_mysql_db(user)
    user = 'soc1024c_' + user
    link_mysql_user(user, user)
    add_ftp_user(user, pw, fullname)

    # Create the folder, store the config
    os.mkdir(fullname)
    with open('%s/config.json' % (fullname),'w') as f:
        json.dump(d, f)

