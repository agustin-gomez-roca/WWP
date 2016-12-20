# Guarda en un array los usuarios logueados.
usuarios_sunray=( $(/opt/SUNWut/bin/utwho |awk '{print $3}') )
usuarios_iptables=( $(/sbin/iptables -t nat -L |awk '/SNAT/ {print $9}') )

echo "SunRay: ${usuarios_sunray[@]}"
echo "IPTables: ${usuarios_iptables[@]}"
exit

for user in ${usuarios_sunray[@]}
do
# /opt/SUNWut/bin/utwho |\
# while read term id user
# do
#	usuarios_sunray=($usuarios_sunray $user)
	rango=$(iptables -t nat -L | awk -v user=$user '/SNAT/ && ($0 ~ user) { print $NF }')
	if [ "$rango" != "" ]
	then
		puertos=$(echo $rango |cut -f3 -d: )
	else
		puertos="No tiene asignado un rango de puertos en iptables"
	fi
	echo "$puertos $user"
done |sort -n
