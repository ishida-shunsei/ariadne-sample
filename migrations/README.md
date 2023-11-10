# マイグレーションの実行

```
alembic upgrade head
```

最新のリビジョンまでマイグレーションを進める場合に head を指定する。
一つだけリビジョンを進める場合は次のように指定する。

```
alembic upgrade +1
```

# マイグレーションファイルを作成
```
# --rev-id には日時を指定
alembic revision --rev-id 20231109_1346 --autogenerate -m "init"
```