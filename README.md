# Text & Image to 3D Model Generator 🎨➡️🧊

This project is a simple yet functional prototype that converts **text prompts** or **photos** into basic 3D models (`.obj`, `.stl`, or `.ply`). It integrates two powerful open-source models:

- 🧠 **Point-E** for generating 3D point clouds from text prompts.
- 📸 **TripoSR** for generating 3D mesh models from single images.

## 🔧 Features

- Text-to-3D using Point-E (outputs colored mesh models).
- Image-to-3D using TripoSR via a user-friendly Gradio interface.
- Unified pipeline (`main.py`) for choosing either text or image input.
- All outputs are saved in a separate `output` directory.

## 🗂️ Project Structure

├── run.py  (Unified pipeline controller) <br>
├── text_to_3d_model.py (Text-to-3D logic using Point-E) <br>
├── TripoSR/ (Contains TripoSR source code) <br>
│ └── app/ <br>
│ └── gradio_app.py  (TripoSR image-based Gradio interface) <br>
├── Output/  (Folder where generated models are saved) <br>
└── README.md <br>

---

## 📦 Libraries Used

### Core
- torch
- numpy
- open3d
- gradio

### Point-E Specific
- point_e (install from OpenAI repo)

### TripoSR Specific
- onnxruntime
- tokenizers
- torchmcubes
- transformers
- pillow
- tqdm
- scipy
- trimesh

> Note: TripoSR also requires **Rust** (for building tokenizers), installable via [https://rustup.rs](https://rustup.rs).

## 🚀 How to Run

### 1. Clone the Repository
git clone https://github.com/Kaustav-JB/3d-Model-Project.git
cd 3d-Model-Project

### 2. Install Dependencies
pip install -r requirements.txt

> If you encounter Rust-related build issues, ensure you have cargo installed:
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

### 3. Run the Pipeline
python main.py

Then choose:

- 1 for text-to-3D (Point-E)
- 2 for image-to-3D (TripoSR Gradio app)

## 💡Thought Process
This prototype is designed to show quick 3D content creation from minimal input: just a text or a photo. I explored open-source AI models that are easy to deploy and output usable .obj/.stl formats. The integration focuses on:

- Ease of use (command-line + GUI)
- Minimal manual preprocessing
- Keeping it modular for future expansion

## 📌Notes
- Outputs are saved inside the output folder.
- For TripoSR, your browser will open the local Gradio interface at http://127.0.0.1:7860.

## 🧠Credits
- Point-E by OpenAI

- TripoSR by Stability AI
