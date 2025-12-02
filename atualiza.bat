@echo off
REM ===== CONFIGURAÇÕES =====
set FRONTEND_DIR=C:\Users\User\ABNT\frontend
set SERVER_USER=root
set SERVER_HOST=69.6.222.172
set SERVER_PORT=22022
set SERVER_FRONTEND_PATH=/var/www/abntx_frontend

echo ============================================
echo   DEPLOY ABNTX - FRONTEND + BACKEND
echo ============================================
echo.

REM ===== FRONTEND: BUILD =====
echo [1/3] Indo para pasta do frontend: %FRONTEND_DIR%
cd /d "%FRONTEND_DIR%" || (
    echo ERRO: Nao consegui acessar %FRONTEND_DIR%
    pause
    exit /b 1
)

echo [2/3] Instalando dependencias (npm install)...
npm install
if errorlevel 1 (
    echo ERRO no npm install
    pause
    exit /b 1
)

echo [3/3] Gerando build (npm run build)...
npm run build
if errorlevel 1 (
    echo ERRO no npm run build
    pause
    exit /b 1
)

if not exist "%FRONTEND_DIR%\dist" (
    echo ERRO: pasta dist nao encontrada apos o build.
    pause
    exit /b 1
)

echo.
echo ===== ENVIANDO BUILD PARA O SERVIDOR =====
scp -P %SERVER_PORT% -r dist/* %SERVER_USER%@%SERVER_HOST%:%SERVER_FRONTEND_PATH%
if errorlevel 1 (
    echo ERRO ao enviar arquivos via scp.
    pause
    exit /b 1
)

echo.
echo ===== ATUALIZANDO BACKEND NO SERVIDOR =====
ssh -p %SERVER_PORT% %SERVER_USER%@%SERVER_HOST% "/root/deploy_abntx.sh"
if errorlevel 1 (
    echo ERRO ao executar deploy_abntx.sh no servidor.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   DEPLOY CONCLUIDO COM SUCESSO! 🎉
echo   Site: https://abntx.com.br
echo ============================================
pause
