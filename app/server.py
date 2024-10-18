#!/usr/bin/env python3

import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for
from flask import send_from_directory
import shutil

app = Flask(__name__)


def run_job_steps(job_name, job_details, repo_dir=None):
    """
    Execute a series of job steps for a C program pipeline.

    Sequentially runs shell commands based on the predefined steps within the "jobs" dict"

    Returns:
      output_logs
      success
      artifact_path
    """
    output_logs = []
    success = True  # Track if all steps are successful
    artifact_path = None

    for step in job_details["steps"]:
        command = step["run"].split()  # Split command into list for subprocess

        try:
            # Run the command in the appropriate directory.
            # This means that we want to run our make command in the dir of our cloned repo.
            if repo_dir:
                result = subprocess.run(
                    command, capture_output=True, text=True, cwd=repo_dir
                )
            else:
                result = subprocess.run(command, capture_output=True, text=True)

            stdout_output = result.stdout.strip()
            stderr_output = result.stderr.strip()

            if result.returncode == 0:
                output_logs.append(
                    {
                        "step": step["name"],
                        "command": step["run"],
                        "output": stdout_output
                        + ("\n" + stderr_output if stderr_output else ""),
                        "error": None,
                    }
                )
            else:
                output_logs.append(
                    {
                        "step": step["name"],
                        "command": step["run"],
                        "output": stdout_output,
                        "error": stderr_output,
                    }
                )
                success = False
                break  # If any command fails, lets break out before wasting any more time.

            # If the step is "make", we know it is suppose to generate an artifact.
            # Hardcoding artifact name does not seem ideal, but for POC reasons, could be OK.
            # Creating the artifact and storing it on the filesystem. We want to make sure we create the directory if it does not exist.
            # Move the C program artifact to the appropriate dir.
            if step["name"] == "Makefile" and success:
                generated_artifact = os.path.join(repo_dir, "hello")
                artifact_folder = os.path.join("artifacts")

                os.makedirs(artifact_folder, exist_ok=True)

                artifact_path = os.path.join(artifact_folder, "hello")
                shutil.move(generated_artifact, artifact_path)

        except Exception as e:
            output_logs.append(
                {
                    "step": step["name"],
                    "command": step["run"],
                    "output": None,
                    "error": str(e),
                }
            )
            success = False
            break

    return output_logs, success, artifact_path


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        repo_url = request.form["repo_url"]
        if repo_url:
            return redirect(url_for("start_page", repo_url=repo_url))

    return render_template("index.html")


@app.route("/start/<path:repo_url>", methods=["GET", "POST"])
def start_page(repo_url):
    if request.method == "POST":
        repo_dir = "build"  # Folder to clone the repo into

        jobs = {
            "build": {
                "steps": [
                    {"name": "Checkout", "run": f"git clone {repo_url} {repo_dir}"},
                    {"name": "Makefile", "run": "make"},
                ]
            }
        }

        # Clone the repository and run the job steps
        clone_command = f"git clone {repo_url} {repo_dir}"
        clone_result = subprocess.run(
            clone_command.split(), capture_output=True, text=True
        )

        # Check if cloning was successful
        if clone_result.returncode == 0:
            # Run the Makefile step in the cloned repo directory which contains our makefile
            build_logs, build_success, artifact_path = run_job_steps(
                "build", jobs["build"], repo_dir=repo_dir
            )
        else:
            # If cloning fails, log the error and stop
            build_logs = [
                {
                    "step": "Clone repository",
                    "command": clone_command,
                    "output": clone_result.stdout,
                    "error": clone_result.stderr,
                }
            ]
            build_success = False
            artifact_path = None

        # Pass the logs and artifact to the template
        return render_template(
            "start.html",
            repo_url=repo_url,
            build_logs=build_logs,
            artifact_path=artifact_path,
        )

    # Initially only show the Start button
    return render_template("start.html", repo_url=repo_url, build_logs=None)


@app.route("/download/<filename>")
def download_artifact(filename):
    artifact_dir = "artifacts"
    return send_from_directory(artifact_dir, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(port=8000, debug=True)

