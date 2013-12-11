import rpyc
import service

client = rpyc.connect("elegantgazelle.com", 55889, service.ClientService, config = {"allow_public_attrs" : True})

c = client.root

#print "Games:"
#for game in c.list_games()["response"]["games"]:
#    print game["name"]
def startgame():
    c.start_game("test1", "bob1")
    
def getstuff(values):
    if values.count('p') > 0:
        print c.get_state(object_type="Planet")["response"]["planet"]
    if values.count('e') > 0:
        print c.get_state(object_type="Environ")["response"]["environ"]
    if values.count('c') > 0:
        print c.get_state(object_type="Character")["response"]["character"]
    if values.count('u') > 0:
        print c.get_state(object_type="Unit")["response"]["unit"]
    if values.count('s') > 0:
        print c.get_state(object_type="Stack")["response"]["stack"]