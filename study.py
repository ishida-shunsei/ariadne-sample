from ariadne import QueryType, gql, make_executable_schema
from ariadne.explorer import ExplorerGraphiQL
from ariadne.asgi import GraphQL

type_defs = gql("""
    type Query {
        hello: String!
    }
""")

# Create type instance for Query type defined in our schema...
query = QueryType()

# ...and assign our resolver function to its "hello" field.
@query.field("hello")
def resolve_hello(_, info):
    request = info.context["request"]
    user_agent = request.headers.get("user-agent", "guest")
    return "Hello, %s!" % user_agent

schema = make_executable_schema(type_defs, query)
graphql_app = GraphQL(schema, debug=True)


explorer_html = ExplorerGraphiQL().html(None)


async def app(scope, receive, send):
    path = scope.get('path')
    method = scope.get('method')
    print(f'{path} [{method}]')
    if method == 'POST':
        await graphql_app(scope, receive, send)
    elif method == 'GET':
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'text/html'],
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': explorer_html.encode('utf-8'),
        })
    else:
        await send({
            'type': 'http.response.start',
            'status': 404,
            'headers': [
                [b'content-type', b'application/json'],
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': b'{"status": 404, "message": "Not found."}',
        })

# run: uvicorn study:app