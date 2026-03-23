@echo off
"C:\users\muhammad shan\appdata\local\programs\python\python310\python.exe" manage.py makemigrations attendance
"C:\users\muhammad shan\appdata\local\programs\python\python310\python.exe" manage.py migrate
echo.
echo Migrations complete!
pause
