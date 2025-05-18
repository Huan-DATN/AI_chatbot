
# 🐍 Flask Project - Setup & Run Guide

Hướng dẫn từng bước để khởi tạo, cấu hình và chạy dự án Flask trong môi trường local.

---

## ✅ Yêu cầu hệ thống

- Python 3.8 trở lên
- pip
- Git (nếu clone dự án từ Git)

---

## 🚀 Bắt đầu

### 1. Tạo virtual environment (venv)

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 2. Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

---

### 3. Tạo file `.env` và cấu hình biến môi trường

Tạo một file tên là `.env` trong thư mục gốc của dự án và thêm các dòng sau:

```env
# Database
DB_URL=

# Gemini API
GEMINI_API_KEY=
GEMINI_MODEL=

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

> 💡 Gợi ý: Điền các thông tin kết nối thực tế vào những biến môi trường này. Không commit file `.env` lên Git để tránh lộ thông tin nhạy cảm.

---

### 4. Khởi động ứng dụng

```bash
python run.py
```

Mặc định, ứng dụng sẽ chạy ở địa chỉ `http://localhost:5000`.

## 📝 Ghi chú

- Luôn kích hoạt virtual environment trước khi chạy hoặc phát triển ứng dụng.
- Sử dụng `.env` để quản lý thông tin nhạy cảm một cách an toàn.
- Đảm bảo Redis và các dịch vụ liên quan đã được khởi chạy nếu ứng dụng cần.

---

## 📬 Liên hệ

Nếu bạn gặp vấn đề khi khởi động dự án, hãy kiểm tra kỹ các bước hoặc liên hệ với nhóm phát triển để được hỗ trợ.
