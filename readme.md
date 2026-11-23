
Для установки необходимых зависимостей в окружение
```
pip install -r requirements.txt
```

Для запуска приложения используйте
```
uvicorn app.main:app --reload --reload-exclude ".venv/*" --port 8080
```

## Swagger
http://localhost:8080/docs