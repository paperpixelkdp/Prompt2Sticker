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
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

    try:
        print("⏳ Engine: Loading Fooocus modules...")
        import modules.config as config
        import modules.core as core
        import args_manager
        from modules.sdxl_styles import legal_style_names
        print("✅ Engine: Fooocus modules loaded successfully!")
    except Exception as e:
        print(f"❌ ERROR: An unexpected error occurred while loading modules.\nDetail: {e}")
        legal_style_names = ["Error: Module Load Failed"]


class FooocusEngine:
    def __init__(self):
        self.styles = legal_style_names
        print(f"✅ Engine: Ready. {len(self.styles)} styles found.")
        self.models_loaded = False
        self.load_models()

    def load_models(self):
        if "FATAL ERROR" in self.styles[0]:
            print("❌ Engine: Skipping model load due to file verification failure.")
            return

        print("⏳ Engine: Loading models... This may take a while and download files on the first run.")
        try:
            args_manager.args.base = config.default_base_model_name
            args_manager.args.refiner = None
            args_manager.args.disable_offload_from_vram = True
            
            core.load_models_and_loras()
            self.models_loaded = True
            print("✅ Engine: Models loaded successfully.")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"❌ FATAL ERROR: Could not load models. \nDetail: {e}")
            self.models_loaded = False
            self.styles = ["FATAL ERROR: Model load failed. Check console."]

    def get_styles(self):
        """Returns the list of available styles."""
        return self.styles

    def generate(self, prompt, style):
        if not self.models_loaded:
            print("❌ Engine: Cannot generate, models are not loaded.")
            return None

        print(f"▶️ Engine: Generating for prompt='{prompt}', style='{style}'")
        
        try:
            result_images = None
            for result in core.generate_image(
                prompt=prompt,
                negative_prompt="",
                style_selections=[style],
                performance_selection='Speed',
                aspect_ratios_selection='1024*1024',
                image_number=1,
                image_seed=-1,
                sharpness=2.0,
                guidance_scale=4.0,
                base_model_name=config.default_base_model_name,
                refiner_model_name='None',
                refiner_switch=0.1,
                loras=[]
            ):
                result_images = result

            if result_images is None:
                raise Exception("Image generation failed, no images were returned.")

            print(f"✅ Engine: Generation complete.")
            return result_images[0]

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"❌ ERROR: Image generation failed.\nDetail: {e}")
            return None
