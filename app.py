"""
AI Hieu Ban — Image Generation Service (Flask)
Internal service called by Node.js backend to generate character images.
Auth: service-to-service shared secret (not user-facing).
"""

import os
import random
import time
import hashlib
from functools import wraps

from flask import Flask, request, jsonify

app = Flask(__name__)

SERVICE_SECRET = os.environ.get("SERVICE_SECRET", "dev-service-secret-change-me")
PORT = int(os.environ.get("PORT", "5002"))

# ── Mock image URLs (DiceBear avatars with different styles) ────────────

MOCK_CHARACTER_IMAGES = [
    "https://api.dicebear.com/9.x/adventurer/svg?seed={seed}&backgroundColor=ffd5dc&size=512",
    "https://api.dicebear.com/9.x/adventurer/svg?seed={seed}&backgroundColor=e8d5f5&size=512",
    "https://api.dicebear.com/9.x/adventurer/svg?seed={seed}&backgroundColor=d4f5d0&size=512",
    "https://api.dicebear.com/9.x/adventurer/svg?seed={seed}&backgroundColor=c0e8ff&size=512",
    "https://api.dicebear.com/9.x/adventurer/svg?seed={seed}&backgroundColor=fed7aa&size=512",
    "https://api.dicebear.com/9.x/adventurer/svg?seed={seed}&backgroundColor=bfdbfe&size=512",
    "https://api.dicebear.com/9.x/adventurer/svg?seed={seed}&backgroundColor=ddd6fe&size=512",
    "https://api.dicebear.com/9.x/adventurer/svg?seed={seed}&backgroundColor=bbf7d0&size=512",
]

MOCK_SCENE_IMAGES = [
    "https://api.dicebear.com/9.x/shapes/svg?seed={seed}&backgroundColor=ffd5dc&size=512",
    "https://api.dicebear.com/9.x/shapes/svg?seed={seed}&backgroundColor=e8d5f5&size=512",
    "https://api.dicebear.com/9.x/shapes/svg?seed={seed}&backgroundColor=d4f5d0&size=512",
    "https://api.dicebear.com/9.x/shapes/svg?seed={seed}&backgroundColor=c0e8ff&size=512",
]

MOCK_IMAGE_CAPTIONS = [
    "(From Python Image Babe) Day la buc anh minh ve cho ban ne! Hy vong ban thich.",
    "(From Python Image Babe) Minh da tao mot buc anh dac biet danh rieng cho ban.",
    "(From Python Image Babe) Xem buc anh nay nhe! Minh ve bang ca tam long day.",
    "(From Python Image Babe) Buc anh nay the hien cam xuc cua minh danh cho ban.",
    "(From Python Image Babe) Minh muon gui ban buc anh nay nhu mot mon qua nho.",
]


# ── Service auth decorator ─────────────────────────────────────────────

def require_service_auth(f):
    """Verify X-Service-Secret header matches our shared secret."""
    @wraps(f)
    def decorated(*args, **kwargs):
        secret = request.headers.get("X-Service-Secret", "")
        if secret != SERVICE_SECRET:
            return jsonify({"error": "Unauthorized service call"}), 403
        return f(*args, **kwargs)
    return decorated


# ── Helpers ─────────────────────────────────────────────────────────────

def generate_seed(prompt: str, character_name: str) -> str:
    """Generate a deterministic seed from prompt + character for consistent results."""
    raw = f"{character_name}_{prompt}_{random.randint(1, 10000)}"
    return hashlib.md5(raw.encode()).hexdigest()[:10]


# ── Routes ──────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "image-service", "engine": "mock"})


@app.route("/generate", methods=["POST"])
@require_service_auth
def generate_image():
    """
    Generate a character image.
    Called by Node.js backend (not directly by frontend).

    Request body:
    {
        "prompt": "user's message or image description",
        "character_id": "1",
        "character_name": "Linh Chi",
        "character_appearance": "Toc dai den muot...",
        "style": "portrait" | "scene" | "selfie"  (optional, default: "portrait")
    }

    Response:
    {
        "image_url": "https://...",
        "caption": "response text about the image",
        "style": "portrait"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400

    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Empty prompt"}), 400

    character_name = data.get("character_name", "Character")
    style = data.get("style", "portrait")

    # Simulate generation delay (2-5s, image gen is slower than chat)
    time.sleep(random.uniform(2.0, 5.0))

    # Generate a unique seed for this request
    seed = generate_seed(prompt, character_name)

    # Pick image URL based on style
    if style == "scene":
        template = random.choice(MOCK_SCENE_IMAGES)
    else:
        template = random.choice(MOCK_CHARACTER_IMAGES)

    image_url = template.format(seed=seed)
    caption = random.choice(MOCK_IMAGE_CAPTIONS)

    # TODO: Replace with actual AI image generation model
    # image_url = image_model.generate(
    #     prompt=prompt,
    #     character_name=character_name,
    #     character_appearance=data.get("character_appearance", ""),
    #     style=style,
    # )

    return jsonify({
        "image_url": image_url,
        "caption": caption,
        "style": style,
    })


if __name__ == "__main__":
    print(f"🎨 Image Service dang chay tai http://localhost:{PORT}")
    print(f"🤖 Engine: mock (placeholder cho AI image generation)")
    app.run(host="0.0.0.0", port=PORT, debug=True)
