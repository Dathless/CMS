# Hệ Thống Quản Lý Khoá Học (Course Management System)

## Giới Thiệu

Hệ thống quản lý khoá học là một ứng dụng web full-stack cho phép quản lý các khoá học, giảng viên, sinh viên với các phân quyền rõ ràng. Dự án được thiết kế với cấu trúc tách biệt giữa Backend (BE) và Frontend (FE), sử dụng SQLite làm cơ sở dữ liệu để dễ dàng phát triển và triển khai.

Dự án hỗ trợ:

- Đăng ký, đăng nhập với JWT Authentication (Access Token + Refresh Token).
- CRUD cho các thực thể chính.
- Phân quyền chi tiết theo vai trò: Admin, Giảng viên, Sinh viên.
- Giao diện riêng biệt cho từng role.
- Tính mở rộng cao để dễ dàng thêm tính năng mới.

## Cấu Trúc Dự Án

```
course-management-system/
├── README.md                    # Tài liệu dự án
├── .gitignore                   # Git ignore rules (root)
├── be/                          # Backend (Python + FastAPI)
│   ├── venv/
|   ├── database.db
│   └── requirements.txt         # Dependencies cho BE
└── fe/                          # Frontend (React + TypeScript + Vite)
```

### Chi Tiết Thư Mục

