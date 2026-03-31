; Inno Setup Script for UR Dashboard Monitor
; Compile this with Inno Setup 6 (https://jrsoftware.org/isinfo.php)
; Run: iscc installer.iss   (from the URDash project root)
;
; Prerequisites: Build the app first with:
;   pyinstaller dashboard_monitor.spec
;
; This will produce: dist/dashboard_monitor/ folder
; The installer bundles that entire folder.

#define MyAppName "UR Dashboard Monitor"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "ISCAR"
#define MyAppExeName "dashboard_monitor.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer_output
OutputBaseFilename=URDashboardMonitor_Setup_{#MyAppVersion}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Bundle the entire PyInstaller onedir output
Source: "dist\dashboard_monitor\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(#MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
