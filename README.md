
---

# README — `bt-netlify-notes`

```md
# bt-netlify-notes (Vue + Netlify Functions + SQL DB) + Docker (Vue + FastAPI + MySQL)

Repo này có 2 phần:
1) Deploy thật trên Netlify: Vue + Netlify Functions + SQL DB (Postgres)
2) Docker local (môi trường khác để đúng yêu cầu “2 môi trường”): Vue + FastAPI + MySQL

Repo này đáp ứng:
- Git/GitHub: branch/merge/conflict + push/clone
- CI/CD: GitHub Actions → trigger Netlify build hook khi `main` thay đổi
- Docker: chạy local bằng `docker compose up --build`

---

## 1) Live Deploy (Netlify)
- Site: https://peaceful-tanuki-62d133.netlify.app
- API test: https://peaceful-tanuki-62d133.netlify.app/api/notes

---

## 2) CI/CD (GitHub Actions → Netlify)
### 2.1 Netlify Build Hook
Netlify site → Project configuration → Build & deploy → Build hooks
- Tạo build hook (branch: `main`)
- Copy URL build hook

### 2.2 Secrets cần có
GitHub repo → Settings → Secrets and variables → Actions

- `NETLIFY_BUILD_HOOK` : URL build hook Netlify

### 2.3 Workflow
File:
- `.github/workflows/deploy-netlify.yml`

Trigger:
- push lên nhánh `main`

Lưu ý:
- Project Vue nằm trong thư mục `app/` nên workflow dùng `working-directory: app`.

### 2.4 Test CI/CD
- Sửa code → commit → push `main`
- GitHub Actions chạy xanh
- Netlify Deploys có build mới
- Mở site thấy thay đổi

---

## 3) Netlify Environment Variables (Deploy)
Netlify site → Project configuration → Environment variables

Cần có:
- `DATABASE_URL` = External Database URL (Postgres) từ provider DB

Sau khi thêm/sửa env:
- Redeploy: Deploys → Trigger deploy → Deploy site

---

## 4) Run Local with Docker (Dev) — Vue + FastAPI + MySQL
### 4.1 Start
```bash
docker compose up -d --build
docker compose ps

-----------------------------------------------------------
Open / Test

Web: http://localhost:5173

API health: http://localhost:8000/api/health

Notes API: http://localhost:8000/api/notes
------------------------------------------------------------------
Stop
docker compose down


Reset sạch DB local:

docker compose down -v