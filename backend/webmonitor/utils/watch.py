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


# 创建一个watch 返回watch的id
def create_watch(watch_url):
    api_key = current_app.config['CHANGEDETECTIONIO_API_KEY']
    url     = current_app.config['CHANGEDETECTIONIO_API_URL']
    headers = { "x-api-key": api_key, "Content-Type": "application/json" }   
    data = {
        "url": watch_url,
        "tag": "webmonitor",
    }
    response = requests.post(url + "/watch", headers=headers, json=data)
    print(response.json())
    return response.json()['uuid']


# 修改一个watch
def update_watch(id, update_data):
    api_key = current_app.config['CHANGEDETECTIONIO_API_KEY']
    url     = current_app.config['CHANGEDETECTIONIO_API_URL']
    headers = { "x-api-key": api_key, "Content-Type": "application/json" }   
    data = {
        "url": update_data['url']
    }
    time_between_check = {}

    # 如果有time_between_check的任何一个字段有值，就更新time_between_check
    if 'time_between_check_weeks' in update_data and update_data['time_between_check_weeks']:
        time_between_check['weeks'] = update_data['time_between_check_weeks']
    if 'time_between_check_days' in update_data and update_data['time_between_check_days']:
        time_between_check['days'] = update_data['time_between_check_days']
    if 'time_between_check_hours' in update_data and update_data['time_between_check_hours']:
        time_between_check['hours'] = update_data['time_between_check_hours']
    if 'time_between_check_minutes' in update_data and update_data['time_between_check_minutes']:
        time_between_check['minutes'] = update_data['time_between_check_minutes']
    if 'time_between_check_seconds' in update_data and update_data['time_between_check_seconds']:
        time_between_check['seconds'] = update_data['time_between_check_seconds']

    if time_between_check:
        data['time_between_check'] = time_between_check
    if 'include_filters' in update_data and update_data['include_filters']:
        data['include_filters'] = update_data['include_filters']
    # if update_data['subtractive_selectors']:
    #     data['subtractive_selectors'] = update_data['subtractive_selectors']
    # if update_data['ignore_text']:
    #     data['ignore_text'] = update_data['ignore_text']
    # if update_data['trigger_text']:
    #     data['trigger_text'] = update_data['trigger_text']

    print(data)
    response = requests.put(url + f"/watch/{id}", headers=headers, json=data)
    print(response)
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
