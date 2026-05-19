from flask import Flask, render_template, request, jsonify, send_from_directory
import os, json
import requests as req_lib
from dotenv import load_dotenv

load_dotenv()   # loads .env locally; on Render/Railway uses env vars directly

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL   = "llama-3.3-70b-versatile"


# ── Groq helper ───────────────────────────────────────────────────────────────
def groq_chat(system_prompt, messages, max_tokens=600, temperature=0.6):
    """Server-side Groq call — API key never leaves the server."""
    if not GROQ_API_KEY:
        return "⚠️ GROQ_API_KEY not configured. Add it to your .env file and restart."
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type":  "application/json",
    }
    payload = {
        "model":       GROQ_MODEL,
        "messages":    [{"role": "system", "content": system_prompt}] + messages,
        "temperature": temperature,
        "max_tokens":  max_tokens,
    }
    resp = req_lib.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


# ── Static files ──────────────────────────────────────────────────────────────
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, "static"), filename)


# ── Topic metadata ────────────────────────────────────────────────────────────
TOPICS = [
    {
        "id": "convolution", "icon": "⊕", "title": "Convolution",
        "subtitle": "Filters, kernels & feature maps",
        "desc": "Watch a filter slide across an image step by step. Understand stride, padding, and why parameter sharing makes CNNs so powerful.",
        "color": "#7C3AED", "glow": "rgba(124,58,237,0.35)", "badge": "Foundation", "sections": 5,
    },
    {
        "id": "pooling", "icon": "⬇", "title": "Pooling",
        "subtitle": "Downsampling & invariance",
        "desc": "Max pool, average pool, global average pool. See how pooling cuts computation and adds translation invariance — interactively.",
        "color": "#0EA5E9", "glow": "rgba(14,165,233,0.35)", "badge": "Foundation", "sections": 4,
    },
    {
        "id": "activation", "icon": "⚡", "title": "Activation Functions",
        "subtitle": "ReLU, GELU, Swish & more",
        "desc": "Without non-linearity, 100 layers equals one. Visualise every activation curve, compare gradients, and learn when to use each.",
        "color": "#F59E0B", "glow": "rgba(245,158,11,0.35)", "badge": "Foundation", "sections": 4,
    },
    {
        "id": "training", "icon": "🎯", "title": "Training CNNs",
        "subtitle": "Backprop, loss & optimisers",
        "desc": "Gradient descent, backpropagation, Adam vs SGD, BatchNorm, Dropout. Run a live loss curve simulator.",
        "color": "#EF4444", "glow": "rgba(239,68,68,0.35)", "badge": "Advanced", "sections": 6,
    },
    {
        "id": "architectures", "icon": "🏛", "title": "Architectures",
        "subtitle": "LeNet → ResNet → EfficientNet",
        "desc": "30 years of CNN breakthroughs. Interactive timeline, ResNet skip-connection animation, and accuracy vs params comparison.",
        "color": "#10B981", "glow": "rgba(16,185,129,0.35)", "badge": "Advanced", "sections": 5,
    },
    {
        "id": "codeLab", "icon": "💻", "title": "Code Lab",
        "subtitle": "PyTorch & TensorFlow side-by-side",
        "desc": "Build a full CNN from scratch in both frameworks. Every line explained. Transfer learning, inference, saving models — all covered.",
        "color": "#6366F1", "glow": "rgba(99,102,241,0.35)", "badge": "PT & TF", "sections": 5,
    },
    {
        "id": "data-augmentation", "icon": "🔀", "title": "Data Augmentation",
        "subtitle": "Transforms & regularisation",
        "desc": "Flip, rotate, crop, colour-jitter, CutOut, MixUp, RandAugment — interactive augmentation playground with PyTorch & Keras code.",
        "color": "#EC4899", "glow": "rgba(236,72,153,0.35)", "badge": "Advanced", "sections": 5,
    },
]


