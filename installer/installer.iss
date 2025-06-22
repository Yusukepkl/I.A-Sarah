; Script de exemplo do Inno Setup para o Gestor de Alunos

; Caminho padrao do projeto. Pode ser sobrescrito ao compilar com /DSourceRoot=...
#ifndef SourceRoot
#define SourceRoot "C:\\Users\\jhona\\Documents\\GitHub\\I.A-Sarah"
#endif

[Setup]
AppName=Gestor de Alunos
AppVersion=0.1.0
DefaultDirName={pf}\GestorAlunos
OutputBaseFilename=GestorAlunosSetup

[Files]
Source: "{#SourceRoot}\dist\gestor-alunos.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceRoot}\scripts\setup_data.ps1"; DestDir: "{app}"; Flags: ignoreversion

[Run]
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File \"{app}\setup_data.ps1\""; Flags: runhidden
