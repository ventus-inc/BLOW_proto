# BLOW プロトタイプ
## リポジトリ概要
BLOWのプロジェクトソースコードです。（いったんは東大SFP用）

## 開発環境について
[wiki](https://github.com/ventus-inc/proto_blow/wiki "wiki")にまとめていきます。必ず目を通してください。

## QuickStart
* 仮想環境を立ち上げる

`. bin/activate`
* pip で必要パッケージのインストール

`pip install -r requirements.txt`
* src/ディレクトリに移動 _ソースはsrcに入っている_

`cd src`
* django のインストールを確認

`pip freeze` or `django-admin.py version`
1.10.3をインストールしている
* DBを作成

    python manage.py makemigrations
    python manage.py migrate
