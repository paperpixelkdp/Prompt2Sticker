import os
import sys

# Add src folder to Python path to find our copied modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# --- Pre-flight Check ---
# Before importing Fooocus modules, verify our folder structure.
print("⏳ Engine: Verifying required files and folders...")
required_items = ['modules', 'ldm_patched', 'presets', 'sdxl_styles', 'args_manager.py']
all_found = True
for item in required_items:
    path = os.path.join(current_dir, item)
    if not os.path.exists(path):
        item_type = "folder" if '.' not in item else "file"
        print(f"❌ FATAL ERROR: The required {item_type} '{item}' was not found inside the 'src' directory.")
        all_found = False

if not all_found:
    print("Engine cannot start. Please ensure all required items from Fooocus are copied correctly into 'src'.")
    # Set a dummy variable so the program doesn't crash on import, but shows the error.
    legal_style_names = ["FATAL ERROR: See console for details."]
else:
    print("✅ Engine: All required items found.")
    # Set up necessary paths for Fooocus to run
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

    # Now that all folders are in the correct place, we can import directly.
    try:
        print("⏳ Engine: Loading Fooocus modules...")
        from modules.sdxl_styles import legal_style_names
        print("✅ Engine: Fooocus modules loaded successfully!")
    except ImportError as e:
        print(f"❌ ERROR: A required Fooocus module was not found during import.\nDetail: {e}")
        legal_style_names = ["Error: Styles could not be loaded"]
    except Exception as e:
        print(f"❌ ERROR: An unexpected error occurred while loading modules.\nDetail: {e}")
        legal_style_names = ["Error: Module Load Failed"]


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
