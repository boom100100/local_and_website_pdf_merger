cd "C:\\Program Files"
git clone https://github.com/boom100100/local_and_website_pdf_merger.git convert_and_combine_pdfs
cd convert_and_combine_pdfs

:: configure the app
copy .env.example.windows .env
copy Pipfile.windows Pipfile
copy Pipfile.lock.windows Pipfile.lock
xcopy outputs.example outputs /S /I

mkdir .venv
pipenv shell
pipenv install --python 3.11
sbase get uc_driver


if [%1]==[] exit /b 0

:: configure the native host (configure this to use the Google Chrome extension ATS Beater):
install_host.bat
