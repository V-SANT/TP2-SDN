from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent.revent import *
from pox.lib.util import dpidToStr
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
from pox.lib.addresses import EthAddr, IPAddr
import json

ERROR = -1


def guardar_reglas(path):
    try:
        with open(path) as archivo:
            reglas = json.load(archivo)
        return reglas
    except Exception:
        log.error("Error al leer el archivo de reglas")
        exit(ERROR)


log = core.getLogger()

#Si no se especifica un switch para que actúe como Firewall, se usa como default el 1
firewall_switch_id = 1

reglas = {"reglas": []}


class Firewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Habilitando el Firewall")

    def _handle_PacketIn(self, evento):
        pass   

    def _handle_ConnectionUp(self, evento):
        if evento.dpid == firewall_switch_id:
            for regla in reglas["reglas"]:
                mensaje = of.ofp_flow_mod()
                self.aplicar_regla(mensaje, regla)
                evento.connection.send(mensaje)
            log.debug(
                "Reglas de Firewall instaladas en %s - switch %i",
                dpidToStr(evento.dpid),
                firewall_switch_id,
            )

    def aplicar_regla(self, mensaje, regla):

        mensaje.match.dl_type = ethernet.IP_TYPE
        print(regla)
        for clave, valor in regla.items():
            
            if clave == "src_ip":
                log.debug("Regla instalada: droppeando paquete proveniente de dirección IP %s", valor)
                mensaje.match.nw_src = IPAddr(valor)
            elif clave == "dst_ip":
                log.debug("Regla instalada: droppeando paquete con dirección IP destino %s", valor)
                mensaje.match.nw_dst = IPAddr(valor)
            elif clave == "src_port":
                log.debug("Regla instalada: droppeando paquete proveniente de puerto %i", valor)
                mensaje.match.tp_src = valor
            elif clave == "dst_port":
                log.debug("Regla instalada: droppeando paquete con puerto de destino %i", valor)
                mensaje.match.tp_dst = valor
            elif clave == "src_mac":
                log.debug("Regla instalada: droppeando paquete proveniente de dirección MAC %s", valor)
                mensaje.match.dl_src = EthAddr(valor)
            elif clave == "dst_mac":
                log.debug("Regla instalada: droppeando paquete con dirección MAC destino %s", valor)
                mensaje.match.dl_dst = EthAddr(valor)
            elif clave == "protocol" and valor == "tcp":
                log.debug("Regla instalada: droppeando paquete TCP")
                mensaje.match.nw_proto = ipv4.TCP_PROTOCOL
            elif clave == "protocol" and valor == "udp":
                log.debug("Regla instalada: droppeando paquete UDP")
                mensaje.match.nw_proto = ipv4.UDP_PROTOCOL


def launch(path_reglas, switch_id=1):
    if int(switch_id) < 1:
        log.error("Switch ID invalido")
        exit(ERROR)
    global firewall_switch_id
    global reglas
    data = guardar_reglas(path_reglas)
    reglas = data
    log.debug("Reglas cargadas:\n" + str(reglas))
    firewall_switch_id = int(switch_id)
    core.registerNew(Firewall)