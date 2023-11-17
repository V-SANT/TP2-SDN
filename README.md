# TP2-SDN

Para ejecutar la topología, primero se debe levantar el controlador.

## Para levantar POX utilizando el controlador sin firewall

```shell
    sudo python3 pox.py log.level --DEBUG log.color openflow.of_01 forwarding.l2_learning
```

## Para levantar POX utilizando el controlador con una serie de reglas y el id del switch al cual aplicar las reglas para actuar como firewall

```shell
sudo python3 pox.py log.level --DEBUG log.color openflow.of_01 forwarding.l2_learning firewall --path_reglas="path_archivo_reglas" --switch_id= id_switch_a_aplicar_reglas
```

Luego se lanza la topología

## Para lanzar la topología
```shell
sudo mn --custom ./topologia.py --topo topologia,n_switches=nro_de_switches --mac --arp --switch ovsk --controller remote
```







