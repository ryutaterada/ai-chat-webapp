# 変数
IMAGE_NAME_1 = chat-chatapi
IMAGE_NAME_2 = chat-flask
CONTAINER_NAME_1 = chat-chatapi-1
CONTAINER_NAME_2 = chat-flask-1

# コンテナをビルドして起動する
up:
	docker compose up -d

# コンテナを停止して削除する
down:
	docker compose down

# コンテナを再起動する
restart:
	docker compose restart

# コンテナのログを表示する
logs:
	docker compose logs -f

# 実行中のコンテナ内でコマンドを実行する
exec1:
	docker compose exec $(CONTAINER_NAME_1) bash

exec2:
	docker compose exec $(CONTAINER_NAME_2) bash

# コンテナ、ネットワーク、ボリュームをクリーンアップする
clean:
	docker compose down -v --remove-orphans --rmi all

# コンテナを再実行する
rerun: down clean up
