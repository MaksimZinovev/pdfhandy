from datetime import datetime
import logging
from os import rename, chdir, remove, path
from pathlib import Path
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
import pytest
import time


UTILS_PATH = path.abspath(__file__)
PROJ_DIR = Path(UTILS_PATH).parents[1]

@pytest.fixture
def current_test_num(cache):
    key = 'test_number'
    if cache.get(key, 0) == 0:
        cache.set(key, 1)
        test_num = 0
    else:
        test_num = cache.get(key, None) + 1
        cache.set(key, test_num)
    return test_num


# @pytest.fixture
# def pdf_factory2():
#     def _pdf_factory(node, current_test_num,
#                       count=1,
#                       folder='data',        # Default folder: project_dir/data
#                       testid_filename='test_id.pdf',
#                       base_files=('contract_template.pdf',),
#                       fname_template='Test_pdf_',
#                       archive_num=2):
#
#         # Generate one-page pdf with test number and  unique text (test number, date/time, node)
#         def get_testid_pdf(node_, folder_, testid_filename_, fname_template_, count_):
#
#             now = datetime.now()
#             test_time = now.strftime("%Y-%m-%d / %H:%M:%S")
#             file = Path(PROJ_DIR/folder_/testid_filename_)      # PROJ_DIR defined in project_dir/tests/conftest.py
#             c = canvas.Canvas(str(file))
#             pdf_num = str(count_)
#             pdf_name = f"{fname_template_}{current_test_num:0>4d}_{pdf_num}"
#             test_name_time = f"[{pdf_name}] - [{test_time}]"
#             test_caller = f"[{node_}]"
#             c.drawString(100,750, test_name_time)
#             c.drawString(100,720, test_caller)
#             c.save()
#             return
#
#         # Merge one-page file with multi-page base pdf file(s)
#         def write_merged_pdf(base_files_, folder_, testid_filename_, fname_template_, count_):
#             pdf_writer = PdfFileWriter()
#             merging_files = [testid_filename_] + list(base_files_)
#             for file in merging_files:
#                 file_path = Path(PROJ_DIR/folder_/file)
#                 path = open(file_path, "rb")
#                 pdf_reader = PdfFileReader(path)
#                 for page in range(pdf_reader.getNumPages()):
#                     # Add each page to the writer object
#                     pdf_writer.addPage(pdf_reader.getPage(page))
#             # Write out the merged PDF
#             pdf_num = str(count_)
#             merged_file_path = Path(PROJ_DIR / folder_ / f"{fname_template_}{current_test_num:0>4d}_{pdf_num}.pdf")
#             with open(merged_file_path, 'wb') as out:
#                 pdf_writer.write(out)
#             return merged_file_path
#
#         # Rename files, delete unwanted files using parameter 'archive_num_'
#         def cleanup(folder_, fname_template_, archive_num_):
#
#             # get list of files using fname_template
#             path = Path(PROJ_DIR/folder_)
#             pdf_list = path.glob(f'{fname_template_}*.pdf')
#
#             # rename archived files prefix '_'
#             chdir(Path(PROJ_DIR / folder_))
#             for file in pdf_list:
#                 rename(file.name, '_' + file.name)
#
#             # get updated list archived files and sort it
#             archive_list = [file.name for file in path.glob(f'_{fname_template_}*.pdf')]
#             archive_list.sort()
#
#             # delete unwanted files (oldest) according to archive_num parameter
#             if archive_num_ < len(archive_list):
#                 slice_ = len(archive_list) - archive_num_
#             else:
#                 slice_ = 0
#
#             delete_list = archive_list[:slice_]
#             for file in delete_list:
#                 remove(Path(PROJ_DIR / folder_ / file))
#
#         def pdf_paths(pdf_dir, name_template):
#             return pdf_dir.glob(f'{name_template}*.pdf')
#
#
#         # _pdf_factory body
#         cleanup(folder, fname_template, archive_num)
#         pdf_path = 'empty'
#         for k in range(1, count+1):
#             get_testid_pdf(node, folder, testid_filename, fname_template, k)
#             pdf_path = write_merged_pdf(base_files, folder, testid_filename, fname_template, k)
#         if count == 1:
#             return pdf_path
#         else:
#             # TODO Question for stackoverflow.com: How to sort file paths in generator?
#             return pdf_paths(Path(PROJ_DIR / folder), fname_template)
#             # TODO Is it possible to use yield here so cleanup is executed after test finished, not before?
#             # yield
#             # cleanup(folder, fname_template, archive_num)
#
#     return _pdf_factory

