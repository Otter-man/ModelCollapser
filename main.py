import os
import uuid
import argparse
import base64
from openai import OpenAI


def generate_chain(base_image_path: str, prompt: str, n: int, retries: int = None, *, correct: bool = False):
    """
    Generates a chain of N images by iteratively editing the previous output using the same prompt.
    If `retries` is set, automatically retries on failure up to that number of times; otherwise, prompts the user.
    If `correct` is True, applies color correction after each generation and uses it as the next input.

    Args:
        base_image_path (str): Path to the initial base image.
        prompt (str): The text prompt for editing.
        n (int): Number of iterations.
        retries (int, optional): Number of automatic retries on failure.

    Returns:
        List of output file paths.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key=api_key)

    # Prepare output directory
    while True:
        dir_uuid = str(uuid.uuid4())
        if not os.path.exists(dir_uuid):
            output_dir = dir_uuid
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
            break

    # Create subfolders
    generated_dir = os.path.join(output_dir, "generated")
    corrected_dir = os.path.join(output_dir, "corrected")
    os.makedirs(generated_dir, exist_ok=True)
    if correct:
        os.makedirs(corrected_dir, exist_ok=True)

    outputs = []
    current_image = base_image_path

    # Lazy import color correction dependencies only if requested
    color_correct_fn = None
    if correct:
        try:
            import cv2  # type: ignore
            from remove_yellow_tint import fix_warm_cast_standalone as color_correct_fn  # type: ignore
        except Exception as e:
            raise RuntimeError("--correct requires opencv-python, numpy, and remove_yellow_tint.py present") from e

    for i in range(1, n + 1):
        attempt = 0
        while True:
            try:
                print(f"Iteration {i}/{n}: editing image '{current_image}' (attempt {attempt + 1})")
                with open(current_image, "rb") as img_file:
                    result = client.images.edit(
                        model="gpt-image-1",
                        image=[img_file],
                        prompt=prompt,
                        quality="high",
                        size="1024x1024",
                        n=1
                    )

                # Decode and save
                image_b64 = result.data[0].b64_json
                image_data = base64.b64decode(image_b64)
                gen_path = os.path.join(generated_dir, f"{i:02d}.png")
                with open(gen_path, "wb") as out_file:
                    out_file.write(image_data)

                print(f"Iteration {i}: saved generated image to '{gen_path}'")

                outputs.append(gen_path)
                if correct:
                    # Color-correct the generated image and save
                    import cv2  # type: ignore

                    img_bgr = cv2.imread(gen_path, cv2.IMREAD_COLOR)
                    corrected_bgr = color_correct_fn(img_bgr)  # type: ignore
                    corr_path = os.path.join(corrected_dir, f"{i:02d}.png")
                    cv2.imwrite(corr_path, corrected_bgr)
                    print(f"Iteration {i}: saved color-corrected image to '{corr_path}'")

                    # Use corrected as input to next iteration
                    outputs.append(corr_path)
                    current_image = corr_path
                else:
                    # Use generated as input to next iteration
                    current_image = gen_path
                break

            except Exception as e:
                attempt += 1
                if retries is not None:
                    if attempt <= retries:
                        print(f"Error on iteration {i}, attempt {attempt}/{retries}: {e}. Retrying...")
                        continue
                    else:
                        print(f"Iteration {i} failed after {retries} retries: {e}. Aborting.")
                        return outputs
                else:
                    resp = input(f"Iteration {i} failed with error: {e}. Retry? [y/N]: ")
                    if resp.strip().lower() == 'y':
                        continue
                    else:
                        print("Aborting.")
                        return outputs

    print("Generation complete.")
    return outputs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate a chain of images via iterative OpenAI edits.")
    parser.add_argument('--image', '-i', required=True, help="Path to base image.")
    parser.add_argument('--prompt', '-p', required=True, help="Text prompt.")
    parser.add_argument('--n', '-n', type=int, required=True, help="Number of iterations.")
    parser.add_argument('--retries', '-r', type=int, help="Number of auto-retries on failure. If omitted, will prompt user.")
    parser.add_argument('--correct', action='store_true', help="Apply color correction after each generation and use it for next iteration.")
    args = parser.parse_args()

    results = generate_chain(args.image, args.prompt, args.n, args.retries, correct=args.correct)
    print("Generated images:" if not args.correct else "Generated and corrected images:")
    for path in results:
        print(path)