- **be/**: Chứa toàn bộ mã nguồn backend (Python + FastAPI).
  - `app/main.py`: Entry point của ứng dụng FastAPI.
  - `app/core/`: Cấu hình, bảo mật, kết nối database.
  - `app/models/`: SQLAlchemy models định nghĩa cấu trúc bảng (SQLite).
  - `app/schemas/`: Pydantic models cho request/response validation.
  - `app/crud/`: Các thao tác CRUD tương ứng với từng model.
  - `app/routers/`: API endpoints được phân chia theo module (auth, courses, users, enrollments, grades).
  - `app/dependencies/`: Các dependency như xác thực JWT, phân quyền.
  - `tests/`: Unit và integration tests.
  - `requirements.txt`: Danh sách thư viện Python cần cài đặt.

- **fe/**: Chứa mã nguồn frontend (React + TypeScript + Vite).
  - `src/main.tsx`: Entry point của ứng dụng React.
  - `src/App.tsx`: Component root.
  - `src/components/`: Các component tái sử dụng (Layout).
  - `src/contexts/`: React contexts (AuthContext cho xác thực, ThemeContext cho chủ đề).
  - `src/pages/`: Các trang tương ứng theo role (AdminDashboard, LecturerDashboard, StudentDashboard, Login, Profile).
  - `src/services/`: Các module gọi API thông qua Axios.

## Tech Stack

### Backend

- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite (file-based: `be/app/database.db`)
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (PyJWT) với Access Token (15 phút) + Refresh Token (7 ngày)
- **Validation**: Pydantic
- **Security**: OAuth2PasswordBearer, bcrypt cho password hashing
- **Virtual Environment**: `venv` (khuyến nghị)

### Frontend

- **Framework**: React.js (v18) + Vite
- **UI Library**: Ant Design (hoặc Tailwind CSS + shadcn/ui cho thiết kế hiện đại)
- **State Management**: React Context + useReducer (hoặc Redux Toolkit nếu phức tạp)
- **HTTP Client**: Axios
- **Routing**: React Router DOM v6

### DevOps

- **Package Manager**: pip (BE), npm/yarn (FE)
- **Linting/Formatting**: Ruff (BE), ESLint + Prettier (FE)
- **Containerization**: Docker + Docker Compose (tùy chọn)

## Cài Đặt và Chạy Dự Án

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### Backend Setup

```bash
cd be

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Cài dependencies
pip install -r requirements.txt

# Khởi tạo database
python -m app.core.init_db  # Hoặc chạy migrate nếu dùng Alembic

# Chạy server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd fe
npm install
npm run dev
```

Mở trình duyệt: `http://localhost:5173` (default Vite port).

### Tài Khoản Mẫu (Seed Data)

- **Admin**: `admin1` / `123456`
- **Giảng viên**: `giangvien1` / `123456`
- **Sinh viên**: `sinhvien1` / `123456`

Dữ liệu seed được tự động chèn khi khởi tạo DB.

## Chức Năng Chính

### Authentication & Authorization

- Đăng ký tài khoản (chọn role: student/lecturer).
- Đăng nhập với username/password.
- JWT: Access Token (short-lived) + Refresh Token (long-lived, stored securely).
- Middleware kiểm tra role và permissions cho từng endpoint.

### Vai Trò và Quyền Hạn

#### 1. Quản Lý (Admin)

- Dashboard tổng quan: Thống kê số khoá học, sinh viên, giảng viên.
- Quản lý Users:
  - Xem, sửa, xoá tài khoản Giảng viên & Sinh viên.
- Quản lý Khoá Học:
  - Tạo mới, sửa, xoá bất kỳ khoá học nào.
- Xem logs hoạt động (audit).

#### 2. Giảng Viên (Lecturer)

- Dashboard cá nhân: Danh sách khoá học đang dạy.
- Đăng ký dạy khoá học mới (gửi request hoặc trực tiếp tạo nếu có quyền).
- Quản lý khoá học của mình:
  - Duyệt sinh viên đăng ký tham gia.
  - CRUD sinh viên trong khoá (thêm/xoá, cập nhật thông tin).
  - Chấm điểm, quản lý tiến độ học tập.
- Xem profile cá nhân.

#### 3. Sinh Viên (Student)

- Dashboard: Danh sách khoá học đang học + khoá học gợi ý.
- Đăng ký khoá học (tìm kiếm và join).
- Xem/sửa thông tin cá nhân.
- Xem điểm số, tài liệu khoá học, tiến độ.

### Các Chức Năng Khác (Bổ Sung)

- Tìm kiếm khoá học (filter theo tên, giảng viên, trạng thái).
- Upload tài liệu cho khoá học (file storage đơn giản).
- Thông báo (in-app notifications).
- Báo cáo (export CSV danh sách sinh viên/khoá học).
- Responsive UI cho mobile.

## Thiết Kế Database (SQLite)

Các bảng chính (SQLAlchemy models):

- **users**: id, username, password_hash, email, full_name, role (admin/lecturer/student), created_at.
- **courses**: id, title, description, lecturer_id (FK), start_date, end_date, status.
- **enrollments**: id, student_id (FK), course_id (FK), status (pending/approved/rejected), enrolled_at.
- **grades**: id, enrollment_id (FK), score, feedback, graded_at.
- **refresh_tokens**: id, user_id, token, expires_at (cho blacklisting nếu cần).

Mối quan hệ:

- 1 Lecturer - N Courses
- 1 Student - N Courses (qua Enrollments)
- 1 Course - N Students (qua Enrollments)

Schema được thiết kế chuẩn hóa, dễ mở rộng (thêm modules như assignments, quizzes sau).

## API Endpoints (Ví Dụ)

- `POST /auth/login` → JWT tokens
- `POST /auth/refresh`
- `GET /users/me` (protected)
- `CRUD /courses`, `/users`, `/enrollments`

Xem chi tiết trong `be/app/routers/`.

## Tính Mở Rộng

- **Scalability**: Dễ migrate sang PostgreSQL/MySQL.
- **Microservices ready**: Tách services nếu cần (Auth Service, Course Service).
- **Testing**: Unit tests với pytest, integration tests.
- **CI/CD**: GitHub Actions template sẵn.
- **Deployment**: Docker, Vercel (FE), Render/Heroku (BE), hoặc self-host.
- **Future Features**:
  - Video streaming integration.
  - Real-time chat (WebSocket).
  - Payment gateway cho khoá học có phí.
  - Analytics dashboard nâng cao.

## Contributing

1. Fork project.
2. Tạo branch feature/new-feature.
3. Commit và push.
4. Tạo Pull Request.

## License

MIT License.

---

**Lưu ý**:

- Password mặc định `123456` chỉ dùng cho demo. Trong production, bắt buộc thay đổi và dùng hashing mạnh.
- Đảm bảo bảo mật Refresh Token (HttpOnly cookie hoặc secure storage).
- Project được thiết kế để dễ hiểu, maintain và scale.
