import requests
from flask import current_app
import brotli
import os


# 打印watch的详情
def print_watch(watch):
    print(f"----------------------------------------")
    print(f"{watch['id']}")
    print(f"* url: {watch['url']}")
    print(f"* title: {watch['title']}")
    print(f"* last_checked: {watch['last_checked']}")
    print(f"* last_changed: {watch['last_changed']}")
    print(f"* last_error: {watch['last_error']}")


# 获取所有的watch
def get_all_watch():
    api_key = current_app.config['CHANGEDETECTIONIO_API_KEY']
    url     = current_app.config['CHANGEDETECTIONIO_API_URL']
    headers = { "x-api-key": api_key, }
    response = requests.get(url + "/watch", headers=headers)
    watches = response.json()
    watch_list = []
    for id, watch in watches.items():
        watch["id"] = id
        watch_list.append(watch)
    return watch_list


# 获取指定的watch
def get_watch(id):
    api_key = current_app.config['CHANGEDETECTIONIO_API_KEY']
    url     = current_app.config['CHANGEDETECTIONIO_API_URL']
    headers = { "x-api-key": api_key, }
    response = requests.get(url + f"/watch/{id}", headers=headers)
    watch = response.json()
    watch["id"] = id
    return watch


# 设置指定watch的状态 recheck:是否立刻更新 paused:设置暂停 muted:设置静音 
def update_watch_state(id, recheck=None, paused=None, muted=None):
    api_key = current_app.config['CHANGEDETECTIONIO_API_KEY']
    url     = current_app.config['CHANGEDETECTIONIO_API_URL']
    headers = { "x-api-key": api_key, }
    params = {}
    if recheck is not None: params["recheck"] = 1 if recheck else 0
    if paused is not None: params["paused"] = 'paused' if paused else 'unpaused'
    if muted is not None: params["muted"] = 'muted' if muted else 'unmuted'
    response = requests.get(url + f"/watch/{id}", headers=headers, params=params)
    return response.json()


# 从watch的models中提取出需要的数据
def extract_watch_data(watch):
    data = {}
    # 标签
    data['tag'] = 'webmonitor'
    # 标题
    data['title'] = f'[{watch.id}] {watch.name} | {watch.url}'
    # 地址
    data['url'] = watch.url
    # 更新时间
    time_between_check = {}
    for unit in ['weeks', 'days', 'hours', 'minutes', 'seconds']:
        time_between_check[unit] = getattr(watch, f'time_between_check_{unit}')
    data['time_between_check'] = time_between_check
    # 过滤器
    if watch.include_filters:
        filters = [f.strip() for f in watch.include_filters.split('\n') if f.strip()]
        data['include_filters'] = filters
    else:
        data['include_filters'] = []

    return data


# 创建一个watch
def create_watch(watch_model):
    api_key = current_app.config['CHANGEDETECTIONIO_API_KEY']
    url     = current_app.config['CHANGEDETECTIONIO_API_URL']
    headers = { "x-api-key": api_key, "Content-Type": "application/json" }   
    response = requests.post(url + "/watch", headers=headers, json=extract_watch_data(watch_model))
    return response.json()['uuid']


# 修改一个watch
def update_watch(id, watch_model):
    api_key = current_app.config['CHANGEDETECTIONIO_API_KEY']
    url     = current_app.config['CHANGEDETECTIONIO_API_URL']
    headers = { "x-api-key": api_key, "Content-Type": "application/json" }   
    response = requests.put(url + f"/watch/{id}", headers=headers, json=extract_watch_data(watch_model))
    return response


# 删除一个watch
def delete_watch(id):
    api_key = current_app.config['CHANGEDETECTIONIO_API_KEY']
    url     = current_app.config['CHANGEDETECTIONIO_API_URL']
    headers = { "x-api-key": api_key, }
    response = requests.delete(url + f"/watch/{id}", headers=headers)
    return response


# 查询一个watch的所有历史记录 返回按时间排序的历史记录列表
def get_watch_history(id):
    api_key = current_app.config['CHANGEDETECTIONIO_API_KEY']
    url     = current_app.config['CHANGEDETECTIONIO_API_URL']
    headers = { "x-api-key": api_key, }
    response = requests.get(url + f"/watch/{id}/history", headers=headers)
    histroy_list = []
    for stamp, history in response.json().items():
        histroy_list.append({"stamp": stamp, "file": history})
    histroy_list.sort(key=lambda x: x['stamp'])
    return histroy_list
    

# 读取某个历史记录的内容
def load_snapshot(snapshot):
    dir = current_app.config['CHANGEDETECTIONIO_DIRECTORY']
    watch_path = '/'.join(snapshot['file'].split('/')[-2:])
    file_path = os.path.join(dir, watch_path)
    with open(file_path, 'rb') as f:
        data = f.read()
    if file_path.endswith('.br'):
        data = brotli.decompress(data)
    return data.decode('utf-8')


# 获取某个watch的最新快照内容
def get_latest_snapshot(id):
    history_list = get_watch_history(id)
    if len(history_list) == 0:
        return None
    return load_snapshot(history_list[-1])


def get_second_latest_snapshot(id):
    history_list = get_watch_history(id)
    if len(history_list) < 2:
        return None
    return load_snapshot(history_list[-2])
