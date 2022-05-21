import cloudinary
import cloudinary.uploader
import cloudinary.api

from dotenv import dotenv_values

config = dotenv_values('.env')

cloudinary.config(
    cloud_name=config["CLOUDINARY_CLOUD_NAME"],
    api_key=config["CLOUDINARY_API_KEY"],
    api_secret=config["CLOUDINARY_API_SECRET"],
    secure=True
)

cloudinary.uploader.upload_large(
    "videos/C1114.mp4",
    resource_type="image",
    public_id="Automatic Video Editor/C1114"
)
