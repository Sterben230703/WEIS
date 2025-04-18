# import os
# from modules.encryption_module import load_image, split_HSB_LSB, additive_secret_sharing, block_scramble, save_image
# from modules.embedding_module import load_watermark, embed_watermark_bits
# from modules.decryption_extraction_module import decrypt_and_extract
# from modules.modified_rrwei_module import apply_modified_rrwei
# from modules.evaluation_module import evaluate_all

# def phase_separator(name):
#     print(f"\n{'='*60}\n🟩 Starting: {name}\n{'='*60}")

# def main():
#     # Setup paths
#     cover_image_path = "images/lena.png"
#     watermark_path = "images/watermark.png"
#     output_dir = "output"
#     os.makedirs(output_dir, exist_ok=True)

#     # 🔐 Phase 1: Image Encryption
#     phase_separator("Phase 1: Image Encryption")
#     image = load_image(cover_image_path)
#     HSB, LSB = split_HSB_LSB(image, n_bits=4)
#     share1, share2 = additive_secret_sharing(HSB, LSB)
#     scrambled_share1 = block_scramble(share1, block_size=2)
#     scrambled_share2 = block_scramble(share2, block_size=2)

#     save_image("output/share1.png", scrambled_share1)
#     save_image("output/share2.png", scrambled_share2)

#     # 🖋️ Phase 2: Watermark Embedding
#     phase_separator("Phase 2: Watermark Embedding")
#     watermark = load_watermark(watermark_path)
#     marked_share1, marked_share2 = embed_watermark_bits(scrambled_share1, scrambled_share2, watermark)

#     save_image("output/marked_share1.png", marked_share1)
#     save_image("output/marked_share2.png", marked_share2)

#     # 🔓 Phase 3: Decryption & Extraction
#     phase_separator("Phase 3: Decryption & Watermark Extraction")
#     recovered_image, extracted_watermark = decrypt_and_extract(marked_share1, marked_share2)

#     save_image("output/recovered_image.png", recovered_image)
#     save_image("output/extracted_watermark.png", extracted_watermark)

#     # 🛡️ Phase 4: Modified RRWEI-SM
#     phase_separator("Phase 4: Robust Two-Stage Watermarking (RRWEI-SM)")
#     robust_marked_image, side_info = apply_modified_rrwei(HSB, watermark)
#     save_image("output/robust_marked_image.png", robust_marked_image)

#     # 📊 Phase 5: Evaluation
#     phase_separator("Phase 5: Evaluation")
#     evaluate_all(original=image,
#                  recovered=recovered_image,
#                  encrypted=scrambled_share1,
#                  extracted_watermark=extracted_watermark,
#                  original_watermark=watermark)

#     print("\n✅ All phases completed successfully.\n")

# if __name__ == "__main__":
#     main()
import argparse
import os
from modules.encryption_module import load_image, split_HSB_LSB, additive_secret_sharing, block_scramble, save_image
from modules.embedding_module import load_watermark, embed_watermark_bits
from modules.decryption_extraction_module import decrypt_and_extract
from modules.modified_rrwei_module import apply_modified_rrwei
from modules.evaluation_module import evaluate_all

def phase_separator(name):
    print(f"\n{'='*60}\n🟩 Starting: {name}\n{'='*60}")

def run_encryption(image_path):
    image = load_image(image_path)
    HSB, LSB = split_HSB_LSB(image, n_bits=4)
    share1, share2 = additive_secret_sharing(HSB, LSB)
    scrambled_share1 = block_scramble(share1, block_size=2)
    scrambled_share2 = block_scramble(share2, block_size=2)
    save_image("output/share1.png", scrambled_share1)
    save_image("output/share2.png", scrambled_share2)
    return scrambled_share1, scrambled_share2, HSB, image

def run_embedding(scrambled_share1, watermark_path):
    watermark = load_watermark(watermark_path)
    marked_share1, embedded_pos = embed_watermark_bits(scrambled_share1, watermark)
    save_image("output/marked_share1.png", marked_share1)
    return marked_share1, watermark


def run_decryption_and_extraction(marked_share1, marked_share2):
    recovered_image, extracted_watermark = decrypt_and_extract(marked_share1, marked_share2)
    save_image("output/recovered_image.png", recovered_image)
    save_image("output/extracted_watermark.png", extracted_watermark)
    return recovered_image, extracted_watermark

def run_modified_rrwei(HSB, watermark):
    robust_marked_image, side_info = apply_modified_rrwei(HSB, watermark)
    save_image("output/robust_marked_image.png", robust_marked_image)

def main():
    parser = argparse.ArgumentParser(description="Run the RRWEI-SM pipeline.")
    parser.add_argument("--phase", type=str, default="all", choices=["all", "encrypt", "embed", "extract", "robust", "evaluate"],
                        help="Choose which phase to run")
    parser.add_argument("--cover", type=str, default="images/lena.png", help="Path to cover image")
    parser.add_argument("--watermark", type=str, default="images/watermark.png", help="Path to binary watermark image")
    args = parser.parse_args()

    os.makedirs("output", exist_ok=True)

    if args.phase == "all":
        phase_separator("Phase 1: Image Encryption")
        s1, s2, HSB, original = run_encryption(args.cover)

        phase_separator("Phase 2: Watermark Embedding")
        m1, watermark = run_embedding(s1, args.watermark)
        m2 = s2  # unmodified second share
        save_image("output/marked_share2.png", m2)


        phase_separator("Phase 3: Decryption & Watermark Extraction")
        recovered_image, extracted_watermark = run_decryption_and_extraction(m1, m2)

        phase_separator("Phase 4: Robust RRWEI-SM Embedding")
        run_modified_rrwei(HSB, watermark)

        phase_separator("Phase 5: Evaluation")
        evaluate_all(original, recovered_image, s1, extracted_watermark, watermark)

    elif args.phase == "encrypt":
        phase_separator("Phase 1: Image Encryption")
        run_encryption(args.cover)

    elif args.phase == "embed":
        s1 = load_image("output/share1.png")
        s2 = load_image("output/share2.png")
        phase_separator("Phase 2: Watermark Embedding")
        run_embedding(s1, s2, args.watermark)

    elif args.phase == "extract":
        m1 = load_image("output/marked_share1.png")
        m2 = load_image("output/marked_share2.png")
        phase_separator("Phase 3: Decryption & Watermark Extraction")
        run_decryption_and_extraction(m1, m2)

    elif args.phase == "robust":
        image = load_image(args.cover)
        HSB, _ = split_HSB_LSB(image, n_bits=4)
        watermark = load_watermark(args.watermark)
        phase_separator("Phase 4: Robust RRWEI-SM Embedding")
        run_modified_rrwei(HSB, watermark)

    elif args.phase == "evaluate":
        original = load_image(args.cover)
        recovered = load_image("output/recovered_image.png")
        encrypted = load_image("output/share1.png")
        extracted_w = load_image("output/extracted_watermark.png")
        watermark = load_watermark(args.watermark)
        phase_separator("Phase 5: Evaluation")
        evaluate_all(original, recovered, encrypted, extracted_w, watermark)

    print("\n✅ Done.\n")

if __name__ == "__main__":
    main()
