import gradio as gr
from engine import FooocusEngine

def main():
    # Motoru başlat
    engine = FooocusEngine()
    
    # Arayüzü oluştur
    with gr.Blocks(title="Prompt2Sticker") as app:
        gr.Markdown("# 🎨 Prompt2Sticker - Motor Testi")
        gr.Markdown("Eğer aşağıdaki 'Stil' kutusunda stilleri (Fooocus V2, Anime vb.) görüyorsan kurulum başarılı demektir.")
        
        with gr.Row():
            with gr.Column():
                prompt_input = gr.Textbox(label="Prompt (Test)", value="Cute cat sticker")
                style_input = gr.Dropdown(label="Stil Seç", choices=engine.get_styles(), value="Fooocus V2")
                generate_btn = gr.Button("Test Et")
            
            with gr.Column():
                output_text = gr.Textbox(label="Sonuç")
        
        generate_btn.click(fn=engine.generate, inputs=[prompt_input, style_input], outputs=output_text)
    
    # Uygulamayı başlat
    app.launch(share=True)

if __name__ == "__main__":
    main()
