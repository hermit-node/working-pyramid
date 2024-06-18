from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
import os
import pandas as pd
from io import BytesIO

UPLOAD_DIR = 'uploads'


@view_config(route_name='home', renderer='templates/upload.html')
def home_view(request):
    return {}


@view_config(route_name='upload', request_method='POST')
def upload_view(request):
    if 'csvfile' not in request.POST:
        return HTTPFound(location='/')

    csvfile = request.POST['csvfile'].file
    filename = request.POST['csvfile'].filename
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, 'wb') as output_file:
        output_file.write(csvfile.read())

    return HTTPFound(location=f'/view?filename={filename}')


@view_config(route_name='view_csv', renderer='templates/view.html')
def view_csv(request):
    filename = request.params.get('filename')
    file_path = os.path.join(UPLOAD_DIR, filename)

    df = pd.read_csv(file_path)
    html_table = df.to_html(classes='table table-striped', index=False)

    return {'table': html_table, 'filename': filename}


@view_config(route_name='edit_csv', renderer='templates/edit.html')
def edit_csv(request):
    filename = request.params.get('filename')
    file_path = os.path.join(UPLOAD_DIR, filename)

    df = pd.read_csv(file_path)
    html_table = df.to_html(classes='table table-striped', index=False, border=0)

    return {'table': html_table, 'filename': filename}


@view_config(route_name='save_csv', request_method='POST')
def save_csv(request):
    filename = request.params.get('filename')
    file_path = os.path.join(UPLOAD_DIR, filename)

    data = request.POST.get('data')
    df = pd.read_csv(BytesIO(data.encode()))
    df.to_csv(file_path, index=False)

    return HTTPFound(location=f'/view?filename={filename}')
