'''
Created on Jul 15, 2012

@author: anass ahmed
'''
from elixir import *
import os.path, sys, datetime

db_user = 'username'
db_password = 'password'
db_name = 'dbname'
db_server = 'localhost'
prefix = "db_"
#metadata.bind = "mysql://%s:%s@%s/%s" %(db_user, db_password, db_server, db_name)
metadata.bind = "sqlite:///"+os.path.join(os.path.dirname(sys.argv[0]), 'db.sqlite')

class user(Entity):
    using_options(tablename = prefix+"users")
    fb_id = Field(Unicode(100), index=True)
    username = Field(Unicode(30), index=True)
    fullname = Field(Unicode(100))
    gender = Field(Unicode(10))
    access_token = Field(UnicodeText)
    expires = Field(Integer)
    created_at = Field(DateTime)
    answers = OneToMany('answer')
    invites = OneToMany('invite', inverse='user')

class question(Entity):
    using_options(tablename = prefix+"questions")
    question = Field(UnicodeText)
    publish_date = Field(Date)
    created_at = Field(DateTime)
    options = OneToMany("option")

class option(Entity):
    using_options(tablename = prefix+"options")
    question = ManyToOne("question")
    option = Field(UnicodeText)

class answer(Entity):
    using_options(tablename = prefix+"answers")
    user = ManyToOne("user")
    question = ManyToOne("question")
    answer = ManyToOne("option")

class invite(Entity):
    using_options(tablename = prefix+"invites")
    user = ManyToOne("user")
    fb_request_id = Field(Unicode(100), index=True)
    user_invited = ManyToOne("user")
    created_at = Field(DateTime)
    
if __name__ == "__main__":
    setup_all()
    try:
        _user = user.get_by(id = 1)
    except Exception:
        create_all()
        print "Created Tables."
    
    while(True):
        a = raw_input("Do you want to add a question? (y/n): ")
        if a == 'y' or a == 'Y':
            q = question(question = str(raw_input("Question: ")).decode('utf8'))
            q.publish_date = datetime.datetime.strptime(raw_input("Publish Date (dd-mm-yyyy): "),
                                                        '%d-%m-%Y')
            q.created_at = datetime.datetime.now()
            o1 = option(option = raw_input("Option 1: ").decode('utf8'), question = q)
            o2 = option(option = raw_input("Option 2: ").decode('utf8'), question = q)
            session.commit()
            print "Question Saved."
        else:
            sys.exit()
            

