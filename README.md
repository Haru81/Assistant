# Assistant
ユーザーサポートアシスタントアプリ（Ver.1）(2024/1/5)

[概要]
音声認識によってAIモデルと会話し、
ユーザーの課題を解決するユーザーサポートアシスタント。

１．入力部
（使用したライブラリ）
・pyAudio


２．AIモデル部
（使用したモデル）
・Gemini 2.0 Flash


３．出力部
（使用したライブラリ）
・
（使用したAPI）
・style-berts-vits

４．アルゴリズム
（記憶（履歴）機能）
会話内容をjson形式で書き出し、それを読み込むことで性格と記憶を引き継ぐ。

５．変更履歴
2024/1/5　Ver.1　初版
2024/1/6　Ver.2　アルゴリズムを追記

６．使用方法
Ver.1
・Fast APIの立ち上げ
sbv2/Style-Bert-VITS2へ移動し、
Python server_fastapi.py

・プログラムの実施
Python main.py
