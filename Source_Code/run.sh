#!/usr/bin/env bash
# Trabajo Final de Graduación Ing.Electrónica
#Sebastián Gamboa Chacón - 2017142512
#Ejecución del Pipeline OKSP

inicio=$(date +%s.%N)

#echo "Ingrese el directorio de EQT:"
#read directorio_eqt
mydir=$1

#echo "Ingrese el directorio de EQT:"
#read directorio_eqt
directorio_eqt=$2

#echo "Ingrese el directorio base del Experimento:"
#read directorio_origen
directorio_origen=$3

#echo "Ingrese el directorio de las ondas del Experimento:"
#read directorio_ondas
directorio_ondas=$4

#echo "Ingrese el año a analizar:"
#read ano
ano=$5

#echo "Ingrese el día a analizar:"
#read dia
dia=$6

dir=$7

stations=$8

conuno=$(($dia+1))

mkdir -p "$directorio_origen"

cp "$stations/stations.csv" "$directorio_origen"

mkdir -p "$directorio_origen"/LOGS
mkdir -p "$directorio_origen"/LOGS/deconv_logs
mkdir -p "$directorio_origen"/LOGS/trans_logs
mkdir -p "$directorio_origen"/LOGS/db2eqt_logs
mkdir -p "$directorio_origen"/LOGS/det_logs
mkdir -p "$directorio_origen"/LOGS/aso_logs
mkdir -p "$directorio_origen"/LOGS/location_logs
mkdir -p "$directorio_origen"/LOGS/events_logs
mkdir -p "$directorio_origen"/LOGS/mag_logs
mkdir -p "$directorio_origen"/LOGS/plot_logs
mkdir -p "$directorio_origen"/LOGS/catalog_logs

#Generando archivos sh de deconvolución en el directorio base
sed "s#directorio_origen#$directorio_origen#g" "$mydir/deconvolution.sh" > "$directorio_origen/deconvolution.sh"
sed -i "s#mydir#"$mydir"#g" "$directorio_origen/deconvolution.sh"
sed -i "s#stations_dir#"$stations"#g" "$directorio_origen/deconvolution.sh"
sed -i "s#directorio_ondas#$directorio_ondas#g" "$directorio_origen/deconvolution.sh"
sed -i "s#ano#$ano#g" "$directorio_origen/deconvolution.sh"
sed -i "s#dia#$dia#g" "$directorio_origen/deconvolution.sh"
chmod +x "$directorio_origen/deconvolution.sh"
#Generando archivos sh de transferencia en el directorio base
sed "s#directorio_origen#$directorio_origen#g" "$mydir/transferencia.sh" > "$directorio_origen/transferencia.sh"
sed -i "s#mydir#"$mydir"#g" "$directorio_origen/transferencia.sh"
sed -i "s#directorio_ondas#$directorio_ondas#g" "$directorio_origen/transferencia.sh"
sed -i "s#ano#$ano#g" "$directorio_origen/transferencia.sh"
sed -i "s#dia#$dia#g" "$directorio_origen/transferencia.sh"
sed -i "s#conuno#$conuno#g" "$directorio_origen/transferencia.sh"
chmod +x "$directorio_origen/transferencia.sh"

#Generando archivo sh db2eqt en el directorio base
sed "s#directorio_origen#$directorio_origen#g" "$mydir/db2eqt.sh" > "$directorio_origen/db2eqt.sh"
sed -i "s#mydir#"$mydir"#g" "$directorio_origen/db2eqt.sh"
sed -i "s#ano#$ano#g" "$directorio_origen/db2eqt.sh"
sed -i "s#dia#$dia#g" "$directorio_origen/db2eqt.sh"
sed -i "s#conuno#$conuno#g" "$directorio_origen/db2eqt.sh"
chmod +x "$directorio_origen/db2eqt.sh"

#Generando archivo sh detección en el directorio base
sed "s#directorio_origen#$directorio_origen#g" "$mydir/deteccion.sh" > "$directorio_origen/deteccion.sh"
sed -i "s#mydir#"$mydir"#g" "$directorio_origen/deteccion.sh"
sed -i "s#directorio_eqt#$directorio_eqt#g" "$directorio_origen/deteccion.sh"
chmod +x "$directorio_origen/deteccion.sh"

#Generando archivo sh asociación en el directorio base
YYYYMMDD=$(python3 "$mydir/ajuste_asociacion.py" "$dia" "$ano")
YYYYMMDE=$(python3 "$mydir/ajuste_asociacion.py" "$conuno" "$ano")
sed "s#directorio_origen#$directorio_origen#g" "$mydir/asociacion.sh" > "$directorio_origen/asociacion.sh"
sed -i "s#mydir#$mydir#g" "$directorio_origen/asociacion.sh"
sed -i "s#YYYY-MM-DD#$YYYYMMDD#g" "$directorio_origen/asociacion.sh"
sed -i "s#YYYY-MM-D+#$YYYYMMDE#g" "$directorio_origen/asociacion.sh"
sed -i "s#directorio_eqt#$directorio_eqt#g" "$directorio_origen/asociacion.sh"
chmod +x "$directorio_origen/asociacion.sh"

