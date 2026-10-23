@echo off
title SGLT2 Virtual Screening App Installer
echo =======================================================
echo Persiapan Lingkungan SGLT2 Drug Discovery App
echo =======================================================
echo.
echo Sedang menginstal pustaka yang dibutuhkan (harap tunggu)...
pip install -r requirements.txt

echo.
echo Membuka aplikasi di browser...
streamlit run app.py

pause
