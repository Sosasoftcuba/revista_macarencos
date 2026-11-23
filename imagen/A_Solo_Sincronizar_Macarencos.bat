@echo off
title Sincronizador Rapido (Solo Web) - Revista Macarencos
color 0B
cd /d "%~dp0"

:: ============================================================
:: Sincronizador para el repositorio: revista_macarencos
:: Version SIN PROXY (para usar desde una conexion directa,
:: sin el proxy de la universidad).
::
:: ANTES DE USARLO:
::   1. Revoca el token viejo (ghp_Duwl... que quedo expuesto)
::      en https://github.com/settings/tokens
::   2. Crea un token NUEVO con scope "repo"
::   3. Reemplaza PON_AQUI_TU_NUEVO_TOKEN mas abajo por ese token
::
:: Si la carpeta del repo no se llama "revista_macarencos" o no
:: esta un nivel arriba de donde pusiste este .bat, ajusta la
:: linea "cd ..\revista_macarencos" de abajo.
:: ============================================================

:: Subir un nivel (salir de la carpeta donde esta este .bat)
:: y entrar a la carpeta del repositorio
cd ..\revista_macarencos

echo ====================================================
echo    INICIANDO ACTUALIZACION RAPIDA (SOLO WEB)...
echo    Revista Macarencos - SIN PROXY
echo ====================================================
echo.

:: 0. Quitar cualquier proxy configurado antes
::    (por si se ejecuto el otro script que si usa proxy)
git config --global --unset http.proxy >nul 2>&1
git config --global --unset https.proxy >nul 2>&1

:: Evitar que Git se quede colgado pidiendo contrasenas
set GIT_TERMINAL_PROMPT=0

:: 1. Asegurar el repositorio CON EL TOKEN INTEGRADO
::    (reemplaza PON_AQUI_TU_NUEVO_TOKEN por tu token nuevo)
git remote set-url origin https://PON_AQUI_TU_NUEVO_TOKEN@github.com/Sosasoftcuba/revista_macarencos.git

:: 2. Preparar y guardar los cambios del HTML
echo [!] Preparando archivos para subir...
git add .
git commit -m "Actualizacion rapida de HTML" >nul 2>&1

:: 3. Subir a GitHub FORZANDO LA SOBRESCRITURA
echo [!] Sobrescribiendo archivos en GitHub...
set intentos=1
:reintentar_push
git push origin main --force
if %errorlevel% equ 0 goto push_exitoso

if %intentos% lss 3 (
    echo.
    echo [AVISO] El push fallo. Reintentando en 5 segundos... (Intento %intentos% de 3)
    timeout /t 5 /nobreak >nul
    set /a intentos+=1
    goto reintentar_push
)

color 0C
echo.
echo ====================================================
echo [ERROR] Hubo un problema al subir los archivos tras 3 intentos.
echo Revisa tu conexion a internet o el token de GitHub.
echo ====================================================
pause
exit /b

:push_exitoso
color 0A
echo.
echo ====================================================
echo    PROCESO TERMINADO CORRECTAMENTE
echo    Tu pagina web en GitHub ha sido actualizada.
echo    (Recuerda presionar Ctrl+F5 en tu navegador)
echo ====================================================
echo.
pause
