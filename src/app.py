import gradio as gr
from engine import FooocusEngine

def main():
    # Initialize the engine
    engine = FooocusEngine()
    
    # Create the interface
    with gr.Blocks(title="Prompt2Sticker") as app:
        gr.Markdown("# 🎨 Prompt2Sticker - Engine Test")
        gr.Markdown("If you see the styles (Fooocus V2, Anime, etc.) in the 'Style' dropdown below, the setup is successful.")
        
        with gr.Row():
            with gr.Column():
                prompt_input = gr.Textbox(label="Prompt (Test)", value="Cute cat sticker")
                style_input = gr.Dropdown(label="Select Style", choices=engine.get_styles(), value="Fooocus V2")
                generate_btn = gr.Button("Test")
            
            with gr.Column():
                output_text = gr.Textbox(label="Result")
        
        generate_btn.click(fn=engine.generate, inputs=[prompt_input, style_input], outputs=output_text)
    
    # Launch the app
    app.launch(share=True)

if __name__ == "__main__":
    main()
