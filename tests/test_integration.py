import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from PIL import Image
import gradio as gr
from app import demo, process_image_chain

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Create a temporary test image
        self.test_image = Image.new('RGB', (100, 100), color='red')
        
        # Create a temporary directory for test outputs in /tmp
        self.test_dir = tempfile.mkdtemp(dir='/tmp')
        os.chdir(self.test_dir)

    def tearDown(self):
        # Reset working directory to /tmp before deleting temp dir
        os.chdir('/tmp')
        # Recursively clean up temporary files and directories
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.unlink(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    @patch("app.demo.launch")
    def test_gradio_interface_components(self, mock_launch):
        """Test that all Gradio interface components are properly initialized"""
        # Ensure the interface is fully initialized
        mock_launch.return_value = None
        self.assertTrue(hasattr(demo, 'blocks'))
        print('DEBUG demo.blocks:', demo.blocks)
        # Recursively collect all component class names
        def collect_component_class_names(blocks):
            class_names = []
            for block in blocks:
                if hasattr(block, 'component'):
                    class_names.append(block.component.__class__.__name__)
                elif hasattr(block, '__class__'):
                    class_names.append(block.__class__.__name__)
                # Check for children (Gradio 4.x+)
                if hasattr(block, 'children') and isinstance(block.children, list):
                    class_names.extend(collect_component_class_names(block.children))
            return class_names
        component_class_names = collect_component_class_names(demo.blocks.values())
        print('DEBUG component_class_names:', component_class_names)
        # Check for expected component class names
        self.assertIn('Image', component_class_names, "Image component not found")
        self.assertIn('Textbox', component_class_names, "Textbox component not found")
        self.assertIn('Slider', component_class_names, "Slider component not found")
        self.assertIn('Button', component_class_names, "Button component not found")

    @patch("main.OpenAI")
    def test_process_chain_output_format(self, mock_openai):
        """Test that process_image_chain returns the correct number of outputs (mocked)"""
        # Use a valid minimal PNG base64
        valid_png_b64 = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/" 
            "/w8AAwMBAAIA9p8AAAAASUVORK5CYII="
        )
        mock_result = MagicMock()
        mock_result.data = [MagicMock(b64_json=valid_png_b64)]
        mock_openai.return_value.images.edit.return_value = mock_result
        with patch.dict(os.environ, {"OPENAI_API_KEY": "fake"}):
            result = process_image_chain(self.test_image, "test prompt", 1, 0)
            self.assertEqual(len(result), 4)  # Should return 4 values: final image, gif, gallery, status
            self.assertIn("Successfully generated", result[3])

if __name__ == '__main__':
    unittest.main() 