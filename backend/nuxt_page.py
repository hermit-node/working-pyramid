import subprocess
import os
import logging
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# API endpoint to return a dummy response
def load_file(request):
    response_data = {'message': 'here you go'}
    logger.debug("Sending dummy response")
    return Response(
        json.dumps(response_data),
        content_type='application/json',
        charset='utf-8'
    )


# Serve the Nuxt app
def serve_nuxt_app(request):
    nuxt_public_path = os.path.join(os.path.dirname(__file__), '..', 'nuxt3-app', 'dist')
    nuxt_index_path = os.path.join(nuxt_public_path, 'index.html')
    logger.debug(f"Serving Nuxt app from {nuxt_index_path}")

    if not os.path.exists(nuxt_index_path):
        logger.error(f"Nuxt index.html not found at {nuxt_index_path}")
        return Response('Nuxt index.html not found', status=404)

    return FileResponse(nuxt_index_path)


def build_nuxt_app():
    try:
        nuxt_app_path = os.path.join(os.path.dirname(__file__), '..', 'nuxt3-app')
        logger.debug(f"Building Nuxt app in directory: {nuxt_app_path}")
        subprocess.check_call('pnpm install', cwd=nuxt_app_path, shell=True)
        subprocess.check_call('pnpm run build', cwd=nuxt_app_path, shell=True)
        subprocess.check_call('pnpm run generate', cwd=nuxt_app_path, shell=True)
        logger.debug("Nuxt app built successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred during Nuxt build process: {e}")
        exit(1)


if __name__ == '__main__':
    # Build the Nuxt app before starting the server
    build_nuxt_app()

    with Configurator() as config:
        # Add new API route
        logger.debug("Adding API route /api/load_file")
        config.add_route('load_file', '/api/load_file')
        config.add_view(load_file, route_name='load_file', renderer='json')

        # Serve static files for the Nuxt app
        logger.debug("Adding static view for Nuxt assets")
        config.add_static_view(name='assets',
                               path=os.path.join(os.path.dirname(__file__), '..', 'nuxt3-app', 'dist', '_nuxt'))

        # Wildcard route to serve the Nuxt app
        logger.debug("Adding wildcard route for Nuxt app")
        config.add_route('nuxt_app', '/*subpath')
        config.add_view(serve_nuxt_app, route_name='nuxt_app')

        app = config.make_wsgi_app()

    logger.info("Starting server on http://localhost:6543")
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
