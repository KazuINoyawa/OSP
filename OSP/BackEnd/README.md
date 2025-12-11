# OSP Backend

## Yêu cầu
- Python 3.8+
- PostgreSQL

## Cài đặt môi trường
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Cấu hình database
Tạo file `.env` trong thư mục `BackEnd` với nội dung:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=osp_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## Khởi tạo database
Đảm bảo PostgreSQL đã chạy và đã tạo database `osp_db`.

## Chạy server
```bash
cd BackEnd/app
uvicorn main:app --reload
```

## Cấu trúc thư mục
- app/
  - main.py
  - models.py
  - database.py
  - routers/
    - user.py
    - classroom.py
    - assignment.py
    - score.py

## API endpoints
- `/users` - Quản lý người dùng
- `/classes` - Quản lý lớp học
- `/assignments` - Quản lý bài tập
- `/scores` - Quản lý điểm số
