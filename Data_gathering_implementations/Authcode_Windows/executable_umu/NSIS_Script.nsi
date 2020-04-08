;--------------------------------
!include "MUI2.nsh"
!define MUI_COMPONENTSPAGE_SMALLDESC ;No value
!define MUI_UI "${NSISDIR}\Contrib\UIs\modern.exe" ;Value
!define MUI_INSTFILESPAGE_COLORS "FFFFFF 000000" 
; The name of the installer
Name "Authcode"

; The file to write
OutFile "AuthcodeInstaller.exe"

; The default installation directory
InstallDir $PROGRAMFILES\Authcode

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------

; Pages

!insertmacro MUI_PAGE_LICENSE "Licencia.txt"
Page directory
Page instfiles

;--------------------------------

; The stuff to install
Section "" ;No components page, name is not important

  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File logger.exe
  File authcode4.ico
  Call LaunchApplication
SectionEnd ; end the section

  

Function LaunchApplication
    ExecShell "" "$INSTDIR\logger.exe" "install"
FunctionEnd