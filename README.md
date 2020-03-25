﻿pysanです。
今回作ったテトリスソルバーのコードです。
実行するにはpcにpython3の実行環境が必要です。

<ファイルたち>
・solver.py　テトリスを学習するやつ。実行すると「genom_log(数字).txt」というファイルを作成し、そこに遺伝子データが書き込まれます。
以下のファイルが、同じ階層に保存されていないとエラーが発生します。
・tetris.py　solverが遺伝子データにテトリスをプレイさせるために使うファイル。人間には見てても面白くないです。
・tetris_write.py　実際にプレイしてるところを可視化したもの。発表で実演するときに使用したのはこのファイル。使い方を後述。
・__init__.py　pythonの仕様で必要なファイル。中身はなにもない。
・__pycache__(ファイル)　同上

<tetris_write.pyの使い方>
実行する
genom list? で、solverが作成した遺伝子データ「genom_log(数字).txt」の数字だけを入力する(0を入力するとランダムな遺伝子データが作成され、それをもとにプレイする(ものすごくへたっぴ))
generation? で、遺伝子データの中の参照させたい遺伝子の世代を数字だけ入力(なにも入力しないと最も良い世代が適用される)

・genom_log1.txtが発表で見せた、計算に4日かかったもの
・2，3は途中で断念した。せっかくなのでのせときます。