@pytest.fixture
def pdf_factory():
    def _pdf_factory(node, current_test_num,
                      count=1,
                      folder='data',        # Default folder: project_dir/data
                      testid_filename='test_id.pdf',
                      base_files=('contract_template.pdf',),
                      fname_template='Test_pdf_',
                      archive_num=2):

        # Generate one-page pdf with test number and  unique text (test number, date/time, node)
        def get_testid_pdf(node_, folder_, testid_filename_, fname_template_, count_):

            now = datetime.now()
            test_time = datetime.now().strftime("%Y-%m-%d / %H:%M:%S")

            file = Path(PROJ_DIR/folder_/testid_filename_)      # PROJ_DIR defined in project_dir/tests/conftest.py
            c = canvas.Canvas(str(file))
            pdf_num = str(count_)
            pdf_name = f"{fname_template_}{current_test_num:0>4d}_{pdf_num}"
            test_name_time = f"[{pdf_name}] - [{test_time}]"
            test_caller = f"[{node_}]"
            c.drawString(100,750, test_name_time)
            c.drawString(100,720, test_caller)
            c.save()

            # Create PDF object
            pdf = PDF()
            pdf.file_num = f'{current_test_num:0>4d}_{pdf_num}'
            pdf.file_name = f'{fname_template_}{current_test_num:0>4d}_{pdf_num}.pdf'

            pdf.file_date = now.date()
            pdf.file_time = now.time()
            pdf.file_dt = now
            pdf.file_tzoffset = -1*time.altzone/3600

            logging.info(f'pdf.file_num: {pdf.file_num}')
            logging.info(f'pdf.file_name: {pdf.file_name}')
            logging.info(f'pdf.file_date: {pdf.file_date}')
            logging.info(f'pdf.file_time: {pdf.file_time}')
            logging.info(f'pdf.file_tzoffset: {pdf.file_tzoffset}')
            return pdf


        # Merge one-page file with multi-page base pdf file(s)
        def write_merged_pdf(base_files_, folder_, testid_filename_, fname_template_, count_):
            pdf_writer = PdfFileWriter()
            merging_files = [testid_filename_] + list(base_files_)
            for file in merging_files:
                path_ = open(Path(PROJ_DIR/folder_/file), "rb")
                pdf_reader = PdfFileReader(path_)
                for page in range(pdf_reader.getNumPages()):
                    # Add each page to the writer object
                    pdf_writer.addPage(pdf_reader.getPage(page))
            # Write out the merged PDF
            pdf_num = str(count_)
            merged_file_path = Path(PROJ_DIR / folder_ / f"{fname_template_}{current_test_num:0>4d}_{pdf_num}.pdf")
            with open(merged_file_path, 'wb') as out:
                pdf_writer.write(out)

            fsize = int(path.getsize(merged_file_path)/1024)
            return merged_file_path, fsize

        # Rename files, delete unwanted files using parameter 'archive_num_'
        def cleanup(folder_, fname_template_, archive_num_):

            # get list of files using fname_template
            path = Path(PROJ_DIR/folder_)
            pdf_list = path.glob(f'{fname_template_}*.pdf')

            # rename archived files prefix '_'
            chdir(Path(PROJ_DIR / folder_))
            for file in pdf_list:
                rename(file.name, '_' + file.name)

            # get updated list archived files and sort it
            archive_list = [file.name for file in path.glob(f'_{fname_template_}*.pdf')]
            archive_list.sort()

            # delete unwanted files (oldest) according to archive_num parameter
            if archive_num_ < len(archive_list):
                slice_ = len(archive_list) - archive_num_
            else:
                slice_ = 0

            delete_list = archive_list[:slice_]
            for file in delete_list:
                remove(Path(PROJ_DIR / folder_ / file))

        # def pdf_paths(pdf_dir, name_template):
        #     return pdf_dir.glob(f'{name_template}*.pdf')


        # _pdf_factory body
        pdf_list = []
        pdf = PDF()

        cleanup(folder, fname_template, archive_num)
        for k in range(1, count+1):
            pdf = get_testid_pdf(node, folder, testid_filename, fname_template, k)
            pdf.file_path, pdf.file_size = write_merged_pdf(base_files, folder, testid_filename, fname_template, k)
            pdf_list.append(pdf)
        return pdf if count == 1 else pdf_list
        # if count == 1:
        #     return pdf
        # else:
        #     # TODO Question for stackoverflow.com: How to sort file paths in generator?
        #     return pdf_list
        #     # TODO Is it possible to use yield here so cleanup is executed after test finished, not before?
        #     # yield
        #     # cleanup(folder, fname_template, archive_num)

    return _pdf_factory



