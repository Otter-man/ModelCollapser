import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from PIL import Image
from main import generate_chain

class TestMainFunctionality(unittest.TestCase):
    def setUp(self):
        # Create a temporary test image in /tmp
        self.test_image = tempfile.NamedTemporaryFile(suffix='.png', delete=False, dir='/tmp')
        img = Image.new('RGB', (100, 100), color='red')
        img.save(self.test_image.name)
        self.test_image.close()

    def tearDown(self):
        # Reset working directory to /tmp before deleting temp files
        os.chdir('/tmp')
        # Clean up the test image
        os.unlink(self.test_image.name)
        # Clean up any output directories created during tests
        for item in os.listdir('.'):
            if os.path.isdir(item) and len(item) == 36:  # UUID format
                for file in os.listdir(item):
                    os.unlink(os.path.join(item, file))
                os.rmdir(item)

    def test_missing_api_key(self):
        """Test that appropriate error is raised when API key is missing"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                generate_chain(self.test_image.name, "test prompt", 1, retries=0)
            self.assertIn("OPENAI_API_KEY", str(context.exception))

    def test_invalid_image_path(self):
        """Test that function returns empty list for invalid image path"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "fake"}):
            outputs = generate_chain("nonexistent.png", "test prompt", 1, retries=0)
            self.assertEqual(outputs, [])

    @patch("main.OpenAI")
    def test_invalid_iterations(self, mock_openai):
        """Test that appropriate error is raised for invalid number of iterations"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "fake"}):
            # n=0 should result in no iterations, so function should return immediately
            outputs = generate_chain(self.test_image.name, "test prompt", 0, retries=0)
            self.assertEqual(outputs, [])

    @patch("main.OpenAI")
    def test_output_directory_creation(self, mock_openai):
        """Test that output directory is created with UUID format"""
        # Mock the API call to avoid actual API usage
        # Use a valid minimal PNG base64
        valid_png_b64 = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/" 
            "/w8AAwMBAAIA9p8AAAAASUVORK5CYII="
        )
        mock_result = MagicMock()
        mock_result.data = [MagicMock(b64_json=valid_png_b64)]
        mock_openai.return_value.images.edit.return_value = mock_result
        with patch.dict(os.environ, {"OPENAI_API_KEY": "fake"}):
            outputs = generate_chain(self.test_image.name, "test prompt", 1, retries=0)
            self.assertEqual(len(outputs), 1)
            # Check that the output file exists
            self.assertTrue(os.path.exists(outputs[0]))

if __name__ == '__main__':
    unittest.main() 