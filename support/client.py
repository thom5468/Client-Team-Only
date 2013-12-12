import rpyc
import service

client = rpyc.connect("elegantgazelle.com", 55889, service.ClientService, config = {"allow_public_attrs" : True})

c = client.root

#print "Games:"
#for game in c.list_games()["response"]["games"]:
#    print game["name"]
def startgame():
    c.start_game("test1", "bob1")
    
def getstuff(value):
    if value == 'p':
        return c.get_state('test1', "Planet")["response"]["planet"]
    if value == 'e':
        return c.get_state('test1',"Environ")["response"]["environ"]
    if value == 'c':
        return c.get_state('test1', "Character")["response"]["character"]
    if value == 'u':
        return c.get_state('test1', "Unit")["response"]["unit"]
    if value == 's':
        return c.get_state('test1', "Stack")["response"]["stack"]

envs = getstuff('e')
planets = getstuff('p')
chars = getstuff('c')
units = getstuff('u')
stacks = getstuff('s')

def printthings(itemlist):
    for thing in itemlist:
        for item in thing.items():
            print item
        print "-------------------"
            
def printids (itemlist):
    for thing in itemlist:
        print thing["id"]
        
def move( stack, location ):
    return c.move(game_id ='test1', stack_id = stack, location_id = location)