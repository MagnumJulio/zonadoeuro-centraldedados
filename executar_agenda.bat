@echo off
REM Caminho até o seu ambiente virtual
set VENV_PATH=D:\Impactus\Projetos-Impactus\pyimpactus\meu-dashboard1\meu-dashboard1\envimpactus

REM Ativa o ambiente virtual (Windows)
call "%VENV_PATH%\Scripts\activate"

REM Verifica se a ativação funcionou
if errorlevel 1 (
    echo ❌ Erro ao ativar o ambiente virtual.
    pause
    exit /b
)

REM Executa cada script listado no agenda.txt
for /f "delims=" %%a in (agenda.txt) do (
    echo Executando %%a...
    python "%%a"
    if errorlevel 1 (
        echo ⚠️ Erro ao executar %%a
    ) else (
        echo ✅ %%a executado com sucesso.
    )
)

REM Desativa o ambiente virtual ao final
call deactivate

pause
