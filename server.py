from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNoContent

from opentelemetry.instrumentation.pyramid import PyramidInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

resource = Resource(attributes={
    SERVICE_NAME: "hello-world"
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

PyramidInstrumentor().instrument()

def hello_world(request):
    return Response('Hello World!')

def redirect_view(Request):
    return HTTPFound(location='/')

def empty_response(Request):
    return HTTPNoContent()

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')


        config.add_route('redirect_view', '/302')
        config.add_view(redirect_view, route_name='redirect_view')

        config.add_route('empty_response', '/204')
        config.add_view(empty_response, route_name='empty_response')

        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()