class PDF:
    file_path = None
    file_name = None
    file_dt = None
    file_date = None
    file_time = None
    file_num = None
    file_pages = None
    file_size = None
    file_tzoffset = None


def test_pdf_factory(request, current_test_num, pdf_factory):
    source = None
    for source in pdf_factory(request.node.nodeid, current_test_num, count=1):
        logging.info(f'\n{source }')
        time.sleep(5)
        pass
    logging.info(f'Result: \n{source }')


def test_pdf_factory_final(request, current_test_num, pdf_factory):
    source = None
    for source in pdf_factory(request.node.nodeid, current_test_num, count=1):
        pdf_list = pdf_loader(source)
        logging.info(f'\nPDF loaded: {pdf_list[0]}')
        pdf_obj = PDF(pdf_list[0])
        logging.info(f"\nGenerated pdf object (filename): {pdf_obj.file_name}")
        logging.info(f"\nGenerated pdf object (filepath): {pdf_obj.file_path}")
        time.sleep(5)

    logging.info(f'Source tuple: \n{source}')


def test_pdf_loader2(request, current_test_num, pdf_factory):

    pdf = pdf_factory(request.node.nodeid, current_test_num, count=1)
    pdf_file = (next(pdf))
    pdf_obj = PDF(pdf_file)
    logging.info(f"\nGenerated pdf object (filename): {pdf_obj.file_name}")
    logging.info(f"\nGenerated pdf object (filepath): {pdf_obj.file_path}")
    next(pdf, None)


def test_pdf_factory_single(request, current_test_num, pdf_factory):
    pdf_path = pdf_factory(request.node.nodeid, current_test_num, count=1)
    logging.info(f'Single path: \n{pdf_path}')



def test_pdf_factory_multiple(request, current_test_num, pdf_factory):
    pdf_paths = pdf_factory(request.node.nodeid, current_test_num, count=3)
    for path in pdf_paths:
        logging.info(f'Multiple pdf generated: \n{path}')


def test_pdf_factory2_single(request, current_test_num, pdf_factory):
    pdf_obj = pdf_factory(request.node.nodeid, current_test_num, count=1)
    logging.info(f'file_path: \n{pdf_obj.file_path}')
    logging.info(f'file_size: \n{pdf_obj.file_size}')

def test_pdf_factory_multiple(request, current_test_num, pdf_factory):
    pdfs = pdf_factory(request.node.nodeid, current_test_num, count=8)
    for k, pdf_obj in enumerate(pdfs):
        logging.info(f'ITERATION: {k}')
        logging.info(f'file_date: {pdf_obj.file_date}')
        logging.info(f'file_path: {pdf_obj.file_path}')
        logging.info(f'file_size: {pdf_obj.file_size}')
        logging.info(f'file_name: {pdf_obj.file_name}')

