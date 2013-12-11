import rpyc
import service

client = rpyc.connect("elegantgazelle.com", 55889, service.ClientService, config = {"allow_public_attrs" : True})

c = client.root

#print "Games:"
#for game in c.list_games()["response"]["games"]:
#    print game["name"]

c.start_game("test1", "bob1")
    
planets = c.get_state(object_type="Planet")["response"]["Planet"]
environs = c.get_state(object_type="Environ")["response"]["Environ"]
characters = c.get_state(object_type="Character")["response"]["Character"]
units = c.get_state(object_type="Unit")["response"]["Unit"]