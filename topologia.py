from mininet.topo import Topo

class NumeroInvalidoDeSwitches(Exception):
    pass


class Topologia(Topo):

    def __init__(self, n_switches=2):

        Topo.__init__(self)

        if n_switches < 1:
            raise NumeroInvalidoDeSwitches("El numero de switches debe ser mayor a 0")

        print(f"Inicializando la topología con {n_switches} switches")
        
        h1 = self.addHost('host_1')
        h2 = self.addHost('host_2')
        h3 = self.addHost('host_3')
        h4 = self.addHost('host_4')

        switches = []
        for i in range(1, n_switches + 1):
            switches.append(self.addSwitch("switch_%s" % i))

        for i in range(n_switches - 1):
            self.addLink(switches[i], switches[i + 1])

        self.addLink(h1, switches[0])
        self.addLink(h2, switches[0])
        self.addLink(h3, switches[-1])
        self.addLink(h4, switches[-1])

topos = {"topologia": Topologia}