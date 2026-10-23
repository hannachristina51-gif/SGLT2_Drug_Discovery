#!/usr/bin/env python3
"""
Script Otomatisasi Deployment SGLT2 Virtual Screening App ke Hugging Face Spaces.
Menggunakan library resmi `huggingface_hub`.
"""

import os
import sys
from huggingface_hub import HfApi, login

def main():
    print("=" * 60)
    print("🚀 SGLT2 Drug Discovery - Hugging Face Spaces Deployer")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    space_dir = os.path.join(base_dir, "hf_space")
    
    if not os.path.exists(space_dir):
        print(f"❌ Direktori {space_dir} tidak ditemukan.")
        sys.exit(1)
        
    # Periksa token dari argumen / environment / input interaktif
    token = os.environ.get("HF_TOKEN")
    if not token and len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        token = sys.argv[1]
        
    if not token:
        print("\nUntuk mengunggah ke Hugging Face, Anda memerlukan Access Token (Write Permission).")
        print("Dapatkan token di: https://huggingface.co/settings/tokens")
        token = input("\nMasukkan Hugging Face Token (hf_...): ").strip()
        
    if not token:
        print("❌ Token tidak boleh kosong. Pembatalan deployment.")
        sys.exit(1)
        
    api = HfApi(token=token)
    
    # Dapatkan username pemilik akun
    try:
        user_info = api.whoami()
        username = user_info['name']
        print(f"\n✅ Terautentikasi sebagai pengguna: {username}")
    except Exception as e:
        print(f"❌ Gagal memvalidasi token: {e}")
        sys.exit(1)
        
    repo_name = input(f"Masukkan nama Space [default: sglt2-virtual-screening]: ").strip()
    if not repo_name:
        repo_name = "sglt2-virtual-screening"
        
    repo_id = f"{username}/{repo_name}"
    print(f"\n📦 Menyiapkan Space: {repo_id}...")
    
    try:
        api.create_repo(
            repo_id=repo_id,
            repo_type="space",
            space_sdk="streamlit",
            exist_ok=True
        )
        print("✅ Space repository siap di Hugging Face.")
        
        print(f"📤 Mengunggah berkas dari {space_dir}...")
        print("(Berkas model ~30MB akan otomatis dikelola oleh sistem LFS Hugging Face)")
        
        api.upload_folder(
            folder_path=space_dir,
            repo_id=repo_id,
            repo_type="space"
        )
        
        space_url = f"https://huggingface.co/spaces/{repo_id}"
        print("\n" + "=" * 60)
        print("🎉 DEPLOYMENT BERHASIL!")
        print(f"🌐 Kunjungi aplikasi Anda di:")
        print(f"   👉 {space_url}")
        print("=" * 60)
        print("Catatan: Diperlukan waktu sekitar 1-2 menit bagi Hugging Face untuk membangun (build) kontainer.")
        
    except Exception as e:
        print(f"\n❌ Terjadi kesalahan saat proses deploy: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
