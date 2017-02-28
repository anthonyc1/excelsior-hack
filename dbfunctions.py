
from database import Database


import sqlite3
import os
import glob

__all__ = ['AuthDatabase']


class AuthDatabase(Database):

    def getPosts(self):
        return self._execute('SELECT * FROM Posts')


    def insertPost(self,title,post):
        self._execute('INSERT INTO Posts(postTitle, post) VALUES (?,?);',(title,post))

    #########################################


    def auth_user(self, name, password):
        
        password = self.Str2id(password)
        if bool(self._execute('SELECT * FROM Users WHERE username=? AND password=?',(name, password))):
            if not name in team:
                self._execute('INSERT INTO Logins(userID,time) values (?,?)',(self.usernameToID(name),time()))
            return True;

    def auth_admin(self, name, password):
        if name == "shaansweb" or name == "mobinsheikh" or name == "sami":
            return self.auth_user(name,password)
        return False

    def validNewUsername(self, name):
        return not bool(self._execute('SELECT * FROM users WHERE username=?',(name,)))

    def validNewEmail(self, email):
        return not bool(self._execute('SELECT * FROM users WHERE email=?',(email,)))

    def uniNameToNum(self, uni):
        results = self._execute('SELECT * FROM Universities WHERE name=?',(uni,))
        if len(results) > 0:
            return results[0][0]
        else:
            return 0

    def uniNumToName(self,uniID):
        results = self._execute('SELECT * FROM Universities WHERE universityID=?',(uniID,))
        if len(results) > 0:
            return results[0][1]
        else:
            return 0

    def getUnis(self):
        return self._execute('SELECT * FROM Universities')

    def getUni(self,uniID):
        return self._execute('SELECT * FROM Universities WHERE universityID=?',(uniID,))


    def uniNameToEmail(self, uni):
        results = self._execute('SELECT * FROM Universities WHERE name=?',(uni,))[0][2]
        return results

    def uniNumToEmail(self, uni):
        results = self._execute('SELECT * FROM Universities WHERE universityID=?',(uni,))[0][2]
        return results

    def validEmail(self, email, uni):
        results = self._execute('SELECT * FROM Universities WHERE universityID=?',(uni,))[0][2]
        return email[email.find('@')+1:] == results

    def delUser(self, username):
        self._execute('DELETE FROM Users WHERE username=?',(username,))

    def getPostNum(self):
        posts = self._execute('SELECT * FROM Posts')
        return posts[-1][0] + 1

    def add_user(self, username, password, email, uni):
        if self.validNewUsername(username):
            if self.validNewEmail(email):
                if uni > 0:
                    if self.validEmail(email,uni):
                        if len(password) > 5:
                            self._execute('INSERT INTO Users(username,password,email,uniID,pkarma,ckarma) values(?,?,?,?,0,0)',(username,self.Str2id(password),email,uni))
                            return 0
                        else:
                            return 5
                    else:
                        return 4
                else:
                    return 3
            else:
                return 2
        else:
            return 1



    def getSubjects(self,uniID):
        return self._execute('SELECT * FROM Subjects WHERE uniID=? ORDER BY name',(uniID,))

    def getSubj(self,subjectID):
        return self._execute('SELECT * FROM Subjects WHERE subjectID=?',(subjectID,))[0]

    def getCoursesBySub(self, subjectnum):
        return self._execute('SELECT * FROM Courses WHERE subjectID=? ORDER BY LOWER(Code)',(subjectnum,))

    def getCoursesByUni(self, uniid):
        return self._execute('SELECT * FROM Courses WHERE uniID=? ORDER BY LOWER(Code)' ,(uniid,))

    def getPostsByProf(self, profnum):
        return self._execute('SELECT * FROM Posts WHERE professorID=?',(profnum,))

    def getPostsByCourse(self, coursenum):
        return self._execute('SELECT * FROM Posts WHERE courseID=?',(coursenum,))

    def getPostsBySubj(self, subjnum):
        return self._execute('SELECT * FROM posts INNER JOIN courses ON posts.courseID = courses.courseID WHERE subjectID=?;',(subjnum,))

    def getPostsByAuthor(self,userID):
        pass

    def getProfsByUni(self, uniid):
        return self._execute('SELECT * FROM Profs WHERE uniID=? ORDER BY Name COLLATE NOCASE',(uniid,))

    def userToUni(self, username):
        return self._execute('SELECT uniID FROM Users WHERE username=?',(username,))[0][0]

    def usernameToID(self,username):
        return self._execute('SELECT userID FROM Users WHERE username=?',(username,))[0][0]

    def addNote(self, extension, courseID, userID, profID, title,pages):
        return self._execute('INSERT INTO Posts (post, ups, downs, excellents, terribles, time, courseID, userID, professorID,title,pages) VALUES(?,0,0,0,0,?,?,?,?,?,?)',(extension,time(),courseID,userID,profID,title,pages))

    def getPost(self, postnum):
        posts = self._execute('SELECT * FROM Posts where postID=?',(postnum,))
        if len(posts) > 0:
            return self._execute('SELECT * FROM Posts where postID=?',(postnum,))[0]
        else:
            return [-1]

    def getAllPosts(self):
        return self._execute('SELECT * FROM Posts')

    def getUser(self,userID):
        return self._execute('SELECT * FROM Users WHERE userID=?',(userID,))[0]

    def getCourse(self,courseID):
        return self._execute('SELECT * FROM Courses WHERE courseID=?',(courseID,))[0]

    def getProf(self,profID):
        return self._execute('SELECT * FROM Profs WHERE profID=?',(profID,))[0]

    def addProf(self,name,uniID):
        return self._execute('INSERT INTO Profs (name,uniID) VALUES (?,?)',(name,uniID))

    def delNote(self, noteid,username):
        try:
            if self.getPost(noteid)[7] == self.usernameToID(username) or username=="shaansweb":
                for file in glob.glob('uploads/' + str(noteid)+"-*"):
                    os.remove(file)
                self._execute('DELETE FROM Posts where postID=?',(noteid,))
                return "deleted"
            else:
                return "autherror" #autherror
        except IndexError:
            return "dne" #notedne

    def addCourse(self, name, code, subjectID):

        self._execute('INSERT INTO Courses(name,code,subjectID,uniID) values(?,?,?,?)',(name,code,subjectID,self.getSubj(subjectID)[2]))

    def addSubj(self,name,uniID):
        self._execute('INSERT INTO Subjects(name,uniID) VALUES(?,?)',(name,uniID))

    def getPostsFiltered(self,courseID,subjectID,profID):
        if courseID > -1 and subjectID > -1 and profID > -1:
            return self._execute('SELECT * FROM posts INNER JOIN courses ON posts.courseID = courses.courseID WHERE subjectID=? AND posts.courseID=? AND professorID=?;',(subjectID,courseID,profID))
        elif courseID > -1 and subjectID > -1:
            return self._execute('SELECT * FROM posts INNER JOIN courses ON posts.courseID = courses.courseID WHERE subjectID=? AND posts.courseID=?;',(subjectID,courseID))
        elif courseID > -1 and profID > -1:
            return self._execute('SELECT * FROM Posts WHERE courseID=? AND professorID',(coursenum,profID))
        elif subjectID > -1 and profID > -1:
            return self._execute('SELECT * FROM posts INNER JOIN courses ON posts.courseID = courses.courseID WHERE subjectID=? AND professorID=?;',(subjectID,profID))
        elif subjectID > -1:
            return self._execute('SELECT * FROM posts INNER JOIN courses ON posts.courseID = courses.courseID WHERE subjectID=?;',(subjectID,))
        elif profID > -1:
            return self._execute('SELECT * FROM Posts WHERE professorID=?',(profID,))
        elif courseID > -1:
            return self._execute('SELECT * FROM Posts WHERE courseID=?',(courseID,))
        else:
            return self.getAllPosts()

    def getVotes(self, userID):
         return self._execute('SELECT * FROM Votes WHERE userID=?',(userID,))

    def addComment(self, parentID, userID, comment):
        return self._execute('INSERT INTO Comments(comment,parentID,userID,time,ups,downs) VALUES(?,?,?,?,0,0)',(comment,parentID,userID,time()))

    def getCommentsByParent(self,parentID):
        return self._execute('SELECT * FROM Comments WHERE parentID=?',(parentID,))

    def getScore(self,targetID,ptype):
        score = 0
        votes = self._execute('SELECT * FROM Votes WHERE targetID=?',(targetID,))
        if ptype:
            for vote in votes:
                if vote[2]==5:
                    score = score-5
                elif vote[2]==6:
                    score = score-2
                elif vote[2]==7:
                    score=score+2
                elif vote[2]==8:
                    score=score+5
        else:
            for vote in votes:
                if vote[2]==4:
                    score = score+5
                elif vote[2]==3:
                    score=score+2
                elif vote[2]==2:
                    score=score-2
                elif vote[2]==1:
                    score=score-5
        return score

    def getVote(self,userID,targetID):
        vote = 0
        if len(self._execute('SELECT * FROM Votes WHERE userID=? AND targetID=?',(userID,targetID))) > 0:
            vote = self._execute('SELECT * FROM Votes WHERE userID=? AND targetID=?',(userID,targetID))[0][2]
        return vote

    def vote(self,targetID,userID,vote):
        if len(self._execute('SELECT * FROM Votes WHERE userID=? AND targetID=?',(userID,targetID))) > 0:
            self.devote(userID,targetID)
        self._execute("INSERT INTO Votes(userID,vote,targetID) VALUES(?,?,?)",(userID,vote,targetID))

    def devote(self,userID,targetID):
        self._execute("DELETE FROM Votes WHERE userID=? AND targetID=?",(userID,targetID))

    def getUsers(self):
        return self._execute("SELECT * FROM Users");

    def getKarma(self,userID):
        votes = self._execute("SELECT vote,posts.userID from Votes, Posts where votes.targetID = Posts.postID and Posts.userID=?",(userID,))
        total = 0
        for vote in votes:
            if vote[0] == 8:
                total=total+5
            elif vote[0] == 7:
                total=total+2
            elif vote[0] == 6:
                total=total-2
            elif vote[0]==5:
                total=total-5
        return total

    def getIP(self,userID):
        rewards = self._execute("SELECT * FROM Rewards WHERE userID=?",(userID,))
        return 10*len(rewards) + 5*len(self.getReferrals(userID))

    def getLastLogin(self,userID):
        logins = self._execute("SELECT * FROM Logins WHERE userID=?",(userID,))
        if len(logins) > 0:
            return logins[-1][2]
        return ""

    #REWARDS

    def fiveDays(self,userID):
        if len(self._execute("SELECT * FROM Rewards WHERE userID=? and reward=1",(userID,))) > 0:
            return -1
        logins = self._execute("SELECT * FROM Logins WHERE userID=?",(userID,))
        index = -1
        days = 1
        run = True
        curr1 = timeparse(logins[index][2]).date()
        while (days < 5 and run):
            newcurr = timeparse(logins[index][2]).date()
            if (curr1 - newcurr).days > 1:
                run = False
            elif (curr1 - newcurr).days == 1:
                days = days + 1
            index = index - 1
            curr1 = newcurr
        if days == 5:
            self._execute("INSERT INTO Rewards(userID, reward) VALUES(?,1)",(userID,))
        return days

    def tenComments(self,userID):
        if len(self._execute("SELECT * FROM Rewards WHERE userID=? and reward=2",(userID,))) > 0:
            return 11
        comments = len(self._execute("SELECT * FROM Comments WHERE userID=?",(userID,)))
        if comments >= 10:
            self._execute("INSERT INTO Rewards(userID, reward) VALUES(?,2)",(userID,))
            return 10
        else:
            return comments

    def fivePosts(self,userID):
        if len(self._execute("SELECT * FROM Rewards WHERE userID=? and reward=3",(userID,))) > 0:
            return 6
        posts = self._execute("SELECT * FROM Posts WHERE userID=?",(userID,))
        if len(posts) >= 5:
            self._execute("INSERT INTO Rewards(userID, reward) VALUES(?,3)",(userID,))
            return 5
        return len(posts)

    def addReferral(self, newuserID, code):
        if len(code) > 0 and code[0] == "r":
            referrerID = (int(code[1:],16)-597)/2
            if len(self._execute("SELECT * FROM Users WHERE userID=?",(referrerID,))) > 0 and len(self._execute("SELECT * FROM Referrals WHERE newuserID=?",(newuserID,))) == 0:
                self._execute("INSERT INTO Referrals(newuserID,referrerID) VALUES(?,?)",(newuserID,referrerID))
            else:
                print "failed"
                print self._execute("SELECT * FROM Users WHERE userID=?",(referrerID,))
                print self._execute("SELECT * FROM Referrals WHERE newuserID=?",(newuserID,))

    def getReferrals(self,referrerID):
        return self._execute("SELECT * FROM Referrals WHERE referrerID=?",(referrerID,))

