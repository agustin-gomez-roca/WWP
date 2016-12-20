# WWP
En memoria de Ezequiel Bernasconi 8 de julio de 1993 - 29 de Noviembre de 2016

https://drive.google.com/open?id=0Bz5ykwxqS9lBak1TX1hsbXRCR00

Working With Ports

Este proyecto fue iniciado por Ezequiel Bernasconi y Mantenido por los administradores de SunRay/ThinLinc
El objetivo es permitir al usuario la navegación sin proxy y mantener la trazabilidad del mismo a traves del PaloAlto.

Para ello se capturan los eventos de Login/Logout del usuario y se ejecutan diferentes scripts según el evento:

Login:
Se ejecuta el portsassignation.py
Le envía al PaloAlto el username, la IP del server y un rango de puertos por los que el usuario saldra a internet por medio de las XML-API del PA.

En el server el usuario queda "atado" a ese rango de puertos mediante el siguiente comando de iptables:

commandiptable = "/sbin/iptables -t nat -A POSTROUTING -m owner --uid-owner " + blankusername +  " -p tcp -j SNAT --to-source " + self.serveripc + ":" + str(inicialportf) + "-" + str(inicialportf+199)

Logout:
Se ejecuta el freeingports.py
Le envía al PaloAlto el username para liberar el rango de puertos asociado al mismo
Libera el rango de puertos en el iptables del servidor con el siguiente comando:

commandiptable = '/sbin/iptables -t nat -D POSTROUTING $(/sbin/iptables -t nat -L --line-numbers |awk -v rango="' + str(inicialportf2) + '-' + str(inicialportf2+199) + '"' + " '($NF ~ rango) {print $1}')"

Internamente mantiene en un archivo binario (tipo pickle) la info de los puertos asignados a cada usuario.
Este archivo se modifica en cada evento de login/logout

Reset:
Se ejecuta el creationports.py
Este script corre durante la noche cuando ya no quedan mas usuarios (por ejemplo como parte del killall.sh) para liberar cualquier rango de puertos que pudiera haber quedado ocupado tanto en el PA como en el iptables.
Re-genera el arhivo pickle vacío. 