# ── Page-wise context for Neelu ───────────────────────────────────────────────
PAGE_CONTEXT = {
    "/": (
        "Home page of the GUVI CNN Study app. Lists 7 modules: Convolution, Pooling, "
        "Activation Functions, Training CNNs, Architectures, Code Lab, Data Augmentation. "
        "There is also a Quiz page. Learners click a topic card to enter that module. "
        "The nav bar has links to every module and a Quiz button."
    ),
    "/convolution": (
        "Convolution module (5 sections). Covers: kernels/filters, element-wise multiply-and-sum, "
        "feature maps, stride, padding, parameter sharing, receptive field, output size formula. "
        "INTERACTIVE DEMO: a 6×6 input grid and an output grid. "
        "Click 'Next Step' to move the kernel one position at a time. "
        "The purple cells show the active input patch; amber cell shows the value being computed. "
        "Dropdowns let you switch kernel type (Edge Detect, Blur, Sharpen, Identity), "
        "stride (1 or 2), and padding (None or Same). "
        "The computation panel shows the full element-wise multiply equation live."
    ),
    "/pooling": (
        "Pooling module (4 sections). Covers: max pooling, average pooling, global average pooling, "
        "translation invariance, downsampling, output size formula ⌊(N−F)/S⌋+1. "
        "INTERACTIVE DEMO: a 6×6 feature map with a sliding pool window. "
        "Click 'Next Step' to advance the window. "
        "Blue cells = active window, green = computed output, amber = current output being written. "
        "Dropdowns: Pool Type (Max / Average), Window size (2×2 or 3×3), Stride (1 or 2). "
        "The max value in the window is highlighted darker blue."
    ),
    "/activation": (
        "Activation Functions module (4 sections). Covers: why non-linearity is needed, "
        "ReLU, Leaky ReLU, Sigmoid, Tanh, GELU, Swish, dead neurons, vanishing gradients. "
        "INTERACTIVE DEMO: click any function card (ReLU, Leaky ReLU, Sigmoid, Tanh, GELU, Swish) "
        "to load it into the plotter. Each card shows a mini sparkline. "
        "Drag the x-slider to set the input value — both f(x) and f′(x) (gradient) canvases "
        "update live with a dot showing the exact value. "
        "A 'Show' dropdown lets you display Function only, Gradient only, or both. "
        "The output chip shows the exact numerical output and gradient at the current x."
    ),
    "/training": (
        "Training CNNs module (6 sections). Covers: forward pass, loss functions "
        "(cross-entropy, MSE, focal), backpropagation, chain rule, "
        "SGD / Momentum / Adam / AdamW optimisers, BatchNorm, Dropout, "
        "LR scheduling, data augmentation overview, weight initialisation. "
        "INTERACTIVE DEMO (Loss Curve Simulator): "
        "Choose Optimiser (SGD/Momentum/Adam/AdamW) and Problem scenario "
        "(Healthy Training / Overfitting / LR Too High / LR Too Low / Underfitting). "
        "Set Learning Rate, Dropout Rate, and number of Epochs with sliders. "
        "Click 'Run Training' to animate the train + val loss curves. "
        "Stats chips show current epoch, train loss, val loss, and status. "
        "Click Reset to clear and reconfigure."
    ),
    "/architectures": (
        "Architectures module (5 sections). Covers CNN evolution: "
        "LeNet (1998) → AlexNet (2012) → VGG (2014) → ResNet (2015) → MobileNet (2017) → EfficientNet (2019). "
        "INTERACTIVE DEMO (Architecture Explorer): "
        "Click any timeline card to load that architecture. "
        "Use the 'Architecture' dropdown to switch, and the 'Show' dropdown to change view: "
        "  - Layer Diagram: visual block strip, click a block to inspect its details in the panel below "
        "  - Param Comparison: horizontal bar chart for all 6 architectures "
        "  - Accuracy vs Params: scatter plot showing the efficiency frontier. "
        "Stats chips show Parameters, Depth, Top-1 Accuracy, Year. "
        "The comparison bar chart at the bottom updates with the selected view."
    ),
    "/codeLab": (
        "Code Lab module (5 sections). PyTorch and TensorFlow/Keras side-by-side. "
        "INTERACTIVE DEMO (Step-through code walkthrough): "
        "Use the 'Framework' dropdown to switch between PyTorch and TensorFlow. "
        "Use the 'Topic' dropdown to choose: Build the CNN / Training Loop / Inference. "
        "Click 'Next →' to advance through 7 code steps; '← Prev' to go back. "
        "The left panel shows the code with the active line highlighted; "
        "the right panel explains what that step does and why. "
        "A progress bar tracks position through the walkthrough. "
        "Full static code reference for both frameworks is in Section 03, "
        "transfer learning code in Section 04, inference + TFLite in Section 05."
    ),
    "/data-augmentation": (
        "Data Augmentation module (5 sections). Covers: why augmentation prevents overfitting, "
        "Horizontal Flip, Random Crop, Colour Jitter, Rotation, Gaussian Blur, "
        "CutOut/RandomErasing, MixUp (λ·xᵢ + (1−λ)·xⱼ), CutMix, RandAugment. "
        "INTERACTIVE DEMO (Augmentation Playground): "
        "Adjust 6 sliders: H-Flip probability, Crop padding, Brightness jitter, "
        "Saturation jitter, Rotation ±°, Blur radius. "
        "Toggle Random Erasing and MixUp on/off with toggle switches. "
        "Click 'Apply Augmentations' to generate 3 side-by-side augmented samples from the original. "
        "Each sample shows which transforms were applied. "
        "Click '🎲 Randomise' to randomise all sliders and apply at once. "
        "Section 04 has full PyTorch (torchvision.transforms) and Keras augmentation code. "
        "Section 05 has a comparison table: when to use each technique and expected accuracy gain."
    ),
    "/quiz": (
        "Quiz page. GUVIans choose: Module (All Modules or any of the 7 individual modules), "
        "Difficulty (Beginner / Intermediate / Advanced), and Number of Questions (5 or 10). "
        "Click 'Generate Quiz with AI' — Groq Llama 3.3 generates fresh MCQ questions server-side. "
        "For each question: 4 options (A–D), click one to answer. "
        "Correct answer turns green with ✓, wrong choice turns red with ✗, "
        "remaining options turn blue. A full explanation appears after every answer (right or wrong). "
        "Progress bar and score counter update throughout. "
        "Results page: animated score ring, Neelu's personalised AI advice based on wrong answers, "
        "full per-question review with explanations, Retry and Home buttons."
    ),
}


