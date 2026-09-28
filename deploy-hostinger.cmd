@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0deploy-hostinger.ps1" %*
