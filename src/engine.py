import os
import sys

# src klasörünü Python yoluna ekle ki modülleri bulabilsin
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Fooocus'un çalışması için gerekli yolları ayarla
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

try:
    print("⏳ Fooocus modülleri yükleniyor...")
    # Fooocus'un kendi modüllerini çağırıyoruz
    import modules.config as config
    from modules.sdxl_styles import legal_style_names
    print("✅ Fooocus modülleri başarıyla yüklendi!")
except ImportError as e:
    print(f"❌ HATA: Fooocus modülleri bulunamadı.\nDetay: {e}")
    print("Lütfen 'modules' ve 'ldm_patched' klasörlerini 'src' içine kopyaladığından emin ol.")
    legal_style_names = ["Hata: Stiller Yüklenemedi"]

class FooocusEngine:
    def __init__(self):
        self.styles = legal_style_names
        print(f"✅ Motor hazır. {len(self.styles)} adet stil bulundu.")

    def get_styles(self):
        """Mevcut stillerin listesini döndürür."""
        return self.styles

    def generate(self, prompt, style):
        """
        Şimdilik sadece bağlantıyı test ediyoruz.
        Gerçek resim üretimi bir sonraki adımda eklenecek.
        """
        return f"✅ BAŞARILI! Motor çalışıyor.\nGelen Prompt: {prompt}\nSeçilen Stil: {style}"
