from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

# View for the home page
def hello_world(request):
    return Response('''
        <html>
            <body>
                <h1>Hello World!</h1>
                <form action="/another" method="get">
                    <button type="submit">Go to Another Page</button>
                </form>
            </body>
        </html>
    ''')

# View for another page
def another_page(request):
    return Response('''
        <html>
            <body>
                <h1>This is another page</h1>
                <form action="/" method="get">
                    <button type="submit">Go back to Home Page</button>
                </form>
            </body>
        </html>
    ''')

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        config.add_route('another', '/another')
        config.add_view(another_page, route_name='another')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
