import contextlib

from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLTransportWSHandler
from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute

from app.database import database_for_lifespan
from app.schema import schema_for_asgi
from app.logging import logging


graphql_app = GraphQL(
    schema_for_asgi,
    debug=True,
    websocket_handler=GraphQLTransportWSHandler(),
)


@contextlib.asynccontextmanager
async def lifespan(app):
    await database_for_lifespan.connect()
    yield
    await database_for_lifespan.disconnect()


# Create Starlette App instance using method handlers from GraphQL as endpoints
app = Starlette(
    routes=[
        Route("/graphql/", graphql_app.handle_request, methods=["GET", "POST", "OPTIONS"]),
        WebSocketRoute("/graphql/", graphql_app.handle_websocket),
    ],
    lifespan=lifespan,
)
