# AWS Lambda 上で動作する MCP サーバー

このプロジェクトは、AWS Lambda 上で Model Context Protocol (MCP) サーバーを構築し、他の Lambda 関数を呼び出すためのサンプル実装です。AWS SAM (Serverless Application Model) を利用して、ローカルでの開発・テストと AWS へのデプロイを容易にします。

## プロジェクト概要

`MCPEngine` ライブラリを利用して、他の Lambda 関数を呼び出す MCP サーバーを実装します。

- **MCPServerFunction**: `invoke_lambda_sync` と `invoke_lambda_async` ツールを提供する MCP サーバー。
- **SampleFunction**: 呼び出される側のサンプル関数。

## 前提条件

- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) がインストールされていること。
- [Docker](https://docs.docker.com/get-docker/) がインストールされていること。
- AWS の認証情報が設定されていること（デプロイ時に必要）。

## 開発とデプロイ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. アプリケーションのビルド

次のコマンドを実行して、SAM アプリケーションをビルドします。これにより、`template.yaml` に基づいてソースコードが準備され、コンテナイメージが作成されます。

```bash
sam build
```

### 3. ローカルでのテスト

SAM CLI を使って、ローカルで Lambda 関数をテストできます。以下のコマンドは、`MCPServerFunction` をローカルで起動し、指定したイベントファイルを使って関数を呼び出します。

```bash
sam local invoke MCPServerFunction --event events/mcp-server-event.json
```

### 4. AWS へのデプロイ

`sam deploy` コマンドを使えば、アプリケーションを簡単に AWS アカウントにデプロイできます。

```bash
# ガイド付きデプロイ (初回)
sam deploy --guided

# 2回目以降のデプロイ
sam deploy
```

ガイドに従ってスタック名、リージョンなどを設定すると、CloudFormation スタックが作成され、Lambda 関数や IAM ロールなどのリソースが自動的にプロビジョニングされます。

### 5. ローカルから AWS Lambda を実行するテスト

- MCP サーバー関数のテスト

関数 URL（https://XXXXX.lambda-url.ap-northeast-1.on.aws/）はデプロイした Lambda の画面から確認できます。適宜変更して実行してください。

```bash
  curl -X POST \
   https://XXXXX.lambda-url.ap-northeast-1.on.aws/ \
   -H 'Content-Type: application/json' \
   -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"invokeLambdaSync","arguments":{"function_name":"test-sample-function","payload":{"name":"From curl"}}},"id":"curl-test-1"}'
```
