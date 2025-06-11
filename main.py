#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conference Room - LLM Chain Automation Platform
Ana çalıştırılabilir dosya
"""

import os
import sys
import traceback

def main():
    try:
        # Proje dizinini sys.path'e ekle
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # GUI uygulamasını başlat
        from top import ConferenceRoomApp
        
        app = ConferenceRoomApp()
        app.mainloop()
        
    except ImportError as e:
        print(f"HATA: Gerekli paketler bulunamadı: {e}")
        print("Lütfen şu komutu çalıştırın: pip install -r requirements.txt")
        input("Devam etmek için Enter'a basın...")
        sys.exit(1)
    except Exception as e:
        print(f"BEKLENMEYEN HATA: {e}")
        print("\nDetaylı hata bilgisi:")
        traceback.print_exc()
        input("Devam etmek için Enter'a basın...")
        sys.exit(1)

if __name__ == "__main__":
    main()
