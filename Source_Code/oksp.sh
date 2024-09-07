#!/bin/bash

read -r -a entrada <<< $(cat params.txt)

mydir=${entrada[0]}
directorio_eqt=${entrada[1]}
directorio_origen=${entrada[2]}
directorio_ondas=${entrada[3]}
stations=${entrada[4]}
ano=${entrada[5]}
start_day=${entrada[6]}
end_day=${entrada[7]}



#echo "Ingrese el directorio de OKSP"
#mydir=$1

#echo "Ingrese el directorio de EQT:"
#read directorio_eqt
#directorio_eqt=$2

#echo "Ingrese el directorio base del Experimento:"
#read directorio_origen
#directorio_origen=$3

#echo "Ingrese el directorio de las ondas del Experimento:"
#read directorio_ondas
#directorio_ondas=$4

#echo "Ingrese el año a analizar:"
#read ano
#ano=$5

#echo "Ingrese el día inicial: "
#read start_day
#start_day=$6

#echo "Ingrese el día final: "
#read end_day
#end_day=$7

for i in $(seq $start_day $end_day); do
    dir_org=$directorio_origen/"$ano-$i"
    mkdir -p $dir_org
    cp "$mydir/run.sh" $dir_org
    cd $dir_org
    ./run.sh $mydir $directorio_eqt $dir_org $directorio_ondas $ano $i $directorio_origen $stations > salida_$i.txt &
    cd $mydir
    wait
done
