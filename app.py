import os
import gradio as gr
from main import generate_chain

def process_image_chain(image, prompt, n_iterations, n_retries):
    if image is None:
        return None, "Please upload an image"
    if not prompt:
        return None, "Please enter a prompt"
    if n_iterations < 1:
        return None, "Number of iterations must be at least 1"
    
    try:
        # Save the uploaded image temporarily
        temp_path = "temp_input.png"
        image.save(temp_path)
        
        # Generate the chain
        output_paths = generate_chain(temp_path, prompt, n_iterations, n_retries)
        
        # Clean up temporary file
        os.remove(temp_path)
        
        if not output_paths:
            return None, "No images were generated"
            
        # Return the last generated image and a success message
        return output_paths[-1], f"Successfully generated {len(output_paths)} images"
        
    except Exception as e:
        return None, f"Error: {str(e)}"

# Create the Gradio interface
with gr.Blocks(title="Model Collapser") as demo:
    gr.Markdown("# Model Collapser")
    gr.Markdown("Generate a chain of images by iteratively editing using OpenAI's image editing model.")
    
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(type="pil", label="Base Image")
            prompt = gr.Textbox(label="Prompt", placeholder="Enter your prompt here...")
            n_iterations = gr.Slider(minimum=1, maximum=10, value=3, step=1, label="Number of Iterations")
            n_retries = gr.Slider(minimum=0, maximum=5, value=2, step=1, label="Number of Retries")
            generate_btn = gr.Button("Generate Chain")
        
        with gr.Column():
            output_image = gr.Image(label="Final Generated Image")
            status = gr.Textbox(label="Status")
    
    generate_btn.click(
        fn=process_image_chain,
        inputs=[input_image, prompt, n_iterations, n_retries],
        outputs=[output_image, status]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860) 