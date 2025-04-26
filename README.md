# Amazon Bedrockを活用した画像からの日本語テキストの抽出

## 概要
このリポジトリは、Amazon Bedrockのマルチモーダル機能を使用して画像やPDFから日本語テキストを抽出するサンプルコードを提供します。
AWSの既存OCRサービス（Amazon Textract、Recognition）では日本語対応が不十分な中、
生成AIを活用した代替手段としてのテキスト抽出方法を実装しています。

## 記事リンク
詳細な解説記事: [Amazon Bedrockを活用した画像からの日本語テキストの抽出](https://qiita.com/enumura1/items/39ffff1a5eb1f5b77cfd)

## 構成
- `lambda_function.py`: Lambda関数のメインファイル
- `invoke_bedrock.py`: Amazon Bedrockの呼び出し処理を担当
- `result_formatter.py`: 結果の整形と統計処理を担当

## 環境
- Python: 3.13
- AWS Bedrock: Claude 3.5 Sonnet v2
- AWS リージョン: 東京リージョン

## 機能
- S3から複数形式（PDF、PNG、JPEG、WebP）の画像ファイルを取得
- Amazon Bedrockを使用して画像内の日本語テキストを抽出
- 処理時間の計測と結果の整形

## 使用方法
1. AWS上でS3バケットとLambda関数を作成
2. 必要なポリシーをLambdaロールに付与（AmazonBedrockFullAccess、AmazonS3FullAccess）
3. 3つのスクリプトファイルをLambdaにアップロード
4. S3バケットに画像ファイルをアップロード
5. Lambda関数を実行して結果を確認
