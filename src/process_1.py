from datetime import date
import os
import requests
from typing import TypedDict


## reference: https://sorabatake.jp/12465/


class SearchPalsarParams(TypedDict):
    lat: float
    lon: float
    start_datetime: str
    end_datetime: str

def data_search_palsar_l11(
    token: str,
    params: SearchPalsarParams = {},
    base_url="https://www.tellusxdp.com/api/traveler/v1/datasets/{}/data-search/"
):
    dataset_id = "8836ec9a-35b5-43c3-92be-263498061e91"  # PALSAR_L1.1のプロダクトID
    headers = {"Authorization": "Bearer " + token}
    url = base_url.format(dataset_id)
    lon = params.get("lon")
    lat = params.get("lat")
    start_datetime = params.get("start_datetime")
    end_datetime = params.get("end_datetime")

    request_body = {
        "intersects": {
            "type":
            "Polygon",
            # 検索範囲を領域で指定
            "coordinates": [[
                [lon, lat],
                [lon + 0.01, lat],
                [lon + 0.01, lat + 0.01],
                [lon, lat + 0.01],
                [lon, lat],
            ]]
        },
        "query": {
            # 検索期間の指定
            "start_datetime": {
                "gte": start_datetime
            },
            "end_datetime": {
                "lte": end_datetime
            },
        }
    }

    # 該当するデータの情報を取得
    response = requests.post(url, json=request_body, headers=headers)
    if not response.status_code == requests.codes.ok:
        response.raise_for_status()
    return response.json()


def data_files_palsar_l11(
    token: str,
    data_id: str,
    base_url="https://www.tellusxdp.com/api/traveler/v1/datasets/{}/data/{}/files/"
):
    dataset_id = "8836ec9a-35b5-43c3-92be-263498061e91"  # PALSAR_L1.1のプロダクトID
    headers = {"Authorization": "Bearer " + token}
    url = base_url.format(dataset_id, data_id)

    # 該当するデータの情報を取得
    response = requests.get(url, headers=headers)
    if not response.status_code == requests.codes.ok:
        response.raise_for_status()
    return response.json()


def get_file_info(files_json, pol: str):
    for i in files_json["results"]:
        if i["name"].startswith(f"IMG-{pol}"):
            img = {str(i["id"]): i["name"]}
        elif i["name"].startswith("LED"):
            led = {str(i["id"]): i["name"]}
    files = [img, led]
    return files


def download_files(
        token,
        data_id_list: list,
        files_list: list,
        base_url:
    str = "https://www.tellusxdp.com/api/traveler/v1/datasets/{}/data/{}/files/{}/download-url/",
        save_dir: str = "./processed_1"):
    dataset_id = "8836ec9a-35b5-43c3-92be-263498061e91"  # PALSAR_L1.1のプロダクトID
    headers = {"Authorization": "Bearer " + token}

    for data_id, files_data in zip(data_id_list, files_list):
        for file_data in files_data:
            file_id = int(list(file_data.keys())[0])
            file_name = list(file_data.values())[0]
            url = base_url.format(dataset_id, data_id, file_id)
            # ダウンロードURLの発行
            response_post = requests.post(url, headers=headers)
            dl_url = response_post.json()["download_url"]
            # 現在のディレクトリ下にファイルをダウンロード
            with open(f"{save_dir}/{file_name}", "wb") as f:
                f.write(requests.get(dl_url).content)


def main():
    token = os.environ['TELLUS_API_ACCESS_TOKEN']
    # 博多駅の座標
    lat = 33.590  # 緯度
    lon = 130.420  # 経度
    # 観測データの検索
    searched_data = data_search_palsar_l11(
        token=token,
        params={
            "lat": lat,
            "lon": lon,
            "start_datetime":
            "2006-01-01T15:00:00Z",
            "end_datetime":
            "2024-03-18T12:31:12Z"
        })
    # 観測データの確認1
    print(searched_data.keys())
    print(searched_data.get("features")[0].keys())
    # 観測データの確認2
    # 取得した観測データの数
    print(len(searched_data.get("features")))
    # 0番目の観測データのプロパティを表示
    for k, v in searched_data["features"][0]["properties"].items():
        print("{:<30} +      {}".format(k, v))

    # 可干渉な観測データIDのリスト
    data_list = []
    for data in searched_data.get("features"):
        prop = data["properties"]
        if (prop["sat:relative_orbit"] == 420  # 衛星の軌道経路
                and prop["sat:orbit_state"] == "ascending"  # 衛星の進行方向
                and prop["sar:observation_direction"] == "right"  # 電波照射方向
                and prop["view:off_nadir"] == 21.5  # オフナディア角
                and prop["tellus:sat_frame"] == 660  # 観測範囲の中心位置
                and prop["sar:polarizations"] == "HH"  # 送受信の偏波  
                and prop["sar:instrument_mode"] == "H"  # 観測モード
            ):
            data_list.append(data["id"])

    for data in data_list:
        print(data)

    # ファイルIDの取得
    file_id_list = []
    pol = "HH"  # 送受信時の偏波
    for data_id in data_list:
        file_id_list.append(
            get_file_info(data_files_palsar_l11(token=token, data_id=data_id),
                          pol))
    for file_id in file_id_list:
        print(file_id)

    # データのダウンロード
    # 直下に processed_1 ディレクトリを作成しておいてください
    download_files(token=token,
                   data_id_list=data_list,
                   files_list=file_id_list)


if __name__ == "__main__":
    main()
