import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from PIL import Image
from app import process_image_chain

class TestAppFunctionality(unittest.TestCase):
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

    def test_missing_image(self):
        """Test handling of missing image input"""
        result = process_image_chain(None, "test prompt", 3, 0)
        self.assertEqual(result[3], "Please upload an image")

    def test_missing_prompt(self):
        """Test handling of missing prompt"""
        result = process_image_chain(self.test_image, "", 3, 0)
        self.assertEqual(result[3], "Please enter a prompt")

    def test_invalid_iterations(self):
        """Test handling of invalid number of iterations"""
        result = process_image_chain(self.test_image, "test prompt", 0, 0)
        self.assertEqual(result[3], "Number of iterations must be at least 1")

    @patch("main.OpenAI")
    def test_temp_file_cleanup(self, mock_openai):
        """Test that temporary files are cleaned up (mocked)"""
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
            # Should return 4 values: final image, gif, gallery, status
            self.assertEqual(len(result), 4)
            self.assertIn("Successfully generated", result[3])

if __name__ == '__main__':
    unittest.main() 