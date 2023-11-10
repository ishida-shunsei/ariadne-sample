# Ariadne + Starlette + SQLAlchemy の GraphQL API サンプル

## セットアップ
```bash
# Python仮想環境を作成
python -m venv .venv
# 仮想環境のコンテキストに移動
.venv/Scripts/activate
# 依存モジュールをインストール
pip install -r requirements.txt
# データベースを作成
alembic upgrade head
# データベースの初期データを投入
python ./fixture_master.py
```

## 実行
```bash
uvicorn asgi:app
```

## ベタープラクティス
UpdateのMutationを実行するとき、変更対象の項目ではなくても必須項目は都度入力させる縛りを設けたほうがよさそう。
そうするとtypeとinputを１つずつ作るだけでCRUDが実現できるのでコードが簡潔になる。
```graphql
type Query {
  users(id: ID=null, name: String=null, email=null): [User]!
}
type Mutation {
  createUser(input: UserInput!): User!
  updateUser(id: ID!, input: UserInput!): User!
}

type User {
  # 必須項目
  id: ID!
  email: String!
  ＃ 非必須項目
  name: String
  job: String
  income: Int
  household: Int
}

# id がない以外はUserと同じ
input UserInput {
  email: String!
  name: String
  job: String
  income: Int
  household: Int
}
```