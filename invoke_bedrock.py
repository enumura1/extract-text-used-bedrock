import boto3
import time
import logging


logger = logging.getLogger()

def process_files(file_keys, bucket, prompt):
    """
    S3からファイルを取得し、Bedrockで処理する
    """
    bedrock_runtime = boto3.client('bedrock-runtime')
    s3 = boto3.client('s3')
    
    results = {}
    metrics = {}
    
    for file_key in file_keys:
        try:
            start_time = time.time()
            
            # S3からファイルを取得
            response = s3.get_object(Bucket=bucket, Key=file_key)
            file_content = response['Body'].read()
            
            # ファイル形式を取得
            file_extension = file_key.split('.')[-1].lower()
            
            # メッセージの構築
            messages = [
                {
                    "role": "user",
                    "content": []
                }
            ]
            
            # ファイルタイプに応じてコンテンツを追加
            if file_extension in ['jpeg', 'jpg', 'png', 'webp']:
                messages[0]["content"].append({
                    "image": {
                        "format": file_extension,
                        "source": {
                            "bytes": file_content
                        }
                    }
                })
            elif file_extension == 'pdf':
                messages[0]["content"].append({
                    "document": {
                        "name": "DocumentFile",
                        "format": "pdf",
                        "source": {
                            "bytes": file_content
                        }
                    }
                })
            
            # プロンプトを追加
            messages[0]["content"].append({"text": prompt})
            
            # Bedrockの呼び出し
            api_start_time = time.time()
            response = bedrock_runtime.converse(
                modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
                messages=messages
            )
            api_end_time = time.time()
            
            # レスポンスを処理
            assistant_message = response["output"]["message"]["content"][0]["text"]
            
            end_time = time.time()
            
            # 処理時間の計測
            total_time = end_time - start_time
            api_time = api_end_time - api_start_time
            
            # 結果の保存
            results[file_key] = {
                "extracted_text": assistant_message,
                "status": "成功"
            }
            
            # メトリクスの保存
            metrics[file_key] = {
                "total_time_seconds": round(total_time, 2),
                "api_time_seconds": round(api_time, 2),
                "file_type": file_extension
            }
            
            logger.info(f"処理完了: {file_key} (API: {round(api_time, 2)}秒, 合計: {round(total_time, 2)}秒)")
            
        except Exception as e:
            error_message = str(e)
            logger.error(f"エラー発生 ({file_key}): {error_message}")
            
            results[file_key] = {
                "extracted_text": f"エラー: {error_message}",
                "status": "失敗"
            }
            
            metrics[file_key] = {
                "error": error_message,
                "file_type": file_key.split('.')[-1].lower()
            }
    
    return results, metrics
