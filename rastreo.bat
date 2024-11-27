@echo off
setlocal


set proceso=opera
set "intervalo=5"
set "archivo_tiempo=tiempo_acumulado.txt"

if exist "%archivo_tiempo%" (
    set /p tiempo_total=<"%archivo_tiempo%"
) else (
    set /a tiempo_total=0
)

:inicio
tasklist | findstr /i "%proceso%" >nul
if %errorlevel%==0 (
    set /a tiempo_total+=intervalo
    echo El proceso %proceso% está en ejecución. Tiempo acumulado: %tiempo_total% segundos.
    echo %tiempo_total% > "%archivo_tiempo%"
) else (
    echo El proceso %proceso% no está en ejecución.
)

timeout /t %intervalo% >nul
goto inicio



