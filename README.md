# AI Fashion Designing Project

An AI-powered fashion design generator that converts text prompts into realistic fashion concepts using diffusion models.

---

## 🚀 Overview

This project allows users to generate clothing designs (e.g., dresses, outfits, couture concepts) from natural language prompts. It is designed for:

* Academic projects
* Interview demonstrations
* AI experimentation in fashion

---

## 🧠 Key Features

* Powered by **SDXL Turbo** (fast, low-latency text-to-image generation)
* Text-to-image fashion generation
* FastAPI-based API
* Colab support for GPU execution
* Tunnel-based access for remote usage
* Built-in prompt enhancement for better fashion outputs

---

## 🏗️ Project Structure

```text
AI-FASHION/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── fashion_brain.py   # (Optional/extended) prompt logic
│   ├── generator.py       # (Optional modular version)
│   ├── main.py            # FastAPI entry (local structure)
│   ├── state.py           # State handling
│   └── __pycache__/
│
├── assets/
│
├── colab/
│   └── run.ipynb          # Main execution environment
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚠️ Hardware Problem (IMPORTANT)

### The Reality

Even though **SDXL Turbo** is optimized for speed, it still requires:

* GPU acceleration
* Moderate VRAM

Running locally on CPU:

* ❌ Slow generation
* ❌ High memory usage
* ❌ Not suitable for real-time results

---

## ✅ Solution Used in This Project

### 👉 Google Colab + ngrok Tunnel

This project avoids hardware limitations by offloading computation to the cloud.

**Flow:**

1. Model runs on **Google Colab GPU**
2. FastAPI backend runs inside Colab
3. ngrok exposes the local server
4. Requests are sent via public URL

👉 Result: Works on **any machine**, regardless of hardware

---

## ▶️ How to Run the Project

## 🔹 Run using Colab (Recommended)

### Step 1: Open Notebook

* Open `colab/run.ipynb`
* Upload to Google Colab
* Enable GPU runtime

---

### Step 2: Install Dependencies

```bash
!pip uninstall -y diffusers transformers accelerate huggingface_hub peft

!pip install --no-cache-dir \
  diffusers==0.29.2 \
  transformers==4.41.2 \
  accelerate==0.31.0 \
  huggingface_hub==0.23.4 \
  peft>=0.11.1 \
  safetensors==0.4.3 \
  fastapi uvicorn pyngrok pillow
```

---

### Step 3: Create Backend (app.py)

Using:

```python
%%writefile app.py
```

This defines:

* FastAPI server
* SDXL Turbo pipeline
* `/generate` endpoint
* Prompt enhancement logic

---

### Step 4: Setup ngrok

```python
from pyngrok import ngrok
ngrok.set_auth_token("<your-ngrok-auth-token>")
```

---

### Step 5: Start Server

```python
import subprocess

subprocess.Popen([
    "uvicorn", "app:app",
    "--host", "0.0.0.0",
    "--port", "8000"
])
```

---

### Step 6: Expose API

```python
public_url = ngrok.connect(8000)
print(public_url)
```

---

### Step 7: Use API

* Copy public URL
* Send requests from frontend or Postman

---

## 📡 API Endpoint

### `POST /generate`

**Input:**

```json
{
  "text": "modern black streetwear hoodie with neon accents"
}
```

**Output:**

* Base64 encoded image
* Enhanced prompt used
* Steps used

---

## 🧩 How the System Works (ACCURATE FLOW)

1. User sends a POST request to `/generate` with input text
2. FastAPI receives the request and validates it using Pydantic model
3. Input prompt is **enhanced** by appending fashion-specific keywords
4. SDXL Turbo pipeline (loaded on GPU in Colab) is invoked with:

   * `num_inference_steps` (1–4)
   * `guidance_scale = 0.0` (required for Turbo)
   * negative prompt for quality control
5. Model generates an image in a single forward pass (Turbo optimization)
6. Image is converted to **base64 format**
7. API returns:

   * generated image
   * final prompt used
   * steps value

---

## 🐞 Common Issues

### ❌ Model crashes

→ Ensure GPU runtime is enabled

### ❌ Slow output

→ You are likely on CPU instead of GPU

### ❌ Tunnel not working

→ Restart ngrok after backend starts

---

## 💡 Example Prompt

```
Luxury royal blue gown with silk texture, high fashion runway style
```

---

## 📌 Final Note

This project is optimized for:

* Fast generation
* Low-latency AI applications
* Interview demonstrations

Not intended for production-scale deployment.

---

## 👤 Author

Satvik Miglani
