from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # ヘッドフルモードでブラウザを起動
    browser = p.chromium.launch(
        headless=False,  # ヘッドレスモードをオフにする
        proxy={
            "server": "http://proxy.km.local:8080",
            "username": "kosuke.usui",
            "password": "JrqV3ngt"
        }
    )
    
    # 新しいページを開く
    page = browser.new_page()
    
    # Googleにアクセス
    page.goto('https://www.google.com')
    
    # スクリーンショットを保存
    page.screenshot(path='screenshot.png')
    
    # ブラウザを閉じる
    browser.close()
