; Inno Setup script for Resolume Composition Converter
; Builds an installer from the already-generated dist/windows package.

#ifndef AppName
  #define AppName "Resolume Composition Converter"
#endif
#ifndef AppVersion
  #define AppVersion "0.0.0-dev"
#endif
#ifndef AppPublisher
  #define AppPublisher "Tijn Schuurmans"
#endif
#ifndef AppExeName
  #define AppExeName "Resolume Composition Converter.exe"
#endif
#ifndef SourceDir
  #define SourceDir "..\..\dist\windows\Resolume Composition Converter"
#endif
#ifndef OutputDir
  #define OutputDir "..\..\dist\windows\installer"
#endif

[Setup]
AppId={{E09E3666-FEAB-4FCA-8DF9-19DB0FAAF740}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
LicenseFile=..\..\LICENSE
OutputDir={#OutputDir}
OutputBaseFilename=Resolume-Composition-Converter-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#AppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
