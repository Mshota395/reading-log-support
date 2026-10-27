#!/usr/bin/env python3
"""Build the public static documentation. No app source or user records belong here."""
import html
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://mshota395.github.io/reading-log-support/"
STYLE_REVISION = hashlib.sha256((ROOT / "assets/style.css").read_bytes()).hexdigest()[:12]


def page(title, body, route="", active=""):
    prefix = "../" if route else "./"
    def nav(label, path, key):
        current = ' aria-current="page"' if key == active else ""
        return f'<a href="{prefix}{path}"{current}>{label}</a>'
    document = f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="読書記録アプリのプライバシーポリシーとサポート案内。">
<meta name="referrer" content="no-referrer"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self'; img-src 'self'; base-uri 'none'; form-action 'none'; object-src 'none'">
<title>{html.escape(title)} · 読書記録</title><link rel="canonical" href="{SITE}{route}">
<link rel="icon" href="{prefix}assets/app-icon.png"><link rel="stylesheet" href="{prefix}assets/style.css?v={STYLE_REVISION}"></head>
<body><a class="skip" href="#main">本文へ移動</a><header><div class="wrap bar"><a class="brand" href="{prefix}"><img src="{prefix}assets/app-icon.png" alt="" width="46" height="46"><span>読書記録<small>READING LOG / SUPPORT</small></span></a><nav aria-label="メインナビゲーション">{nav('ホーム','','home')}{nav('プライバシー','privacy/','privacy')}{nav('サポート','support/','support')}</nav></div></header>
<main id="main"><div class="wrap">{body}</div></main><footer><div class="wrap"><div class="footer-row"><span>© 2026 Mshota395</span><div class="footer-links"><a href="{prefix}privacy/">プライバシーポリシー</a><a href="{prefix}support/">サポート</a></div></div><p>このサイトはGitHub Pagesを利用しています。アクセス時の接続情報の扱いは<a href="https://docs.github.com/site-policy/privacy-policies/github-privacy-statement">GitHubのプライバシーに関する声明</a>もご確認ください。このサイトにアクセス解析・広告・問い合わせフォームは設置していません。</p></div></footer></body></html>'''
    destination = ROOT / route / "index.html"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(document)


def inline(text):
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return re.sub(r"\[([^\]]+)\]\((https://[^\s)]+)\)", r'<a href="\2">\1</a>', escaped)


def markdown(text):
    chunks, paragraph = [], []
    def flush():
        if paragraph:
            chunks.append("<p>" + inline(" ".join(paragraph)) + "</p>")
            paragraph.clear()
    for line in text.splitlines():
        if not line.strip():
            flush()
        elif line.startswith("## "):
            flush(); chunks.append("<h2>" + inline(line[3:]) + "</h2>")
        elif line.startswith("# "):
            flush(); chunks.append("<h1>" + inline(line[2:]) + "</h1>")
        elif line.startswith("- "):
            flush(); chunks.append("<p>・" + inline(line[2:]) + "</p>")
        else:
            paragraph.append(line)
    flush()
    return "\n".join(chunks)


page("公式サポート", '''<section class="hero"><div><div class="eyebrow">YOUR BOOKS, YOUR OWN RECORD.</div><h1>本と過ごした時間を、<br>自分の記録に。</h1><p class="lead">読書記録アプリのプライバシーと、使い方について。<br>大切な記録を扱う前に、ご確認ください。</p></div><img class="hero-icon" src="./assets/app-icon.png" alt="3冊の本を描いた読書記録のアイコン" width="180" height="180"></section><div class="cards"><section class="card"><span class="number">01</span><h2>プライバシー</h2><p>端末内の保存、外部サービスとの通信、バックアップ、記録の削除について説明します。</p><a href="./privacy/">プライバシーポリシーを読む →</a></section><section class="card"><span class="number">02</span><h2>サポート</h2><p>よくある質問と、問い合わせ窓口の準備状況を案内します。</p><a href="./support/">サポート案内を見る →</a></section></div><aside class="note">現在は開発版です。問い合わせ用メールアドレスは準備中です。一般公開・配布の前に、このページで窓口をご案内します。</aside>''', active="home")

policy = (ROOT / "PRIVACY.md").read_text()
page("プライバシーポリシー", '<article class="article"><div class="eyebrow">PRIVACY POLICY</div>' + markdown(policy) + '</article>', "privacy/", "privacy")

page("サポート", '''<article class="article"><div class="eyebrow">HELP & SUPPORT</div><h1>サポート</h1><p class="lead">読書記録の使い方と、データの扱いについて。</p><section class="note"><strong>問い合わせ用メールは準備中です。</strong><p>現在は開発版です。窓口の用意ができ次第、このページにメールアドレスを掲載します。個人情報やメモ本文、バックアップファイルを公開の場所へ投稿しないでください。</p></section><h2>よくある質問</h2><details><summary>今後、広告が表示される予定はありますか？</summary><p>将来の更新で広告と広告非表示の買い切りを導入する可能性があります。現在は広告SDKや購入機能を組み込んでいません。導入時にはプライバシーポリシー等を更新し、必要な許可や選択方法を案内します。読書メモや読書履歴を広告配信に渡さない方針です。</p></details><details><summary>記録はどこに保存されますか？</summary><p>このiPhoneのアプリ内に保存します。開発者のサーバーへ本棚やメモを送信しません。OSのバックアップに含まれる場合は、Appleの設定に従います。</p></details><details><summary>インターネットなしでも使えますか？</summary><p>手入力登録、記録、メモ、端末内検索はオフラインで利用できます。書籍検索や、オンにした表紙取得には通信が必要です。</p></details><details><summary>表紙をオンラインで取得したくありません。</summary><p>「設定」→「プライバシー」→「表紙画像をオンラインで取得」をオフにします。初期状態もオフです。</p></details><details><summary>バックアップはどう作りますか？</summary><p>「設定」→「取り込み・バックアップ・復元」からJSONを書き出せます。メモを含む全記録が入り、暗号化はされません。自分だけがアクセスできる場所に保存してください。</p></details><details><summary>CSVを取り込めません。</summary><p>UTF-8で保存し、title列を含めてください。ファイルは8 MiB以下、1回5,000行までです。重複候補が多い場合もファイルを分割してください。上限や検証エラーがある場合、保存済みデータは変更しません。</p></details><details><summary>アプリを削除すると記録は消えますか？</summary><p>アプリの削除で端末内の保存データも削除されます。先にバックアップしてください。OSバックアップや書き出したコピーは別途管理してください。開発者は紛失した記録を復旧できません。</p></details><details><summary>カメラを許可しなくても登録できますか？</summary><p>はい。カメラはISBNバーコードの読み取りにだけ使います。許可せずに検索・手入力で登録できます。</p></details><p class="meta">開発者：Mshota395 / 最終更新：2026年10月27日</p><p><a href="../privacy/">データの扱いを詳しく確認する →</a></p></article>''', "support/", "support")
print("Built index.html, privacy/index.html, support/index.html")
