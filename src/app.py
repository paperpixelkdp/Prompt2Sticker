import gradio as gr
from engine import FooocusEngine

# Initialize the engine once when the script starts
print("Initializing Engine...")
engine = FooocusEngine()
print("Engine Initialized.")

def generate_stickers(prompts_text: str, style: str, progress=gr.Progress(track_tqdm=True)):
    """
    Takes a string of prompts (one per line), generates an image for each,
    and eventually will combine them into a sticker sheet.
    For now, it returns the first generated image as a preview.
    """
    if not engine.models_loaded:
        raise gr.Error("Engine models are not loaded. Please check the console for errors and restart.")

    prompts = [p.strip() for p in prompts_text.split('\n') if p.strip()]
    
    if not prompts:
        raise gr.Error("Please enter at least one prompt.")

    print(f"🎨 App: Received {len(prompts)} prompts. Starting generation...")
    
    generated_images = []
    
    for i in progress.tqdm(range(len(prompts)), desc="Generating Stickers"):
        prompt = prompts[i]
        print(f"  -> Generating image {i+1}/{len(prompts)} for: '{prompt}'")
        
        image = engine.generate(prompt, style)
        
        if image is None:
            print(f"  ⚠️ WARNING: Generation failed for prompt: '{prompt}'")
            continue
            
        generated_images.append(image)

    print("✅ App: All generations complete.")
    
    if generated_images:
        # TODO: Implement sticker sheet generation logic.
        # For now, just return the first image as a preview.
        return generated_images[0]
    else:
        raise gr.Error("Image generation failed for all prompts. Please check your prompts or the console for errors.")

def main():
    with gr.Blocks(title="Prompt2Sticker", theme=gr.themes.Soft()) as app:
        gr.Markdown("# 🎨 Prompt2Sticker\n### Create sticker sheets from text prompts.")
        
        with gr.Row():
            with gr.Column(scale=1):
                prompt_input = gr.Textbox(
                    label="Prompts (one per line)", 
                    lines=8,
                    placeholder="A cute cat sticker, vector art, white background\nA happy dog sticker, cartoon style, white background\n..."
                )
                style_input = gr.Dropdown(
                    label="Image Style", 
                    choices=engine.get_styles(), 
                    value="Fooocus V2"
                )
                generate_btn = gr.Button("Generate Stickers", variant="primary")
            
            with gr.Column(scale=2):
                output_image = gr.Image(label="Result Preview (First Sticker)", type="pil")
        
        generate_btn.click(
            fn=generate_stickers, 
            inputs=[prompt_input, style_input], 
            outputs=output_image
        )
    
    app.launch(share=True, show_error=True)

if __name__ == "__main__":
    if "FATAL ERROR" in engine.styles[0]:
        print("\n" + "="*50)
        print("Could not start the application due to a fatal error during engine initialization.")
        print("Please check the error messages above.")
        print("="*50)
    else:
        main()
