import logging
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import json
import os

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

# View to serve the home page
def home_view(request):
    home_path = os.path.join(os.path.dirname(__file__), 'templates', 'home.html')
    logger.debug(f"Serving home page from {home_path}")
    return FileResponse(home_path)

if __name__ == '__main__':
    with Configurator() as config:
        # Add new API route
        logger.debug("Adding API route /api/load_file")
        config.add_route('load_file', '/api/load_file')
        config.add_view(load_file, route_name='load_file', renderer='json')

        # Add route for home page
        logger.debug("Adding route for home page /")
        config.add_route('home', '/')
        config.add_view(home_view, route_name='home')

        app = config.make_wsgi_app()

    logger.info("Starting server on http://localhost:6543")
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
