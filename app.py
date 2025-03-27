from flask import Flask, request, render_template, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

# Folder to store downloaded videos
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Full path to ffmpeg
FFMPEG_PATH = r"D:\New folder (2)\Downloads\ffmpeg-2025-03-06-git-696ea1c223-essentials_build\ffmpeg-2025-03-06-git-696ea1c223-essentials_build\bin\ffmpeg.exe"  # Make sure this is the correct path

# Function to download the video
def download_video(url, quality):
    # Format map based on quality selection
    format_map = {
        "2160p": "bestvideo[height<=2160]+bestaudio/best",
        "4K": "bestvideo[height<=2160]+bestaudio/best",
        "1080p": "bestvideo[height<=1080]+bestaudio/best",
        "720p": "bestvideo[height<=720]+bestaudio/best",
        "480p": "bestvideo[height<=480]+bestaudio/best",
        "audio": "bestaudio/best"
    }

    # Options for yt-dlp, including ffmpeg location
    ydl_opts = {
        'format': format_map.get(quality, 'best'),  # Default to best quality
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',  # Save path for video
        'ffmpeg_location': FFMPEG_PATH  # Path to ffmpeg
    }

    # Download video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)  # Extract video info and download
        filename = ydl.prepare_filename(info)  # Get the filename
        return os.path.basename(filename)  # Return only the filename

# Route for the homepage
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["url"]  # Get video URL from form
        quality = request.form["quality"]  # Get selected quality
        try:
            # Call download function
            filename = download_video(video_url, quality)
            return render_template("index.html", message="Download complete!", filename=filename)
        except Exception as e:
            return render_template("index.html", message=f"Error: {str(e)}")
    
    return render_template("index.html")

# Route to serve downloaded files
@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
