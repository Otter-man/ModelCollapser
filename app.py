import os
import gradio as gr
from main import generate_chain
from PIL import Image

def process_image_chain(image, prompt, n_iterations, n_retries):
    if image is None:
        return None, None, None, "Please upload an image"
    if not prompt:
        return None, None, None, "Please enter a prompt"
    if n_iterations < 1:
        return None, None, None, "Number of iterations must be at least 1"
    
    try:
        # Save the uploaded image temporarily
        temp_path = "temp_input.png"
        image.save(temp_path)
        
        # Generate the chain
        output_paths = generate_chain(temp_path, prompt, n_iterations, n_retries)
        
        # Clean up temporary file
        os.remove(temp_path)
        
        if not output_paths:
            return None, None, None, "No images were generated"
        
        # Create a GIF from the output images
        images = [Image.open(path) for path in output_paths]
        gif_path = "output_chain.gif"
        images[0].save(
            gif_path,
            save_all=True,
            append_images=images[1:],
            duration=500,  # 500ms between frames
            loop=0
        )
            
        # Return the last generated image, the GIF, all image paths, and a success message
        return output_paths[-1], gif_path, output_paths, f"Successfully generated {len(output_paths)} images"
        
    except Exception as e:
        return None, None, None, f"Error: {str(e)}"

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
            gif_output = gr.Image(label="Generation Progress (GIF)")
            status = gr.Textbox(label="Status")
    
    # Add a gallery component below the main interface
    with gr.Row():
        gallery = gr.Gallery(
            label="All Generation Steps",
            show_label=True,
            elem_id="gallery",
            columns=[4],
            rows=[2],
            height="auto",
            object_fit="contain"
        )
    
    generate_btn.click(
        fn=process_image_chain,
        inputs=[input_image, prompt, n_iterations, n_retries],
        outputs=[output_image, gif_output, gallery, status]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860) 