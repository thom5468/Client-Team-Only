import rpyc
import service

client = rpyc.connect("elegantgazelle.com", 55889, service.ClientService)

c = client.root

print "Games:"
for game in c.list_games["response"]["games"]:
    print game["name"]