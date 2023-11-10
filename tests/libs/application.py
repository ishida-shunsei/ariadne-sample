from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLTransportWSHandler
from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute

from app.schema import schema_for_asgi


graphql_app = GraphQL(
    schema_for_asgi,
    debug=True,
    websocket_handler=GraphQLTransportWSHandler(),
)


# Create Starlette App instance using method handlers from GraphQL as endpoints
app = Starlette(
    routes=[
        Route("/graphql/", graphql_app.handle_request, methods=["GET", "POST", "OPTIONS"]),
        WebSocketRoute("/graphql/", graphql_app.handle_websocket),
    ],
)
