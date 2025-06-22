; Script de exemplo do Inno Setup para o Gestor de Alunos

; Defina a raiz do projeto ao compilar usando
;   /DSourceRoot=<caminho do repositório>
; Este parâmetro é obrigatório para localizar os arquivos
#ifndef SourceRoot
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
