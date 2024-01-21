# 変数
IMAGE_NAME = flask-image
CONTAINER_NAME = flask-container

# Dockerイメージをビルドする
build:
	docker build -t $(IMAGE_NAME) .

# Dockerコンテナを実行する
run:
	docker run -d --name $(CONTAINER_NAME) -p 3000:3000 $(IMAGE_NAME)

# Dockerコンテナを停止する
stop:
	docker stop $(CONTAINER_NAME)

# Dockerコンテナを開始する
start:
	docker start $(CONTAINER_NAME)

# Dockerコンテナを削除する
remove:
	docker rm $(CONTAINER_NAME)

# Dockerイメージを削除する
clean:
	docker rmi $(IMAGE_NAME)

# Dockerコンテナを再実行する
rerun: stop remove clean build run

# Dockerコンテナのログを表示する
log:
	docker logs -f $(CONTAINER_NAME)

# Dockerコンテナ内でコマンドを実行する
exec:
	docker exec -it $(CONTAINER_NAME) /bin/bash
