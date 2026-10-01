[Setup]
AppName=Sinhala Keyboard
AppVersion=1.0
DefaultDirName={autopf}\SinhalaKeyboard
DefaultGroupName=Sinhala Keyboard
OutputDir=output
OutputBaseFilename=SinhalaKeyboard_Setup
Compression=lzma
SolidCompression=yes
InfoBeforeFile=key_guide.txt

[Files]
Source: "dist\SinhalaKeyboard.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "key_guide.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Sinhala Keyboard"; Filename: "{app}\SinhalaKeyboard.exe"
Name: "{autodesktop}\Sinhala Keyboard"; Filename: "{app}\SinhalaKeyboard.exe"
Name: "{autoprograms}\Sinhala Keyboard Key Guide"; Filename: "{app}\key_guide.txt"

[Run]
Filename: "{app}\SinhalaKeyboard.exe"; Description: "Launch Sinhala Keyboard now"; Flags: nowait postinstall skipifsilent
