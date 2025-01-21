# Machine Learning with Flask

Serve ML models as web APIs using Flask — from simple prediction endpoints to production deployment.

---

## 1. Basic Pattern: Serve a Trained Model

```python
import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load model once at startup (not per-request!)
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = [data['features']]    # e.g. [[5.1, 3.5, 1.4, 0.2]]
    prediction = model.predict(features)
    return jsonify({
        'prediction': prediction.tolist(),
        'status': 'success'
    })
```

### Train & Save the Model

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
import pickle

X, y = load_iris(return_X_y=True)
model = RandomForestClassifier().fit(X, y)

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

### Call the API

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'

# → {"prediction": [0], "status": "success"}
```

---

## 2. With Input Validation

```python
import numpy as np

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    if not data or 'features' not in data:
        return jsonify({'error': 'features required'}), 400
    
    features = data['features']
    if not isinstance(features, list):
        return jsonify({'error': 'features must be a list'}), 400
    
    try:
        arr = np.array(features).reshape(1, -1)
        prediction = model.predict(arr)
        probability = model.predict_proba(arr).max()
        return jsonify({
            'prediction': int(prediction[0]),
            'confidence': round(float(probability), 4),
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

---

## 3. Image Classification (Deep Learning)

```python
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io

app = Flask(__name__)
model = load_model('image_classifier.h5')
labels = ['cat', 'dog', 'bird']

@app.route('/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    img = Image.open(io.BytesIO(file.read()))
    img = img.resize((224, 224))
    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)
    
    preds = model.predict(arr)
    idx = np.argmax(preds)
    
    return jsonify({
        'label': labels[idx],
        'confidence': float(preds[0][idx]),
    })
```

```bash
curl -X POST -F "image=@photo.jpg" http://127.0.0.1:5000/classify
```

---

## 4. NLP / Text Prediction

```python
from transformers import pipeline

classifier = pipeline('sentiment-analysis')

@app.route('/sentiment', methods=['POST'])
def sentiment():
    text = request.get_json().get('text', '')
    result = classifier(text)[0]
    return jsonify({
        'label': result['label'],     # POSITIVE / NEGATIVE
        'score': round(result['score'], 4),
    })
```

---

## 5. Model Loading Strategies

```python
# ❌ BAD — loads model on every request
@app.route('/predict')
def predict():
    model = pickle.load(open('model.pkl', 'rb'))  # SLOW!

# ✅ GOOD — load once at startup
model = pickle.load(open('model.pkl', 'rb'))

# ✅ GOOD — lazy loading with caching
_model = None
def get_model():
    global _model
    if _model is None:
        _model = pickle.load(open('model.pkl', 'rb'))
    return _model

# ✅ BEST — with application factory
def create_app():
    app = Flask(__name__)
    app.model = pickle.load(open('model.pkl', 'rb'))
    
    @app.route('/predict', methods=['POST'])
    def predict():
        pred = app.model.predict(...)
```

---

## 6. Production Architecture

```
Client → Nginx → Gunicorn (4 workers) → Flask + Model
                                           ↓
                                    Redis (caching predictions)
```

### Gunicorn with Preload (share model across workers)

```bash
gunicorn -w 4 --preload -b 0.0.0.0:8000 app:app
```

`--preload` loads the model once in the master process and shares it with all workers (saves memory).

---

## 7. Async Predictions (Heavy Models)

```python
import threading

@app.route('/predict-async', methods=['POST'])
def predict_async():
    task_id = str(uuid.uuid4())
    data = request.get_json()
    
    def run_prediction(tid, features):
        result = heavy_model.predict(features)
        cache[tid] = {'status': 'done', 'result': result.tolist()}
    
    threading.Thread(target=run_prediction, args=(task_id, data['features'])).start()
    return jsonify({'task_id': task_id}), 202

@app.route('/result/<task_id>')
def get_result(task_id):
    return jsonify(cache.get(task_id, {'status': 'processing'}))
```

---

## 8. Common ML Libraries with Flask

| Library | Use Case | Model Format |
|---------|----------|-------------|
| scikit-learn | Classic ML (classification, regression) | `.pkl`, `.joblib` |
| TensorFlow/Keras | Deep learning, images, NLP | `.h5`, SavedModel |
| PyTorch | Deep learning, research | `.pt`, `.pth` |
| XGBoost | Gradient boosting | `.json`, `.pkl` |
| Hugging Face | NLP (transformers) | `pipeline()` |
| ONNX Runtime | Cross-framework inference | `.onnx` |

---

## 9. Project Structure

```
ml_flask_app/
├── app.py              ← Flask API
├── model.py            ← Model loading & prediction logic
├── train.py            ← Training script (generates model file)
├── models/
│   └── model_v1.pkl    ← Trained model
├── requirements.txt
├── Dockerfile
└── tests/
    └── test_api.py
```

---

## 10. Flask vs FastAPI for ML

| Feature | Flask | FastAPI |
|---------|-------|---------|
| Ease of use | ✅ Simple | ✅ Simple |
| Auto docs (Swagger) | ❌ Needs extension | ✅ Built-in |
| Async support | Limited | ✅ Native |
| Type validation | Manual | ✅ Pydantic |
| Community/ecosystem | ✅ Massive | Growing |
| Best for | Simple APIs, prototypes | High-performance APIs |

**Verdict**: Flask is great for serving ML models quickly. For high-throughput production APIs, consider FastAPI.

---

## Key Takeaways

- Load models **once at startup**, never per-request
- Use `--preload` with Gunicorn to share models across workers
- Validate inputs before passing to model
- Return confidence/probability alongside predictions
- Use async patterns for heavy models (threading or Celery)
- Pickle (`.pkl`) for scikit-learn, `.h5` for Keras, `.pt` for PyTorch
