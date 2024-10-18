import shutil
import unittest
import os
from unittest.mock import patch
from app.server import run_job_steps


class TestJobSteps(unittest.TestCase):

    @patch("subprocess.run")
    def test_run_job_steps_success(self, mock_subprocess):
        # Mock subprocess to simulate successful command execution
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = "Success!"
        mock_subprocess.return_value.stderr = ""

        # Define a mock job for testing
        mock_jobs = {
            "build": {
                "steps": [
                    {
                        "name": "Checkout",
                        "run": "git clone git@github.com:aodeniyide/sample-program.git build",
                    },
                    {"name": "Makefile", "run": "make"},
                ]
            }
        }

        # Simulate creating the artifact 'hello' that 'make' would generate
        # Make sure the directory exists
        # Simulate the artifact
        os.makedirs("build", exist_ok=True)  
        with open("build/hello", "w") as f:
            f.write("This is the build artifact.")

        # Run the steps
        logs, success, artifact = run_job_steps(
            "build", mock_jobs["build"], repo_dir="build"
        )

        # Assertions to ensure the steps completed successfully
        self.assertTrue(success)
        self.assertIsNotNone(artifact)
        self.assertTrue(os.path.exists(artifact))

    
    def tearDown(self):
        # Remove the 'build' directory and 'artifacts' directory if they exist
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('artifacts'):
            shutil.rmtree('artifacts')
