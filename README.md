## プロジェクト名
旅のしおり作成アプリ

## 環境
Python 3.11.7
FastAPI 0.111.0
Uvicorn 0.30.1

## ディレクトリ構成
<pre>
.
├── README.md
├── __init__.py
├── __pycache__
├── auth.py
├── config.py
├── database.py
├── main.py
├── routers
│   ├── __init__.py
│   ├── __pycache__
│   ├── guides.py
│   ├── map.py
│   └── users.py
└── travel_guide.db
</pre>

## 環境構築コマンド
pip install fastapi  
pip install "uvicorn[standard]"  
pip install pyjwt  
pip install "passlib[bcrypt]"  
pip install pydantic-settings

## 環境変数(.envファイル)
- トークンキー(文字列)
SECRET_KEY
- トークンアルゴリズム(文字列)
ALGORITHM
- トークン有効期限(数値)
ACCESS_TOKEN_EXPIRE_MINUTES
- 画面URL(文字列)
BROWSER_URL

## 起動コマンド
uvicorn main:app --reload