#Generando archivo sh localización en el directorio base
sed "s#directorio_origen#$directorio_origen#g" "$mydir/localizar.sh" > "$directorio_origen/localizar.sh"
sed -i "s#mydir#"$mydir"#g" "$directorio_origen/localizar.sh"
chmod +x "$directorio_origen/localizar.sh"

#Generando archivo sh eventos en el directorio base
sed "s#directorio_origen#$directorio_origen#g" "$mydir/events.sh" > "$directorio_origen/events.sh"
sed -i "s#mydir#"$mydir"#g" "$directorio_origen/events.sh"
chmod +x "$directorio_origen/events.sh"

#Generando archivo sh eventos en el directorio base
sed "s#directorio_origen#$directorio_origen#g" "$mydir/magnitud.sh" > "$directorio_origen/magnitud.sh"
sed -i "s#mydir#"$mydir"#g" "$directorio_origen/magnitud.sh"
chmod +x "$directorio_origen/magnitud.sh"

#Generando archivo sh plots en el directorio base
sed "s#directorio_origen#$directorio_origen#g" "$mydir/plot.sh" > "$directorio_origen/plot.sh"
sed -i "s#mydir#"$mydir"#g" "$directorio_origen/plot.sh"
sed -i "s#ano#"$ano"#g" "$directorio_origen/plot.sh"
sed -i "s#dia#"$dia"#g" "$directorio_origen/plot.sh"
chmod +x "$directorio_origen/plot.sh"

#Generando archivos sh de catalogo en el directorio base
sed "s#directorio_origen#$directorio_origen#g" "$mydir/catalog.sh" > "$directorio_origen/catalog.sh"
sed -i "s#mydir#"$mydir"#g" "$directorio_origen/catalog.sh"
sed -i "s#dir#$dir#g" "$directorio_origen/catalog.sh"
sed -i "s#ano#$ano#g" "$directorio_origen/catalog.sh"
sed -i "s#dia#$dia#g" "$directorio_origen/catalog.sh"
chmod +x "$directorio_origen/catalog.sh"

echo "------ Ejecutando Transferencia -------"
ini_trans=$(date +%s.%N)
#$directorio_origen/deconvolution.sh
#wait
$directorio_origen/transferencia.sh
wait
$directorio_origen/db2eqt.sh
wait
t_trans=$(date +%s.%N)
trans=$(echo "$t_trans - $ini_trans" | bc)
echo "La transmisión tardó $trans segundos en ejecutarse."
echo "------ Transferencia Finalizada -------"

echo "------ Ejecutando la detección -------"
ini_det=$(date +%s.%N)
$directorio_origen/deteccion.sh
wait
t_det=$(date +%s.%N)
det=$(echo "$t_det - $ini_det" | bc)
echo "La detección tardó $det segundos en ejecutarse."
echo "------ Detección Finalizada -------"

echo "------ Ejecutando la asociacion -------"
ini_aso=$(date +%s.%N)
#$directorio_origen/asociacion.sh
wait
t_aso=$(date +%s.%N)
aso=$(echo "$t_aso - $ini_aso" | bc)
echo "La asociación tardó $aso segundos en ejecutarse."
echo "------ Asociación Finalizada -------"

echo "------ Ejecutando la localización -------"
ini_loc=$(date +%s.%N)
#$directorio_origen/localizar.sh
wait
t_loc=$(date +%s.%N)
loc=$(echo "$t_loc - $ini_loc" | bc)
echo "La localización tardó $loc segundos en ejecutarse."
#cp "$directorio_origen"/LOCATION/4_LOC/OKSP.sum.hypo_ell "$directorio_origen"/LOCATION/"Catalogo-$ano-$dia.hypo_ell"
echo "------ Detección Finalizada -------"

echo "------ Ejecutando la descomposición en eventos -------"
ini_events=$(date +%s.%N)
#$directorio_origen/events.sh
wait
#$directorio_origen/magnitud.sh
wait
t_events=$(date +%s.%N)
events=$(echo "$t_events - $ini_events" | bc)
echo "La descomposición de eventos tardó $events segundos en ejecutarse."
echo "------ Descomposición en eventos Finalizada -------"

echo "------ Ejecutando la generación del Plot -------"
ini_plot=$(date +%s.%N)
#$directorio_origen/plot.sh
wait
t_plot=$(date +%s.%N)
plot=$(echo "$t_plot - $ini_plot" | bc)
echo "La descomposición de eventos tardó $plot segundos en ejecutarse."
echo "------ Generación del Plot Finalizada -------"

echo "------ Ejecutando la generación del catálogo -------"
ini_catalog=$(date +%s.%N)
#$directorio_origen/catalog.sh
wait
t_catalog=$(date +%s.%N)
catalog=$(echo "$t_catalog - $ini_catalog" | bc)
echo "La descomposición de eventos tardó $catalog segundos en ejecutarse."
echo "------ Generación del catálogo Finalizada -------"


fin=$(date +%s.%N)

duracion=$(echo "$fin - $inicio" | bc)
echo "El script total tardó $duracion segundos en ejecutarse."
