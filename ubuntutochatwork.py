#!/usr/bin/env python3
#coding: UTF-8

import subprocess

server_remaining_amount = subprocess.run(['df', '-h','/dev/mapper/ubuntu--vg-ubuntu--lv'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
necessity_reboot = subprocess.run(['find', 'reboot-required'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
update_notice = subprocess.run(['apt', 'list', '--upgradable'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")

sra = server_remaining_amount.stdout
t = sra.split()
remain_amount = t[10]
use_ratio = t[11]

tgt = '%'
idx = use_ratio.find(tgt)
use_ratio = use_ratio[:idx]

if int(use_ratio) >= 95:
case_1 = “要対応”
else:
case_1 = “保留”

nr = necessity_reboot.stdout
if nr == "/var/run/reboot-required":
nr = "要再起動"
else:
nr = " "

updaten = update_notice.stdout
updaten.splitlines()
update_in = [s for s in updaten if 'security' in s]

if update_in:
update_in = "アップデート通知があります。”
else:
update_in = " "

import sys
import requests
import pprint
import datetime

APIKEY = '*******************'
ENDPOINT = 'https://api.chatwork.com/v2'
ROOMID = '********'
now = datetime.datetime.now()

str_out = now.strftime('%m月%d日') + use_ratio + '%使用(残' + remain_amount + 'B)' + nr + update_in + '\n' + case_1

post_message_url = '{}/rooms/{}/messages'.format(ENDPOINT,ROOMID)

headers = { 'X-ChatWorkToken': APIKEY }
params = { 'body': str_out}

resp = requests.post(post_message_url,
headers=headers,
params=params)

pprint.pprint(resp.content)