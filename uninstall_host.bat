:: %~dp0 is the directory containing this bat script and ends with a backslash.
REG DELETE "HKCU\Software\Google\Chrome\NativeMessagingHosts\com.automatedbooks.convert_and_combine_pdfs"

:: trigger chrome extension uninstallation
REG DELETE HKLM\SOFTWARE\Policies\Google\Chrome\ExtensionInstallForcelist