def time():
    time = datetime.now().isoformat()[:-7]
    return time

def consecutiveDates(date1,date2):
    diff = diff(date1,date2)
    if diff == "less":
        return 0
    elif diff == "1 day ago":
        return 1
    else:
        return 2

def diff(date1,date2):
    timein =date1
    timenow = date2
    timeinA = timein[:timein.find("-")]
    timein = timein[timein.find("-")+1:]
    timenowA = timenow[:timenow.find("-")]
    timenow = timenow[timenow.find("-")+1:]
    if timeinA != timenowA:
        diff = int(timenowA)-int(timeinA)
        if diff == 1:
            return str(diff) + " year ago"
        else:
            return str(diff) + " years ago"
    timeinA = timein[:timein.find("-")]
    timein = timein[timein.find("-")+1:]
    timenowA = timenow[:timenow.find("-")]
    timenow = timenow[timenow.find("-")+1:]
    if timeinA != timenowA:
        diff = int(timenowA)-int(timeinA)
        if diff == 1:
            return str(diff) + " month ago"
        else:
            return str(diff) + " months ago"
    timeinA = timein[:timein.find("T")]
    timein = timein[timein.find("T")+1:]
    timenowA = timenow[:timenow.find("T")]
    timenow = timenow[timenow.find("T")+1:]
    if timeinA != timenowA:
        diff = int(timenowA)-int(timeinA)
        if diff == 1:
            return "1 day ago"
        else:
            return str(diff) + " days ago"
    return "less"

def timeparse(timein):
    return datetime.strptime(timein,"%Y-%m-%dT%H:%M:%S")