# ── Page routes ───────────────────────────────────────────────────────────────
@app.route("/ping")
def ping():
    return "ok", 200
    
@app.route("/")
def index():
    return render_template("index.html", topics=TOPICS)

@app.route("/convolution")
def convolution():
    return render_template("convolution.html")

@app.route("/pooling")
def pooling():
    return render_template("pooling.html")

@app.route("/activation")
def activation():
    return render_template("activation.html")

@app.route("/training")
def training():
    return render_template("training.html")

@app.route("/architectures")
def architectures():
    return render_template("architectures.html")

@app.route("/codeLab")
def code_lab():
    return render_template("codeLab.html")

@app.route("/data-augmentation")
def data_augmentation():
    return render_template("data_augmentation.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")


# ── API: Neelu chatbot ────────────────────────────────────────────────────────
@app.route("/api/neelu-chat", methods=["POST"])
def api_neelu_chat():
    data      = request.json or {}
    user_msg  = data.get("message", "").strip()
    history   = data.get("history", [])
    page_path = data.get("page_path", "/")

    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

    page_ctx = PAGE_CONTEXT.get(page_path, PAGE_CONTEXT["/"])

    system = f"""You are Neelu 🤖 — a warm, knowledgeable AI study guide for GUVI's CNN Study app.
You address learners as "GUVIan" (naturally, not every sentence).

APP — 7 modules + quiz:
1. /convolution       — kernels, stride, padding, parameter sharing
2. /pooling           — max pool, avg pool, global avg pool, invariance
3. /activation        — ReLU, GELU, Swish, Sigmoid, Tanh, dead neurons
4. /training          — backprop, loss, Adam, BatchNorm, Dropout, LR scheduling
5. /architectures     — LeNet → AlexNet → VGG → ResNet → MobileNet → EfficientNet
6. /codeLab           — PyTorch & TensorFlow CNN implementation side-by-side
7. /data-augmentation — Flip, Crop, Jitter, MixUp, CutMix, RandAugment playground
/quiz                 — AI-generated MCQ with personalised feedback

CURRENT PAGE (use this to give specific, actionable demo guidance):
{page_ctx}

RULES:
- Reference the current page's specific interactive controls when relevant
- Keep answers concise: 2–5 sentences for simple questions; more only for code/multi-step
- Use **bold** for key terms and `code` for snippets
- Be encouraging and specific — name exact slider labels, button names, dropdown options
- You are Neelu, not Claude, ChatGPT, or any other AI
- When a learner seems stuck on the demo, walk them through it step by step"""

    try:
        trimmed = history[-12:] if len(history) > 12 else history
        reply = groq_chat(
            system,
            trimmed + [{"role": "user", "content": user_msg}],
            max_tokens=500,
        )
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── API: Quiz generation ──────────────────────────────────────────────────────
@app.route("/api/generate-quiz", methods=["POST"])
def api_generate_quiz():
    data   = request.json or {}
    module = data.get("module", "all")
    diff   = data.get("difficulty", "intermediate")
    count  = int(data.get("count", 10))

    module_desc = {
        "all": (
            "all CNN topics: convolution (kernels, stride, padding), pooling (max/avg/global), "
            "activation functions (ReLU/GELU/Swish/Sigmoid), training (backprop/Adam/BatchNorm/Dropout), "
            "CNN architectures (LeNet/AlexNet/VGG/ResNet/MobileNet/EfficientNet), "
            "PyTorch & TensorFlow implementation, and data augmentation (MixUp/CutOut/RandAugment)"
        ),
        "convolution": (
            "CNN convolution: kernels/filters, element-wise multiply-and-sum, feature maps, "
            "stride, padding, parameter sharing, receptive field, output size formula ⌊(N−F)/S⌋+1"
        ),
        "pooling": (
            "CNN pooling: max pooling, average pooling, global average pooling, "
            "translation invariance, downsampling, output size formula"
        ),
        "activation": (
            "activation functions: ReLU, Leaky ReLU, Sigmoid, Tanh, GELU, Swish — "
            "formulas, dead neuron problem, vanishing gradients, saturation, when to use each"
        ),
        "training": (
            "CNN training: backpropagation, chain rule, cross-entropy/MSE/focal loss, "
            "SGD/Momentum/Adam/AdamW, BatchNorm, Dropout, learning rate scheduling, "
            "data augmentation, weight initialisation (He/Xavier)"
        ),
        "architectures": (
            "CNN architectures: LeNet, AlexNet, VGG, ResNet (skip connections, residual blocks, "
            "degradation problem), MobileNet (depthwise separable conv), "
            "EfficientNet (compound scaling, NAS), transfer learning, backbone selection"
        ),
        "codeLab": (
            "PyTorch and TensorFlow/Keras CNN implementation: nn.Module, Sequential, functional API, "
            "training loops, DataLoaders, transfer learning (freeze/unfreeze), "
            "model.eval(), state_dict, TFLite export, inference"
        ),
        "data-augmentation": (
            "data augmentation: horizontal flip, random crop, colour jitter, rotation, "
            "Gaussian blur, CutOut/RandomErasing, MixUp (formula: x̃=λxᵢ+(1−λ)xⱼ), "
            "CutMix, RandAugment, test-time augmentation (TTA), when to use each technique"
        ),
    }

    diff_desc = {
        "beginner":     "straightforward recall and conceptual understanding. No calculations. Focus on definitions and intuition.",
        "intermediate": "applied understanding and some calculation questions (e.g. compute output size with formula). Mix conceptual and applied.",
        "advanced":     "deep understanding, tricky edge cases, implementation details, multi-step reasoning, code-reading questions.",
    }

    system = (
        "You are an expert CNN educator for GUVI. "
        "Generate quiz questions and return ONLY valid JSON — "
        "no markdown fences, no preamble, no trailing text."
    )

    prompt = f"""Generate exactly {count} multiple-choice questions about {module_desc.get(module, module_desc["all"])}.

Difficulty: {diff_desc.get(diff, diff_desc["intermediate"])}

Return ONLY this JSON array — no extra text before or after:
[
  {{
    "question": "Full question text?",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "correct": 0,
    "explanation": "3-5 sentences explaining why the correct answer is right AND why the main distractors are wrong. Reference specific concepts from the GUVI CNN Study app."
  }}
]

Rules:
- correct is the 0-based index of the correct option (0=A, 1=B, 2=C, 3=D)
- All 4 options must be plausible distractors — no obviously silly choices
- Vary question styles: definition, calculation, comparison, code-reading, "which is NOT correct", scenario-based
- Do not repeat similar questions
- Generate exactly {count} questions"""

    try:
        raw = groq_chat(system, [{"role": "user", "content": prompt}],
                        max_tokens=3500, temperature=0.4)
        raw = raw.strip().replace("```json", "").replace("```", "").strip()
        start = raw.find("[")
        end   = raw.rfind("]") + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON array found in response")
        questions = json.loads(raw[start:end])
        return jsonify({"questions": questions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── API: Personalised advice ──────────────────────────────────────────────────
@app.route("/api/personalized-message", methods=["POST"])
def api_personalized_message():
    data      = request.json or {}
    score     = data.get("score", 0)
    total     = data.get("total", 1)
    module    = data.get("module", "CNNs")
    diff      = data.get("difficulty", "intermediate")
    wrong_qs  = data.get("wrong_questions", [])
    pct       = round((score / total) * 100) if total else 0

    wrong_summary = ""
    if wrong_qs:
        lines = [
            f'Q: "{q["question"]}" — Chose: "{q["chosen"]}", Correct: "{q["correct"]}"'
            for q in wrong_qs[:6]
        ]
        wrong_summary = "Questions they got wrong:\n" + "\n".join(lines)

    system = (
        "You are Neelu, the GUVI CNN Study AI guide. "
        "Give warm, specific, personalised coaching advice. "
        "Address the learner as 'GUVIan'. Plain text only — no markdown."
    )

    prompt = f"""A GUVIan completed a {diff} quiz on "{module}" and scored {score}/{total} ({pct}%).

{wrong_summary if wrong_summary else "They answered all questions correctly — perfect score!"}

Write personalised advice in 4–6 sentences:
1. Open with an encouraging, score-specific comment
2. Name the exact concept(s) they struggled with (from the wrong answers, if any)
3. Tell them the specific section of the GUVI CNN Study app to revisit and what to look for there
4. Give one concrete tip or mental model to fix the misconception
5. End with forward-looking motivation for their next step

Be specific, warm, and actionable. Address them as GUVIan. Plain text only."""

    try:
        message = groq_chat(system, [{"role": "user", "content": prompt}],
                            max_tokens=320, temperature=0.65)
        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
