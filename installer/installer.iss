; Script de exemplo do Inno Setup para o Gestor de Alunos
[Setup]
AppName=Gestor de Alunos
AppVersion=0.1.0
DefaultDirName={pf}\GestorAlunos
OutputBaseFilename=GestorAlunosSetup

[Files]
Source: "dist\gestor-alunos.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "scripts\setup_data.ps1"; DestDir: "{app}"; Flags: ignoreversion

[Run]
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File \"{app}\setup_data.ps1\""; Flags: runhidden
