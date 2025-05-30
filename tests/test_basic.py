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
        self.assertTrue(os.path.exists("main.py"), "main.py exists")
        self.assertTrue(os.path.exists("app.py"), "app.py exists")
        self.assertTrue(os.path.exists("requirements.txt"), "requirements.txt exists")

if __name__ == '__main__':
    unittest.main() 