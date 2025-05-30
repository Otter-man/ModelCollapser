import unittest
from PIL import Image
import os

class TestBasicFunctionality(unittest.TestCase):
    def test_requirements_installed(self):
        """Test that required packages are installed"""
        import openai
        import gradio
        from PIL import Image
        
        self.assertTrue(True, "All required packages are installed")

    def test_main_files_exist(self):
        """Test that main project files exist"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assertTrue(os.path.exists(os.path.join(base_dir, "main.py")), "main.py exists")
        self.assertTrue(os.path.exists(os.path.join(base_dir, "app.py")), "app.py exists")
        self.assertTrue(os.path.exists(os.path.join(base_dir, "requirements.txt")), "requirements.txt exists")

if __name__ == '__main__':
    unittest.main() 