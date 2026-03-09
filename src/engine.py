import os
import sys

# Add src folder to Python path to find modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Fix: Create 'sdxl_styles' directory if it doesn't exist
# Fooocus expects this directory to exist to load custom styles
# We create it in both the current directory and src to be safe
for path in ['sdxl_styles', os.path.join(current_dir, 'sdxl_styles')]:
    os.makedirs(path, exist_ok=True)

# Set up necessary paths for Fooocus to run
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

try:
    print("⏳ Loading Fooocus modules...")
    # Importing Fooocus's own modules
    import modules.config as config
    from modules.sdxl_styles import legal_style_names
    print("✅ Fooocus modules loaded successfully!")
except ImportError as e:
    print(f"❌ ERROR: Fooocus modules not found.\nDetail: {e}")
    print("Please ensure 'modules', 'ldm_patched', and 'args_manager.py' are copied into the 'src' folder.")
    legal_style_names = ["Error: Styles could not be loaded"]
except Exception as e:
    print(f"❌ ERROR: Unexpected error loading modules.\nDetail: {e}")
    legal_style_names = ["Error: Module Load Failed"]

class FooocusEngine:
    def __init__(self):
        self.styles = legal_style_names
        print(f"✅ Engine ready. {len(self.styles)} styles found.")

    def get_styles(self):
        """Returns the list of available styles."""
        return self.styles

    def generate(self, prompt, style):
        """For now, we are just testing the connection. Real image generation will be added in the next step."""
        return f"✅ SUCCESS! Engine is running.\nReceived Prompt: {prompt}\nSelected Style: {style}"
