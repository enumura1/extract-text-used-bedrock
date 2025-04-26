import json
import datetime


# 実行結果をフォーマット
def format_results(results, metrics, file_keys):

    # 結果を整形
    formatted_results = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "total_files": len(file_keys),
            "successful": sum(1 for k in results if results[k]["status"] == "成功"),
            "failed": sum(1 for k in results if results[k]["status"] == "失敗")
        },
        "performance": {
            file_key: {
                "file_type": metrics[file_key].get("file_type", "不明"),
                "processing_time": f"{metrics[file_key].get('total_time_seconds', 'N/A')}秒",
                "api_time": f"{metrics[file_key].get('api_time_seconds', 'N/A')}秒" if "api_time_seconds" in metrics[file_key] else "N/A"
            } for file_key in file_keys
        },
        "extraction_results": {
            file_key: results[file_key]["extracted_text"] if results[file_key]["status"] == "成功" else f"エラー: {results[file_key]['extracted_text']}"
            for file_key in file_keys
        }
    }
    
    return formatted_results

# パフォーマンス概要を作成
def create_performance_summary(formatted_results, metrics):
    performance_summary = {
        "timestamp": formatted_results["timestamp"],
        "summary": formatted_results["summary"],
        "average_processing_time": f"{sum(metrics[k].get('total_time_seconds', 0) for k in metrics) / len(metrics):.2f}秒"
    }
    
    return performance_summary
