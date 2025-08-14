name: Rapid-Uploader-Bot
services:
  - name: Rapid-Uploader-Bot
    type: web
    env: python
    buildCommand: |
      apt-get update && apt-get install -y ffmpeg
      pip install --no-cache-dir -r requirements.txt
    startCommand: python main.py
