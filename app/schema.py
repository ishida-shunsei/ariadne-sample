from datetime import datetime
import dateutil.parser

from ariadne import (
    QueryType,
    MutationType,
    ScalarType,
    make_executable_schema,
    load_schema_from_path,
)

from app import resolvers

# GraphQL スキーマ定義
type_defs = load_schema_from_path("schema.graphql")

### Scalar 定義 ###
datetime_scalar = ScalarType("Datetime")

@datetime_scalar.serializer
def serialze_datetime(value: datetime):
    return value.isoformat()


@datetime_scalar.value_parser
def parse_datetime_input(value):
    return dateutil.parser.parse(value)


### Query 定義 ###
query = QueryType()
query.set_field("users", resolvers.resolve_users)
query.set_field("departments", resolvers.resolve_departments)
query.set_field("employees", resolvers.resolve_employees)


### Mutation 定義 ###
mutation = MutationType()
mutation.set_field("createUser", resolvers.resolve_create_user)
mutation.set_field("updateUser", resolvers.resolve_update_user)
mutation.set_field("deleteUser", resolvers.resolve_delete_user)
mutation.set_field("createEmployee", resolvers.resolve_create_employee)
mutation.set_field("updateEmployee", resolvers.resolve_update_employee)
mutation.set_field("deleteEmployee", resolvers.resolve_delete_employee)


# 定義された型
defined_types = [
    query,
    mutation,
    datetime_scalar,
]

# ASGIアプリに読み込ませるスキーマ
schema_for_asgi = make_executable_schema(
    type_defs,
    *defined_types,
    convert_names_case=True,
)
