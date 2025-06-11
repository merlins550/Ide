@echo off
echo Conference Room - LLM Chain Automation Platform baslatiliyor...
echo.

REM Gerekli paketlerin kurulu olup olmadigini kontrol et
python -c "import customtkinter, PIL, darkdetect" 2>nul
if errorlevel 1 (
    echo Gerekli paketler kuruluyor...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo HATA: Paket kurulumu basarisiz!
        pause
        exit /b 1
    )
)

REM Ana uygulamayi baslat
python main.py
if errorlevel 1 (
    echo HATA: Uygulama baslatilirken hata olustu!
    pause
    exit /b 1
)

pause
