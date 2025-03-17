:: Copyright 2014 The Chromium Authors. All rights reserved.
:: Use of this source code is governed by a BSD-style license that can be
:: found in the LICENSE file.

cp "%~dp0com.automatedbooks.convert_and_combine_pdfs.json.windows" "%~dp0com.automatedbooks.convert_and_combine_pdfs.json"
rm "%~dp0com.automatedbooks.convert_and_combine_pdfs.json.windows"

:: Change HKCU to HKLM if you want to install globally.
:: %~dp0 is the directory containing this bat script and ends with a backslash.
REG ADD "HKCU\Software\Google\Chrome\NativeMessagingHosts\com.automatedbooks.convert_and_combine_pdfs" /ve /t REG_SZ /d "%~dp0com.automatedbooks.convert_and_combine_pdfs.json" /f
