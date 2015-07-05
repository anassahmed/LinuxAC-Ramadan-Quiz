'''
Created on Jul 16, 2012

@author: anass ahmed
'''

#configuration

APP_ID = 'APP_ID'
APP_SECRET = 'APP_SECRET'
CANVAS_URL = 'http://apps.facebook.com/linuxac_quiz_test'
PAGE_URL = "https://www.facebook.com/linuxac.org/app_307348792694597"
#CANVAS_URL = PAGE_URL
PAGE_ID = "120042248076755"

from okasha.baseWebApp import baseWebApp, expose, forbiddenException
from okasha.bottleTemplate import bottleTemplate
from elixir import *
from db import *
import time, datetime, facebook, json, base64

setup_all()
try:
    _user = user.get_by(id = 1)
except Exception:
    create_all()
    print "Created Tables."

class linuxQuiz(baseWebApp):
    """
    Main Web Framework class.
    """
    
    def __init__(self, *args, **kw):
        baseWebApp.__init__(self, *args, **kw)
        self.access_token = u''
        self.access_token_expires = time.time()
        
    def decode_signed_request(self, signed_request):
        sep = signed_request.find('.')
        data = signed_request[sep:].replace('.','') + '='
        try:
            data = json.loads(base64.urlsafe_b64decode(data))
        except TypeError:
            data += '='
            data = json.loads(base64.urlsafe_b64decode(data))
        return data
    
    def is_liked(self):
        """ 
        Check if the user liked the facebook page of LinuxAC.
        """
        d = self.graph.get_connections("me","likes/%s" %PAGE_ID)
        if d["data"]: 
            return True
        else:
            return False
        
    def add_user(self):
        """
        Adds New User or get the existing user from database.
        """
        
        self.user_db = user.get_by(fb_id = self.user_graph["id"].decode('utf8'))
        if not self.user_db:
            self.user_db = user(fb_id = self.user_graph["id"].decode('utf8'),
                                username = self.user_graph["username"].decode('utf8'),
                                fullname = self.user_graph["name"],
                                gender = self.user_graph["gender"].decode('utf8'),
                                access_token = self.access_token.decode('utf8'),
                                expires = self.access_expires,
                                created_at = datetime.datetime.now())
            session.commit()
            self.add_invite()
        return self.user_db
    
    def add_invite(self):
        invites = self.graph.get_connections("me", "apprequests")
        print invites["data"]
        if invites["data"]:
            for i in invites["data"]:
                if not invite.get_by(user_invited = self.user_db):
                    inv = invite(user = user.get_by(fb_id = i["from"]["id"]), 
                                 user_invited = self.user_db, 
                                 fb_request_id = i["id"], 
                                 created_at = datetime.datetime.strptime(i["created_time"][:19], "%Y-%m-%dT%H:%M:%S"))
                    session.commit()
                    #self.graph.delete(inv.fb_request_id)
    
    def get_question(self):
        q = question.get_by(publish_date = datetime.date.today())
        from sqlalchemy import and_
        if not answer.query.filter(and_(answer.user == self.user_db, answer.question == q)).count():
            return q
    
    def add_answer(self, user, option_id):
        q = self.get_question()
        if q:
            a = answer(user = user, question = q, answer = option.get_by(id = option_id))
            session.commit()
    
    @expose(bottleTemplate, ['index.tpl'])
    def _root(self, rq, *args):
        auth_url = facebook.auth_url(APP_ID, CANVAS_URL, perms=['user_likes'])
        r = {'rq':rq, 
             'args':args, 
             'is_authed':0, 
             'auth_url':auth_url,
             'is_liked':False,
             'APP_ID':APP_ID,
             'question': question.get_by(publish_date = datetime.date.today()),
             }
        if rq.q.has_key("signed_request"):
            if rq.q.getfirst("signed_request",""):
                parsed_request = self.decode_signed_request(rq.q.getfirst("signed_request", ""))
                if parsed_request: 
                    try:
                        self.access_token = parsed_request['oauth_token']
                        self.access_expires = int(parsed_request['expires'])
                        if self.access_expires > time.time():
                            self.graph = facebook.GraphAPI(self.access_token)
                            self.user_graph = self.graph.get_object("me")
                            r['is_authed'] = 1
                            r['is_liked'] = self.is_liked()
                            r['user'] = self.add_user()
                            r['question'] = self.get_question()
                        else: 
                            self.graph.extend_access_token(APP_ID, APP_SECRET)
                            return self._root(rq, *args)
                    except KeyError:
                        return r
        return r
    
    @expose(bottleTemplate, ['index.tpl'])
    def answer(self, rq, *args):
        if rq.q.has_key("answer"):
            auth_url = facebook.auth_url(APP_ID, CANVAS_URL, perms=['user_likes'])
            r = {'rq':rq, 
                 'args':args, 
                 'is_authed':1, 
                 'auth_url':auth_url,
                 'is_liked':True,
                 'question':self.get_question(),
                 'APP_ID':APP_ID,
                 'question': question.get_by(publish_date = datetime.date.today())
                 }
            answer_user = user.get_by(id = int(rq.q.getfirst("user_id")))
            self.add_answer(answer_user, int(rq.q.getfirst("answer","")))
            r["question"] = "answered"
            r['user'] = answer_user
            return r
        else:
            raise forbiddenException()
    
    @expose()
    def redirect(self, rq, *args):
        return """
        <script type="text/javascript">
            top.location.href = "%s";
        </script> """ % PAGE_URL
    
