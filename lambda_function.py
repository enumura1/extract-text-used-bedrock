import json
import logging
from invoke_bedrock import process_files
from result_formatter import format_results, create_performance_summary


# ロガーの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # S3バケット名とオブジェクトキーの設定
    bucket = "extract-image-used-bedrock"
    file_keys = [
        "textExtractionSheet.jpeg",
        "textExtractionSheet.pdf",
        "textExtractionSheet.png",
        "textExtractionSheet.webp"
    ]
    
    # システムプロンプト
    prompt = """画像からテキストを抽出してください。必ず以下の形式で出力してください。
・チーム名：
・費用：
・費用の内訳：
・支払日時：
・用途（チェックが入っているもの）：
チェックボックスがある場合は、チェックが入っている項目のみを「用途」欄に記載してください。
すべての情報を正確に抽出し、見つからない項目がある場合は「情報なし」と記載してください。"""
    
    # ファイル処理
    results, metrics = process_files(file_keys, bucket, prompt)
    
    # 結果フォーマット
    formatted_results = format_results(results, metrics, file_keys)
    
    # CWに実行結果を出力
    logger.info("実行結果:\n%s", json.dumps(formatted_results, ensure_ascii=False, indent=2))
    performance_summary = create_performance_summary(formatted_results, metrics)
    logger.info("処理概要: %s", json.dumps(performance_summary, ensure_ascii=False))
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(formatted_results, ensure_ascii=False, indent=2)
    }
