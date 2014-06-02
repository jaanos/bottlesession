from bottle import request, response
import glob
import pickle
import os

SESSIONDIR = "sessions/"

class session:
    #Objects of this class will allow for easy session management in a bottle-py based, web app
    
    def __init__(self, secret_key="reallyinsecurepassword"):
        #Set the secret key to sign the cookies
        self.sessionid = None
        self.secret_key = secret_key
        self.sess = {}
        #Look for a session cookie
        #If one exists, then open the corresponding session file. Otherwise, continue with a blank session.
        try:
            self.sessionid = str(request.get_cookie("sessionid", secret=self.secret_key))
            print("Loading %s" % self.sessionid)
            print(SESSIONDIR+self.sessionid+".ses")
            #Load the session variables from file
            f = open(SESSIONDIR+self.sessionid+".ses", "rb")
            self.sess = pickle.load(f)
            f.close()
            print("Loaded %s" % self.sessionid)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            #If the file doesn't exist, continue with a blank session.
            pass
    
    def set(self, arg1, arg2):
        self.sess[arg1] = arg2
    
    def read(self, arg1):
        return self.sess[arg1]
    
    def close(self):
        print("closing %s" % self.sessionid)
        if self.sessionid == None:
            #generate a new sessionid
            ids = glob.glob(SESSIONDIR+"*.ses")
            highest = 0
            if len(ids) > 0:
                highest = max([int(i[len(SESSIONDIR):-4]) for i in ids])
            self.sessionid = highest + 1
        #save the session variables back to file
        if not os.path.exists(SESSIONDIR):
            os.makedirs(SESSIONDIR)
        path = SESSIONDIR+str(self.sessionid)+".ses"
        f = open(path,"wb")
        print(f)
        print(self.sess)
        pickle.dump(self.sess, f)
        f.close()
        #set the sessionid in the user cookie
        response.set_cookie("sessionid", self.sessionid, secret=self.secret_key)
        