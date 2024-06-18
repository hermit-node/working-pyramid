import subprocess
import os
import logging
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import FileResponse, Response
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Serve the Vue app
def serve_vue_app(request):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'vue_app', 'dist', 'index.html')
    logger.debug(f"Serving file: {file_path}")
    return FileResponse(file_path)

# API endpoint to return a dummy response
def load_file(request):
    response_data = {'message': 'here you go'}
    logger.debug("Sending dummy response")
    return Response(
        json.dumps(response_data),
        content_type='application/json',
        charset='utf-8'
    )

def build_vue_app():
    try:
        vue_app_path = os.path.join(os.path.dirname(__file__), '..', 'vue_app')
        logger.debug(f"Building Vue app in directory: {vue_app_path}")
        subprocess.check_call('npm install', cwd=vue_app_path, shell=True)
        subprocess.check_call('npm run build', cwd=vue_app_path, shell=True)
        logger.debug("Vue app built successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred during Vue build process: {e}")
        exit(1)

if __name__ == '__main__':
    # Build the Vue app before starting the server
    build_vue_app()

    with Configurator() as config:

        logger.debug("Adding API route /api/load_file")
        config.add_route('load_file', '/api/load_file')
        config.add_view(load_file, route_name='load_file', renderer='json')

        config.add_static_view(name='assets', path=os.path.join(os.path.dirname(__file__), '..', 'vue_app', 'dist', 'assets'))
        config.add_static_view(name='', path=os.path.join(os.path.dirname(__file__), '..', 'vue_app', 'dist'))

        # Add new API route before the wildcard route

        # Adding wildcard route for Vue app
        config.add_route('vue_app', '/*subpath')
        config.add_view(serve_vue_app, route_name='vue_app')

        app = config.make_wsgi_app()

    logger.info("Starting server on http://localhost:6543")
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
