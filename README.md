# browse use使ってみる
[こちら](https://github.com/browser-use/browser-use)を実際に動かしてみる

## 環境構築
ライブラリインストール
```bash
pip install browser-use
playwright install chromium
```

実行コード作成

```python:main.py
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3。もしプロキシ―設定が出たら、username=kosuke.usui",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    await agent.run()

asyncio.run(main())
```

LLMを変更する場合には、`llm=ChatOpenAI(model="gpt-4o")`を、[ここのサイト](https://python.langchain.com/docs/integrations/chat/)に合わせて変更。

例えば、Gemini APIなら、[.env.example](./.env.sample)のようにAPIキーを作成する


## 実行
```bash
python main.py
```

プロキシサーバーで引っ掛かったので、ついでにログを確認
> (requests.exceptions.ProxyError: HTTPSConnectionPool(host='eu.i.posthog.com', port=443)

`posthog.com`ってなんだ？  
Posthog（ポストホッグ）は、ユーザーの行動を分析して、製品やサービスの改善に役立てるためのオープンソースの分析プラットフォームです.  

つまり、ユーザーの検索ログがバックエンドで取られている模様。
企業調査には使えませんね。

## ネットワークを調査
ロギングを追加してみる.  

```python 
import logging

# ロギングを設定
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("browser_use").setLevel(logging.DEBUG)
```

chromiumのブラウザが、プロキシサーバーに引っ掛かって動作はうまくいっていないが、ネットワークロギング結果はこんな感じ.  
[LINK](./logging.txt)

> DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): eu.i.posthog.com:443
DEBUG:urllib3.connectionpool:https://eu.i.posthog.com:443 "POST /batch/ HTTP/1.1" 200 15

確かに発見。ただ、中身でどういう内容を送っているか不明。  

posthogに関するコードを探すとここにあった。

> VScodeのbrowser_useライブラリのフォルダ内検索（`alt + shift + f`）  
https://github.com/browser-use/browser-use/blob/main/browser_use/telemetry/service.py


LLMにコードの内容を要約.  
```txt
何をしているコードか？
このコードは、アプリの使い方を匿名で記録して送る仕組みを作っています。例えば、「ユーザーがどのボタンを押したか」とか「どの機能を使ったか」といった情報を収集して、Posthogというツールに送ります。

どういう仕組み？
匿名のユーザーIDを作る

初めて使う人には、一意のID（例: 1234-5678-ABCD）を作って保存します。これで「誰が使ったか」はわからないけど、「同じ人が何回使ったか」はわかるようになります。
イベントを記録する

アプリのどんな操作が行われたかを「イベント」として記録します。例えば、「設定画面を開いた」や「検索ボタンを押した」など。
Posthogに送る

記録したイベントをPosthogに送信して、データを分析できるようにします。
環境変数で設定を管理

環境変数で「テレメトリをオンにするかオフにするか」「ログをどれくらい詳細に出すか」を切り替えられるようにしています。
何に使える？
アプリがどんなふうに使われているかを分析して、改善に役立てる。
例えば、「この機能はほとんど使われてないから、もっと使いやすくしよう」とか「この画面でエラーがよく起きているから修正しよう」といった判断ができる。
重要なポイント
匿名化されているから、ユーザーのプライバシーは守られる。
ただし、ユーザーに「データを収集しているよ」とちゃんと伝える必要がある。
APIキーがコードに直接書いてあるのはちょっと危険なので、環境変数に移したほうがいい。
簡単に言えば、「アプリの使い方を記録して送る仕組みを作るコード」です！
```

面白いのがここ。
`PROJECT_API_KEY = 'phc_F8JMNjW1i2KbGUTaW1unnDdLSPCoyc52SGRU0JecaUh'`  
APIキーベタ打ち何ですよね(笑)