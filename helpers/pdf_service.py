import os
from flask import Response
from helpers.tablepdf import TableContentParser as Parser, Runner


def generate_pdf_response(keys, table_data, file_name='report', output_extension='.pdf', is_attachment=True,
                          directory_name='files'):
    mkdir_if_not_exists(directory_name)
    remove_if_exists(directory_name, file_name)
    parse_data(directory_name, file_name, keys, table_data)
    # create pdf
    Runner().run(file_name, orientation='landscape')
    output_path = os.path.join(os.getcwd(), f'\\{directory_name}\\{file_name}{output_extension}')
    return return_file_data(file_name, is_attachment, output_extension, output_path)


def return_file_data(file_name, is_attachment, output_extension, output_path):
    if os.path.exists(output_path):
        try:
            with open(output_path, 'rb') as f:
                response = Response(f.read(), mimetype='application/pdf')
                if is_attachment:
                    response.headers['Content-Disposition'] = f'attachment; filename={file_name}{output_extension}'
                else:
                    response.headers['Content-Disposition'] = f'inline; filename={file_name}{output_extension}'
                return response
        except OSError as e:
            print(f'error reading file {e}')
    else:
        print(f'file {output_path} does not exist')
    return "no_data_found"


def parse_data(directory_name, file_name, keys, table_data):
    print(table_data)
    parser = Parser(file_name, file_directory_name=directory_name)
    data = []
    for entry in table_data:
        for i, value in enumerate(entry.values()):
            data.append(str(value))
    parser.putKeysAndValues(keys, data)
    parser.parse()


def remove_if_exists(directory_name, file_name):
    path = os.path.join(os.getcwd(), f'\\{directory_name}\\{file_name}.txt')
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError as e:
            print(f'error deleting file {e}')
    else:
        print(f'file {path} does not exist')


def mkdir_if_not_exists(directory_name):
    if not os.path.exists(f'\\{directory_name}'):
        os.makedirs(f'\\{directory_name}')
