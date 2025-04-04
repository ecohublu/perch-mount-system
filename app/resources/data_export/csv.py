import csv
import io


def json_to_csv(json_data: dict[str]) -> str:
    if not isinstance(json_data, dict):
        raise ValueError("Input must be a dictionary.")

    # 準備一個 StringIO 物件來暫存 CSV 資料
    output = io.StringIO()
    writer = csv.writer(output)

    # 把字典的 keys 作為 CSV 的標頭
    headers = json_data.keys()
    writer.writerow(headers)

    # 把字典的 values 作為 CSV 的資料列
    writer.writerow(json_data.values())

    # 取得 CSV 字串
    csv_string = output.getvalue()
    output.close()

    return csv_string
