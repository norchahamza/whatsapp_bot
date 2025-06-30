@echo off
setlocal enabledelayedexpansion
title 🚀 WhatsApp Bot Launcher

REM === Vérification de l'environnement ===
if not exist "whatsapp_bot_env\Scripts\activate.bat" (
    echo ❌ Environnement virtuel introuvable.
    pause
    exit /b 1
)

echo.
echo ============================
echo ⚙️ Activation de l'environnement virtuel...
echo ============================
call whatsapp_bot_env\Scripts\activate.bat || (
    echo ❌ Échec de l'activation.
    pause
    exit /b 1
)

echo.
echo ============================
echo 🧹 Nettoyage du dataset...
echo ============================
python -m scripts.clean_dataset || (
    echo ❌ Échec du nettoyage.
    pause
    exit /b 1
)

echo.
echo ============================
echo 🧠 Entraînement du modèle de réponse...
echo ============================
python -m app.train_bot || (
    echo ❌ Échec entraînement chatbot.
    pause
    exit /b 1
)

echo.
echo ============================
echo 🧠 Entraînement classifieur d’intention...
echo ============================
python -m app.utils.intent_trainer || (
    echo ❌ Échec entraînement intention.
    pause
    exit /b 1
)

echo.
echo ============================
echo 🚀 Lancement du bot WhatsApp...
echo ============================
python -m app.main || (
    echo ❌ Échec lancement Flask.
    pause
    exit /b 1
)

endlocal
pause
echo.
echo ============================
echo ✅ Bot WhatsApp lancé avec succès !
echo ============================
