import os
import base64
from io import BytesIO

import requests
from PIL import Image


def get_base_url():
    return os.getenv("FASHION_API_URL", "").rstrip("/")


def generate_image(prompt: str, steps: int = 4, retries: int = 2) -> Image.Image:
    BASE_URL = get_base_url()

    if not BASE_URL:
        raise ValueError("Please enter API URL in sidebar")

    GENERATE_URL = f"{BASE_URL}/generate"

    steps = max(1, min(steps, 4))
    last_error = None

    for _ in range(retries + 1):
        try:
            response = requests.post(
                GENERATE_URL,
                json={"text": prompt, "steps": steps},
                timeout=180,
            )
            response.raise_for_status()

            data = response.json()

            if "image" not in data:
                raise ValueError(f"Invalid API response: {data}")

            img_bytes = base64.b64decode(data["image"])
            return Image.open(BytesIO(img_bytes)).convert("RGB")

        except requests.exceptions.ConnectionError:
            last_error = ConnectionError(f"Cannot reach API at {BASE_URL}")

        except requests.exceptions.Timeout:
            last_error = TimeoutError("Server timeout — model may still be loading")

        except Exception as e:
            last_error = e

    raise last_error


def check_server_health(base_url: str = None) -> bool:
    url = (base_url or get_base_url()).rstrip("/")

    if not url:
        return False

    try:
        r = requests.get(url, timeout=5)
        return r.status_code == 200
    except Exception:
        return False