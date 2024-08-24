# 変数
IMAGE_NAME_1 = ai-chat-webapp-chatapi
IMAGE_NAME_2 = ai-chat-webapp-flask
CONTAINER_NAME_1 = chatapi
CONTAINER_NAME_2 = flask

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
	docker compose exec $(CONTAINER_NAME_1) /bin/bash

exec2:
	docker compose exec $(CONTAINER_NAME_2) /bin/bash

# コンテナ、ネットワーク、ボリュームをクリーンアップする
clean:
	docker compose down -v --remove-orphans --rmi all

# コンテナを再実行する
rerun: down clean up

# gitのコミットメッセージを生成する
commit:
	git add .
	git commit -m $(m)
	git push origin main

# コンテナの再起動を行う
rebuild1:
	docker compose stop $(CONTAINER_NAME_1)
	docker compose rm -f $(CONTAINER_NAME_1)
	docker compose build $(CONTAINER_NAME_1)
	docker compose up -d $(CONTAINER_NAME_1)

rebuild2:
	docker compose stop $(CONTAINER_NAME_2)
	docker compose rm -f $(CONTAINER_NAME_2)
	docker compose build $(CONTAINER_NAME_2)
	docker compose up -d $(CONTAINER_NAME_2)
