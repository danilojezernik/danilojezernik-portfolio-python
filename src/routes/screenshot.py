"""
Route is used to get to the admin page where all the settings are
"""
from asyncio import wait_for

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from playwright.async_api import async_playwright
import os
from datetime import datetime
import asyncio
import validators

from src.domain.user import User
from src.services.security import get_current_user

router = APIRouter()

# Define the root media directory and the subdirectory for screenshots
media_root_directory = 'media'  # The root directory for all media files
screenshots_directory = os.path.join(media_root_directory, 'screenshots')  # Subdirectory for screenshots
os.makedirs(screenshots_directory, exist_ok=True)

class ScreenshotRequest(BaseModel):
    url: str

# SCREENSHOT PANEL
@router.post("/")
async def capture_screenshot(request: ScreenshotRequest):
    url = request.url  # Get the URL from the request body

    # Ensure that the URL has a proper scheme
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    # Validate the URL format
    if not validators.url(url):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    # Generate the file name and file path
    screenshot_filename = f"screenshot_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.png"
    screenshot_path = os.path.join(screenshots_directory, screenshot_filename)

    try:
        # Use Playwright to capture the screenshot
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            await page.wait_for_timeout(3000)  # Wait for 3 seconds
            await page.screenshot(path=screenshot_path, full_page=True)  # Capture the entire page
            await browser.close()
    except Exception as e:
        print(f"Failed to capture screenshot: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to capture screenshot: {str(e)}")

    asyncio.create_task(delete_file_after_delay(screenshot_path, 10))

    return FileResponse(screenshot_path, filename=screenshot_filename)

async def delete_file_after_delay(file_path: str, delay: int):
    """
    Delete the given file after the specified delay.

    :param file_path: Path to the file to be deleted.
    :param delay: Delay in seconds before the file is deleted.
    """
    await asyncio.sleep(delay)  # Wait for the specified delay
    if os.path.exists(file_path):
        os.remove(file_path)  # Delete the file
        print(f"File {file_path} has been deleted.")
    else:
        print(f"File {file_path} not found for deletion.")