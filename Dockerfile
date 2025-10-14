# AWS Lambdaの公式Python 3.12イメージをベースとして使用
FROM public.ecr.aws/lambda/python:3.12

# 作業ディレクトリを設定
WORKDIR ${LAMBDA_TASK_ROOT}

# 依存関係ファイルをコピー
COPY requirements.txt .

# キャッシュを無効化するためのダミーファイルをコピー
COPY cache_buster.txt .

# pipを使用して依存関係をインストール
RUN pip install -r requirements.txt --no-cache-dir

# アプリケーションのソースコードをコピー
COPY src/ ${LAMBDA_TASK_ROOT}/src

# CMDはtemplate.yamlで指定するため、ここでは設定しない
