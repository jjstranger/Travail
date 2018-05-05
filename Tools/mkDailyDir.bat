set dailyPath = d:/Daily/
set currentDate =echo %Date:~0,4%%Date:~5,2%%Date:~8,2%
if not exist %dailyPath%%currentDate% md %dailyPath%%currentDate%
echo %dailyPath%
echo %currentDate%
pause
