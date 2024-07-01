## プロジェクト名
旅のしおり作成アプリ

## 環境
Python 3.11.7
FastAPI 0.111.0
Uvicorn 0.30.1

## 開発環境構築コマンド
pip install fastapi  
pip install "uvicorn[standard]"  
pip install pyjwt  
pip install "passlib[bcrypt]"  
pip install pydantic-settings

## ディレクトリ構成
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

## 起動コマンド
uvicorn main:app --reload
