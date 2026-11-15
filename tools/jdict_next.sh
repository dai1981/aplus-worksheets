#!/bin/bash
# 辞書バッチのキュー（jdict/queue.txt）から次のバッチ名を1つ取り出す。同時に呼ばれても重ならない。
cd "$(dirname "$0")/.."
exec 9>jdict/.queue.lock; flock 9
b=$(head -1 jdict/queue.txt 2>/dev/null); [ -n "$b" ] && sed -i 1d jdict/queue.txt; echo "$b"
