import sys
import cPickle as pickle
sys.path.append('lib/')

import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
import thing

class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print data
    def Network_login(self, data):
        print "Login Started..."
        self._server.login(data['name'],data['userid'])
    def Network_moveLeft(self, data):
        self._server.moveLeft(data['userid'])
    def Network_moveRight(self, data):
        self._server.moveRight(data['userid'])
    def Network_moveUp(self, data):
        self._server.moveUp(data['userid'])
    def Network_moveDown(self, data):
        self._server.moveDown(data['userid'])
    def Network_seeThings(self, data):
        self._server.seeThings(data['userid'])

class MyServer(PodSixNet.Server.Server):
    channelClass = ClientChannel
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.users = []
        self.players = {}
        self.things = []
    def Connected(self,channel,addr):
        self.users.append(channel)
        print 'new connection:', channel
        channel.Send({'action':'getuserid','userid':self.users.index(channel)})
    def login(self, name, userid):
        print "Login Method Found..."
        channel = self.users[userid]
        player = thing.Thing((0,0), name)
        self.things.append(player)
        self.players[userid] = player
        package = pickle.dumps(player)
        data = {'action':'getplayer','package':package}
        print "Sending Login Data..."
        channel.Send(data)
        print "Send Successful"
    def update(self):
        for thing in self.things:
            thing.update()
    def moveLeft(self, userid):
        player = self.players[userid]
        player.moveLeft()
    def moveRight(self, userid):
        player = self.players[userid]
        player.moveRight()
    def moveUp(self, userid):
        player = self.players[userid]
        player.moveUp()
    def moveDown(self, userid):
        player = self.players[userid]
        player.moveDown()
    def seeThings(self, userid):
        channel = self.users[userid]
        package = pickle.dumps({'player':self.players[userid],'things':self.things})
        data = {'action':'recThings','package':package}
        channel.Send(data)

print "STARTING SERVER ON LOCALHOST"
s = MyServer(localaddr=("localhost",4001))
while True:
    s.update()
    s.Pump()
    sleep(0.01)
