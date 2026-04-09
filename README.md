# AI Hieu Ban — Image Generation Service (Flask)

Internal microservice tao hinh anh nhan vat. Duoc goi boi Node.js backend, KHONG truc tiep tu frontend.

## Kien truc

```
Frontend → Node.js Backend → [Flask Image Service] → (AI Image Model placeholder)
              ↓                        ↓
         Auth, DB, Limits         Generate image
         (gatekeeper)             (replaceable engine)
```

## Yeu cau

- Python >= 3.9
- pip

## Cai dat local

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Service chay tai `http://localhost:5002`

## Environment Variables

| Bien | Mo ta | Mac dinh |
|------|-------|----------|
| `SERVICE_SECRET` | Shared secret voi Node.js backend | `dev-service-secret-change-me` |
| `PORT` | Port chay service | `5002` |

**QUAN TRONG:** `SERVICE_SECRET` phai giong voi `IMAGE_SERVICE_SECRET` trong Node.js backend.

## API Endpoints

| Method | Path | Auth | Mo ta |
|--------|------|------|-------|
| GET | `/health` | - | Health check |
| POST | `/generate` | X-Service-Secret | Generate character image |

### POST /generate

Request (tu Node.js backend):
```json
{
  "prompt": "ve cho minh mot buc anh cute",
  "character_id": "1",
  "character_name": "Linh Chi",
  "character_appearance": "Toc dai den muot, mat nau am ap",
  "style": "portrait"
}
```

Response:
```json
{
  "image_url": "https://api.dicebear.com/9.x/adventurer/svg?seed=abc123&...",
  "caption": "(From Python Image Babe) Day la buc anh minh ve cho ban ne!",
  "style": "portrait"
}
```

### Style options

| Style | Mo ta |
|-------|-------|
| `portrait` | Anh chan dung nhan vat (mac dinh) |
| `scene` | Anh canh/background |
| `selfie` | Anh selfie nhan vat |

### Bao mat

- Chi chap nhan request co header `X-Service-Secret` khop voi `SERVICE_SECRET`
- Tra ve 403 neu secret sai
- Frontend KHONG BAO GIO goi truc tiep service nay

## Deploy len Railway

1. Tao service moi tren Railway tu repo nay
2. Set env vars:
   - `SERVICE_SECRET` = (giong voi `IMAGE_SERVICE_SECRET` cua backend)
   - `PORT` = Railway tu set
3. Railway tu detect Dockerfile va build
4. Copy Railway URL, set vao backend: `IMAGE_SERVICE_URL=https://<railway-url>`

## Thay the AI Model

Khi team AI san sang, sua file `app.py` tai ham `generate_image()`:

```python
# Thay dong nay:
image_url = template.format(seed=seed)

# Bang:
image_url = image_model.generate(
    prompt=prompt,
    character_name=character_name,
    character_appearance=data.get("character_appearance", ""),
    style=style,
)
```

## Chay 4 services local

```bash
# Terminal 1 — Flask Chat Service (localhost:5001)
cd ai-hieu-ban-chat-service
source venv/bin/activate && python app.py

# Terminal 2 — Flask Image Service (localhost:5002)
cd ai-hieu-ban-image-service
source venv/bin/activate && python app.py

# Terminal 3 — Node.js Backend (localhost:3001)
cd ai-hieu-ban-backend
npm run dev:local

# Terminal 4 — Next.js Frontend (localhost:3000)
cd ai-hieu-ban-frontend
npm run dev
```
