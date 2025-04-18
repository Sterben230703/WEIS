# 🔒 Robust Reversible Watermarking in Encrypted Images using Secure Multi-Party and Lightweight Cryptography

This project implements a **robust and reversible watermarking system** for encrypted grayscale images. It leverages **additive secret sharing**, **prediction error expansion**, and **patchwork watermarking**, all within a **Secure Multi-Party Computation (SMC)** framework.

---

## 📌 Key Modules & Phases

### 1️⃣ Image Encryption Phase
- **Goal**: Encrypt the grayscale cover image using additive secret sharing and block-level scrambling.
- **Output**: Two scrambled encrypted image shares.
- 📁 `modules/encryption_module.py`

---

### 2️⃣ Watermark Embedding Phase
- **Goal**: Embed watermark bits into encrypted shares using Prediction Error Expansion (PEE) in SMC style.
- **Output**: Two marked encrypted shares.
- 📁 `modules/embedding_module.py`

---

### 3️⃣ Decryption and Extraction Phase
- **Goal**: Reconstruct original image and extract watermark bits.
- **Output**: Recovered image, extracted watermark.
- 📁 `modules/decryption_extraction_module.py`

---

### 4️⃣ Modified RRWEI-SM (Two-Stage Watermarking)
- **Goal**: Improve robustness by combining patchwork + PEE in a two-stage embedding pipeline.
- **Output**: More robust watermark-embedded shares.
- 📁 `modules/modified_rrwei_module.py`

---

### 5️⃣ Evaluation Phase
- **Goal**: Evaluate image quality, watermark robustness, and encryption security.
- 📊 Metrics:
  - PSNR, SSIM (Image Quality)
  - BER (Watermark Error Rate)
  - NPCR (Encryption Diffusion Strength)
- 📁 `modules/evaluation_module.py`

---

## 🖼️ Folder Structure

🧪 Installation & Setup
bash
Copy
Edit
# Clone project and set up environment
python -m venv venv
source venv/bin/activate       # For Linux/macOS
venv\Scripts\activate          # For Windows

# Install dependencies
pip install -r requirements.txt
🖼️ Input Requirements
Grayscale image (e.g., lena.png)

Binary watermark image (e.g., watermark.png — black & white)

Place both files inside the /images/ directory.

🚀 How to Run the Project
bash
Copy
Edit
python main.py
This will:

🔐 Encrypt the cover image

🖋️ Embed the watermark

🔓 Reconstruct the original image & extract watermark

🛡️ Run two-stage robust watermarking

📊 Evaluate system metrics (PSNR, SSIM, BER, NPCR, etc.)

📦 Requirements
txt
Copy
Edit
numpy
opencv-python
scikit-image
matplotlib
Install with:

bash
Copy
Edit
pip install -r requirements.txt

python main.py --phase all
python main.py --phase encrypt --cover images/my_image.png
python main.py --phase embed --watermark images/logo_bw.png
python main.py --phase all --cover images/lena.png --watermark images/watermark.png
