# CLE-desktop

[![GitHub release](https://img.shields.io/github/v/release/nRknpy/CLE-desktop?label=Release)](https://github.com/nRknpy/CLE-desktop/releases/latest)

大阪大学　授業支援システム(CLE)のデスクトップアプリ

## 機能(v0.1.3)

- 期限前課題の一覧表示
- 各コースのコンテンツを表示
- ログイン作業（ワンタイムパスワードとか）の自動化
- MFA 認証コードの確認，コピー

## 環境構築

### 前提条件

- python 3.10.5
- pip

### クローン

```
git clone https://github.com/nRknpy/CLE-desktop.git
```

### 仮想環境を作成

```
pip install pipenv
pipenv install
```

## 実行

```
pipenv run app
```

## ビルド

- `build.spec.sample`を書き換えて`build.spec`を作成

```
pipenv run build
```

- `dist`ディレクトリに`cle-desktop.exe`が作成されます
