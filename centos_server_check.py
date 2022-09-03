#!/usr/bin/env python3
# coding: UTF-8

# コマンド実行と結果取得の処理
import subprocess

# コマンド実行
server_remaining_amount = subprocess.run(['df', '-h','/dev/mapper/centos-root'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
update_notice = subprocess.run(['yum','check-update','--security'],stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")

# 出力結果から必要な情報のみを抽出
sra = server_remaining_amount.stdout
t = sra.split()
remain_amount = t[9]
use_ratio = t[10]

tgt = '%'
idx = use_ratio.find(tgt)
use_ratio = use_ratio[:idx]
# ↑数値として扱うために%を切り捨て

# 70%未満は対応保留、70%以上は対応とする
if int(use_ratio) >= 70:
	case_1 = "\n  70%以上のため対応してください。"
else:
	case_1 = "\n  70%未満のため対応保留します。"

# セキュリティのアップデートのみ抽出
updaten = update_notice.stdout
target = 'needed for security'
idx_1 = updaten.find(target)
p = updaten[:idx_1]
sep = ' '
t = p.split(sep)
update_in = t[-3]
update_in = update_in.replace('(updateinfo)\n', '')

if update_in == 'No':
    update_in = '0'

# chatworkに飛ばす処理
import sys
import requests
import pprint
import datetime

APIKEY = '*******************'
ENDPOINT = 'https://api.chatwork.com/v2'
ROOMID = '*****'
now = datetime.datetime.now()

str_out = now.strftime('%m月%d日') + ' Linuxサーバメンテナンス結果\n / 以下 ' + use_ratio + '%使用(残' + remain_amount + 'B) ' + update_in + '個のアップデート通知があります。' + case_1

post_message_url = '{}/rooms/{}/messages'.format(ENDPOINT,ROOMID)

headers = { 'X-ChatWorkToken': APIKEY }
params = { 'body': str_out}

resp = requests.post(post_message_url,
                     headers=headers,
                     params=params)

pprint.pprint(resp.content)
