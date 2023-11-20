# TP2-SDN

Para ejecutar la topología, primero se debe levantar el controlador.

### Para levantar POX utilizando el controlador sin firewall

```shell
sudo python3 pox.py log.level --DEBUG log.color openflow.of_01 forwarding.l2_learning
```

### Para levantar POX utilizando el controlador con una serie de reglas y el id del switch al cual aplicar las reglas para actuar como firewall

```shell
sudo python3 pox.py log.level --DEBUG log.color openflow.of_01 forwarding.l2_learning firewall --path_reglas="path_archivo_reglas" --switch_id= id_switch_a_aplicar_reglas
```

Luego se lanza la topología

### Para lanzar la topología
```shell
sudo mn --custom ./topologia.py --topo topologia,n_switches=nro_de_switches --mac --arp --switch ovsk --controller remote
```

### Para probar las simulaciones

Primero se deben dar los permisos correspondientes:

```shell
chmod +x ./scripts/*
```
Luego se deben ejecutar los comandos mencionados anteriormente para utilizar el controlador POX y levantar la topología.

#### Para probar la simulación con la regla de bloqueo dst_port: 80

Estando en la terminal de mininet, ejecutar:

```shell
./scripts/xterm.sh host_2 host_4
```

Luego, ejecutar el comando de iperf para el server en la terminal correspondiente:
```shell
./scripts/server.sh 80
# OR
./scripts/server.sh 80 -u
```
La opción de -u corresponde a si se quiere establecer utilizando el protocolo UDP. Por default, utiliza el protocolo TCP.

Por último, se debe ejecutar en la terminal correspondiente el comando de iperf para el cliente con el parámetro de la ip del servidor a conectarse:

```shell
./scripts/client.sh 10.0.0.x 80
# OR
./scripts/client.sh 10.0.0.x 80 -u
```

#### Para probar la simulación con la regla de bloqueo dst_port: 5001, protocol: UDP y proveniente del host 1

Estando en la terminal de mininet, ejecutar:

```shell
./scripts/xterm.sh host_1 host_2
```

Luego, ejecutar los comandos de iperf (el server en el host_2 y el client en el host_1):
```shell
./scripts/server.sh 5001
# OR
./scripts/server.sh 5001 -u
```

```shell
./scripts/client.sh 10.0.0.2 5001
# OR
./scripts/client.sh 10.0.0.2 5001 -u
```

#### Para probar la simulación con la regla de impedir la comunicación entre dos hosts:

##### Para probar la comunicación para un lado:

Estando en la terminal de mininet, ejecutar:

```shell
./scripts/xterm.sh host_1 host_3
```

Luego, ejecutar los comandos de iperf (server en el host_1 y client en el host_3):

```shell
./scripts/server.sh <port>
# OR
./scripts/server.sh <port> -u
```

```shell
./scripts/client.sh 10.0.0.1 <port>
# OR
./scripts/client.sh 10.0.0.1 <port> -u
```

##### Para probar la comunicación en el otro sentido:

Estando en la terminal de mininet, ejecutar:

```shell
./scripts/xterm.sh host_1 host_3
```

Luego, ejecutar los comandos de iperf (server en el host_3 y client en el host_1):

```shell
./scripts/server.sh <port>
# OR
./scripts/server.sh <port> -u
```

```shell
./scripts/client.sh 10.0.0.3 <port>
# OR
./scripts/client.sh 10.0.0.3 <port> -u
```













