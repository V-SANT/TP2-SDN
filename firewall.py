from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent.revent import *
from pox.lib.util import dpidToStr
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
from pox.lib.addresses import EthAddr, IPAddr
import json

ERROR = -1

class NumeroInvalidoDeSwitch(Exception):
    pass
class LecturaIncorrectaDeReglas(Exception):
    pass

def guardar_reglas(path):
    try:
        with open(path) as archivo:
            reglas = json.load(archivo)
        return reglas
    except Exception:
        log.error("Error al leer el archivo de reglas")
        raise LecturaIncorrectaDeReglas("Error al leer el archivo de reglas")

log = core.getLogger()
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
            log.debug(f"Reglas de Firewall instaladas en {dpidToStr(evento.dpid)} switch {firewall_switch_id}")

    def aplicar_regla_data_link(self, mensaje, clave, valor):
        if clave == "src_mac":
            log.debug(f"Regla instalada: droppeando paquete proveniente de dirección MAC {valor}")
            mensaje.match.dl_src = EthAddr(valor)
        elif clave == "dst_mac":
            log.debug(f"Regla instalada: droppeando paquete con dirección MAC destino {valor}")
            mensaje.match.dl_dst = EthAddr(valor)

    def aplicar_regla_network(self, mensaje, clave, valor):
        if clave == "src_ip":
            log.debug(f"Regla instalada: droppeando paquete proveniente de dirección IP {valor}")
            mensaje.match.nw_src = IPAddr(valor)
        elif clave == "dst_ip":
            log.debug(f"Regla instalada: droppeando paquete con dirección IP destino {valor}")
            mensaje.match.nw_dst = IPAddr(valor)
        elif clave == "src_port":
            log.debug(f"Regla instalada: droppeando paquete proveniente de puerto {valor}")
            mensaje.match.tp_src = valor
        elif clave == "dst_port":
            log.debug(f"Regla instalada: droppeando paquete con puerto de destino {valor}")
            mensaje.match.tp_dst = valor

    def aplicar_regla_transporte(self, mensaje, clave, valor):
        if clave == "protocol" and valor == "tcp":
            log.debug("Regla instalada: droppeando paquete TCP")
            mensaje.match.nw_proto = ipv4.TCP_PROTOCOL
        elif clave == "protocol" and valor == "udp":
            log.debug("Regla instalada: droppeando paquete UDP")
            mensaje.match.nw_proto = ipv4.UDP_PROTOCOL

    def aplicar_regla(self, mensaje, regla):
        mensaje.match.dl_type = ethernet.IP_TYPE

        for clave, valor in regla.items():
            if clave in ["src_mac", "dst_mac"]:
                self.aplicar_regla_data_link(mensaje, clave, valor)
            elif clave in ["src_ip", "dst_ip", "src_port", "dst_port"]:
                self.aplicar_regla_network(mensaje, clave, valor)
            elif clave in ["protocol"]:
                self.aplicar_regla_transporte(mensaje, clave, valor)




def launch(path_reglas, switch_id=1):
    id_switch = int(switch_id)
    if id_switch < 1:
        log.error("Switch ID invalido")
        raise NumeroInvalidoDeSwitch("El ID del switch debe ser mayor a 0")
    global firewall_switch_id
    global reglas
    reglas_a_aplicar = guardar_reglas(path_reglas)
    reglas = reglas_a_aplicar
    log.debug("Reglas:\n" + str(reglas))
    firewall_switch_id = id_switch
    core.registerNew(Firewall)