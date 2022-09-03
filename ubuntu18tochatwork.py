#!/usr/bin/env python3
# coding: UTF-8

import subprocess

# コマンド実行
server_remaining_amount = subprocess.run(['df', '-h','/dev/mapper/ubuntu--vg-ubuntu--lv'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
necessity_reboot= subprocess.run(['find','/var/run/reboot-required.pkgs'],stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
update_notice = subprocess.run(['apt','list','--upgradable'],stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")

# 出力結果から必要な情報のみを抽出
sra = server_remaining_amount.stdout
t = sra.split()
remain_amount = t[10]
use_ratio = t[11]

tgt = '%'
idx = use_ratio.find(tgt)
use_ratio = use_ratio[:idx]
# ↑数値として扱うために%を切り捨て

# 95%未満は対応保留、95%以上は対応とする
if int(use_ratio) >= 95:
	case_1 = "95%以上のため対応してください。"
else:
	case_1 = "95%未満のため対応保留します。"

# 再起動ファイルの有無を表示
nr = necessity_reboot.stdout
print("result:" + nr)
nr = str(nr)

#if nr == path:
#        nr = "null"
#else:
#        nr = "再起動"

print("実行後:"+ nr)

# セキュリティのアップデートのみ抽出
updaten = update_notice.stdout
updaten.splitlines()
update_in = [s for s in updaten if 'security' in s]

if update_in:
	update_in = "セキュリティアップデートがあります。"
else:
	update_in = "アップデート通知はありません。"

# chatworkに飛ばす処理
import sys
import requests
import pprint
import datetime

APIKEY = '*******************'
ENDPOINT = 'https://api.chatwork.com/v2'
ROOMID = '*****'
now = datetime.datetime.now()

str_out = now.strftime('%m月%d日') + ' Linuxサーバメンテナンス結果\n / 以下 ' + use_ratio + '%使用(残' + remain_amount + 'B) 再起動=' + nr + ' ' + update_in + '\n    ' + case_1

post_message_url = '{}/rooms/{}/messages'.format(ENDPOINT,ROOMID)

headers = { 'X-ChatWorkToken': APIKEY }
params = { 'body': str_out}

resp = requests.post(post_message_url,
                     headers=headers,
                     params=params)

pprint.pprint(resp.content)
