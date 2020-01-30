@echo off


set BASE_DIR=%cd%

echo.
echo Cleaning sandbox...
echo.
cd %BASE_DIR%\..
IF EXIST .\obj attrib -R .\obj\*.* /S
IF EXIST .\src attrib -R .\src\*.* /S

echo Cleaning files ...
IF EXIST .\obj del /F /S /Q .\obj
IF EXIST .\src del /F /S /Q .\src

echo.
echo Sandbox cleaned !
echo.
PAUSE

cd %BASE_DIR%
REM Determines previous sandbox derivate
if exist 2MCurrent (
	set CURRENT_DERIVATE=2M
	del 2MCurrent
) else if exist 6MCurrent (
	set CURRENT_DERIVATE=6M
	del 6MCurrent
) else if exist notestCurrent (
	set CURRENT_DERIVATE=notest
	del notestCurrent
REM Default version is 4M
) else (
	set CURRENT_DERIVATE=4M
	del 4MCurrent
)

echo.
echo Transitioning from %CURRENT_DERIVATE% to %TARGET_DERIVATE%...
echo.


echo . > %TARGET_DERIVATE%Current

if "%CURRENT_DERIVATE%" NEQ "%TARGET_DERIVATE%" (
 	forfiles /P .. /S /M *.%CURRENT_DERIVATE% /C "cmd /c echo Saving %CURRENT_DERIVATE% file : @fname ... & attrib -R @fname.%CURRENT_DERIVATE% & copy @fname @fname.%CURRENT_DERIVATE%"
	forfiles /P .. /S /M *.%TARGET_DERIVATE% /C "cmd /c echo Saving %CURRENT_DERIVATE% file : @fname ... & attrib -R @fname.%CURRENT_DERIVATE% & copy @fname @fname.%CURRENT_DERIVATE%"
	forfiles /P .. /S /M *.4M /C "cmd /c echo Restoring 4M default file : @file ... & attrib -R @fname & copy @file @fname"
	forfiles /P .. /S /M *.%TARGET_DERIVATE% /C "cmd /c echo Setting %TARGET_DERIVATE% file : @file ... & attrib -R @fname & copy @file @fname"
	echo.
	echo Updating Ideas...
	echo.
	call .\..\etools\TsStarter.cmd update

	echo.
	echo Updating Cessar-CT...
	echo.
	call .\..\etools\TsStarter.cmd CessarUpdater -pdr

	echo.
	echo Transition %TARGET_DERIVATE% done !
	echo.
) else (
	echo.
	echo Already on %CURRENT_DERIVATE%, nothing to transition !
	echo.
)
PAUSE