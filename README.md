# GrubOS

Snap a photo of your ingredients, get recipes instantly. GrubOS uses computer vision to detect ingredients in your fridge or on your counter, then generates recipes using a local LLM.

## Architecture

```
Image Upload ──▶ YOLOv8 (ingredient detection) ──▶ Ingredient List
                                                         │
                                                         ▼
                                               Ollama / Llama 3.2
                                                         │
                                                         ▼
                                                  Streamed Recipes
```

- **Backend** -- FastAPI serving a YOLOv8 vision model and an Ollama LLM client
- **Frontend** -- React + Vite + Tailwind CSS

## Prerequisites

| Dependency | Version | Notes |
|---|---|---|
| Python | 3.11+ | |
| Node.js | 18+ | |
| [Ollama](https://ollama.com/) | latest | Install from ollama.com |

## Quick Start

### 1. Clone and install

```bash
git clone <repo-url> && cd GrubOS
```

**Backend:**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**

```bash
cd frontend
npm install
```

### 2. Pull the LLM model

```bash
ollama pull llama3.2:3b
```

Make sure Ollama is running (`ollama serve` or the Ollama desktop app).

### 3. Start the backend

```bash
cd backend
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`. Visit `/docs` for the interactive Swagger UI.

### 4. Start the frontend

```bash
cd frontend
npm run dev
```

Open `http://localhost:5173` in your browser.

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/detect` | Upload an image, returns detected ingredients with bounding boxes |
| `POST` | `/api/recipes` | Send ingredient list + preferences, returns streamed recipe text |
| `GET` | `/api/health` | Health check (vision model loaded, Ollama reachable) |

## Fine-Tuning the Vision Model

The pre-trained YOLOv8 model knows general COCO object classes. To specialize it for grocery/ingredient detection, fine-tune on a custom dataset.

### Prepare a dataset

Use a YOLO-format dataset (e.g., from [Roboflow](https://roboflow.com/)). The directory structure should look like:

```
data/
  my_dataset/
    dataset.yaml
    train/
      images/
      labels/
    valid/
      images/
      labels/
```

### Run training

```bash
python scripts/train.py --data data/my_dataset/dataset.yaml
```

Options:

```
--model    Base model (default: yolov8s.pt)
--epochs   Training epochs (default: 50)
--imgsz    Image size (default: 640)
--batch    Batch size (default: 16)
--device   cpu, 0, 0,1, or mps (default: auto)
```

Trained weights are saved to `data/weights/best.pt` and automatically picked up by the backend on next start.

## Project Structure

```
GrubOS/
  backend/
    app/
      main.py              # FastAPI entry point
      routers/
        detect.py          # /api/detect endpoint
        recipes.py         # /api/recipes endpoint
      services/
        vision.py          # YOLOv8 wrapper
        llm.py             # Ollama client + prompt template
      models/
        schemas.py         # Pydantic request/response models
    requirements.txt
  frontend/
    src/
      App.jsx              # Main app shell
      components/
        ImageUpload.jsx    # Drag-and-drop image upload
        IngredientList.jsx # Editable ingredient tags
        RecipeCard.jsx     # Streamed recipe display
      api/
        client.js          # API fetch wrappers
  scripts/
    train.py               # YOLOv8 fine-tuning CLI
  data/                    # Datasets & weights (gitignored)
```

