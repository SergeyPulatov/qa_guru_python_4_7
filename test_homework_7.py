import zipfile
import shutil
import os
import pytest
import pandas as pd
from PyPDF2 import PdfReader


@pytest.fixture
def test_making_zip():
    new_zip = zipfile.ZipFile('files.zip', 'w')
    new_zip.write('username.csv')
    new_zip.write('file_example_XLS_10.xls')
    new_zip.write('docs-pytest-org-en-latest.pdf')
    new_zip.close()
    shutil.move(os.getcwd() + '/files.zip',  os.getcwd() + '/resources' + '/files.zip')
    yield
    os.remove(os.getcwd() + '/resources' + '/files.zip')

def test_csv(test_making_zip):
    with zipfile.ZipFile(os.getcwd() + '/resources' + '/files.zip', 'r') as my_zip:
        csv_file = my_zip.open('username.csv')
        check_csv_file_length_lines = len(csv_file.readlines())
        assert check_csv_file_length_lines == 6
def test_xls(test_making_zip):
    with zipfile.ZipFile(os.getcwd() + '/resources' + '/files.zip', 'r') as my_zip:
        xlx_file = my_zip.open('file_example_XLS_10.xls')
        xlx_read = pd.read_excel(xlx_file)
        check_first_name = xlx_read.at[4, 'First Name']
        assert check_first_name == 'Nereida'

def test_pdf(test_making_zip):
    with zipfile.ZipFile(os.getcwd() + '/resources' + '/files.zip', 'r') as my_zip:
        pdf_file = PdfReader(my_zip.open('docs-pytest-org-en-latest.pdf'))
        pdf_check_page = pdf_file.pages[5].extract_text()
        assert pdf_check_page == 'pytest Documentation, Release 0.1\n2 CONTENTS'










