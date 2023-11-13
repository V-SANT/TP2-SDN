from mininet.topo import Topo

class NumeroInvalidoDeSwitches(Exception):
    pass


class Topologia(Topo):

    def __init__(self, n_switches=2):

        #Inicializa la topologia
        Topo.__init__(self)

        if n_switches < 1:
            raise NumeroInvalidoDeSwitches("El numero de switches debe ser mayor a 0")

        print("Inicializando la topología con %s switches" % (n_switches))
        hosts = []

        # Se agregan los 4 hosts (2 para cada extremo)
        for i in range(1, 5):
            hosts.append(self.addHost("host_%s" % i))

        # Se agregan los switches
        switches = []
        for i in range(1, n_switches + 1):
            switches.append(self.addSwitch("switch_%s" % i))

        # Se conectan los switches entre si
        for i in range(n_switches - 1):
            self.addLink(switches[i], switches[i + 1])

        # Se conectan los hosts a los switches correspondientes
        self.addLink(hosts[0], switches[0])
        self.addLink(hosts[1], switches[0])
        self.addLink(hosts[2], switches[-1])
        self.addLink(hosts[3], switches[-1])


topos = {"topologia": Topologia}