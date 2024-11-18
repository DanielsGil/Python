#!/bin/bash

proceso=firefox
intervalo=5
archivo_tiempo="tiempo_acumulado.txt"

# Verificar si el archivo de tiempo acumulado existe
if [ -f "$archivo_tiempo" ]; then
    tiempo_total=$(cat "$archivo_tiempo")
else
    tiempo_total=0
fi

while true; do
    # Comprobar si el proceso está en ejecución
    if pgrep -i "$proceso" > /dev/null; then
        tiempo_total=$((tiempo_total + intervalo))
        echo "El proceso $proceso está en ejecución. Tiempo acumulado: $tiempo_total segundos."
        echo $tiempo_total > "$archivo_tiempo"
    else
        echo "El proceso $proceso no está en ejecución."
    fi

    # Esperar el intervalo
    sleep $intervalo
done

