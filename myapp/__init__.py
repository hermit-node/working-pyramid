from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from wsgiref.simple_server import make_server
import os
import pandas as pd
from io import BytesIO

UPLOAD_DIR = '../uploads'

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


# Views
@view_config(route_name='home', renderer='templates/upload.jinja2')
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


@view_config(route_name='view_csv', renderer='templates/view.jinja2')
def view_csv(request):
    filename = request.params.get('filename')
    file_path = os.path.join(UPLOAD_DIR, filename)

    df = pd.read_csv(file_path)
    html_table = df.to_html(classes='table table-striped', index=False)

    return {'table': html_table, 'filename': filename}


@view_config(route_name='edit_csv', renderer='templates/edit.jinja2')
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


# Main application setup
def main(global_config=None, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('upload', '/upload')
    config.add_route('view_csv', '/view')
    config.add_route('edit_csv', '/edit')
    config.add_route('save_csv', '/save')
    config.scan()
    return config.make_wsgi_app()


if __name__ == "__main__":
    app = main()
    server = make_server('0.0.0.0', 6544, app)
    server.serve_forever()
