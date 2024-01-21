# 公式のPythonイメージをベースイメージとして使用
FROM python:3.9-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# コンテナ内の作業ディレクトリを設定
WORKDIR /src
COPY app ./

# 依存関係をインストール
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# エントリポイントコマンドを設定してアプリを実行
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:3000", "--worker-class", "eventlet"]