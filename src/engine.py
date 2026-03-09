import os
import sys
import json

# Set up necessary paths for Fooocus to run
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# Add src folder to Python path to find our copied modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# --- The Root Cause Fix ---
# 1. Import the config module first. It holds all path information.
import modules.config as config

# 2. Define the correct path for the styles directory relative to this file.
correct_style_path = os.path.join(current_dir, 'sdxl_styles')

# 3. Override Fooocus's default path variable BEFORE other modules are loaded.
# This tells all other Fooocus modules the correct place to look for styles.
config.path_styles = correct_style_path
print(f"✅ Engine: Overriding Fooocus style path to -> {config.path_styles}")

# 4. Now that the path is corrected, we can safely import the rest.
try:
    print("⏳ Engine: Loading Fooocus modules with correct paths...")
    from modules.sdxl_styles import legal_style_names
    print("✅ Engine: Fooocus modules loaded successfully!")
except ImportError as e:
    print(f"❌ ERROR: Fooocus modules not found.\nDetail: {e}")
    print("Please ensure 'modules', 'ldm_patched', and 'args_manager.py' are copied into the 'src' folder.")
    legal_style_names = ["Error: Styles could not be loaded"]
except Exception as e:
    print(f"❌ ERROR: Unexpected error loading modules.\nDetail: {e}")
    legal_style_names = ["Error: Module Load Failed"]
finally:
    # Robustness: Ensure the style directory exists.
    os.makedirs(config.path_styles, exist_ok=True)

class FooocusEngine:
    def __init__(self):
        self.styles = legal_style_names
        print(f"✅ Engine: Ready. {len(self.styles)} styles found.")

    def get_styles(self):
        """Returns the list of available styles."""
        return self.styles

    def generate(self, prompt, style):
        """Placeholder for image generation. To be implemented."""
        return f"SUCCESS! Engine is running.\nReceived Prompt: {prompt}\nSelected Style: {style}"
