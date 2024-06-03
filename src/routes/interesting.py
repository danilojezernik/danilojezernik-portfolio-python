"""
Route is used to get to the admin page where all the settings are
"""

import os
import platform
import subprocess

from fastapi import APIRouter

from src.domain.sleep import Sleep

router = APIRouter()


# SHUTDOWN COMPUTER
@router.get("/shutdown")
async def shut_down_pc():
    """
    Shutdowns the computer after a specified sleep time.

    Args:
        sleep (Sleep): Sleep time in seconds.

    Returns:
        dict: Shutdown action confirmation.
    """
    os.system(f'shutdown /s /t 1')

    return {'Action': f'computer shutdown was in 1s'}


# Get system information
@router.get("/sysinfo")
async def sys_info():
    """
    Retrieves system information based on the operating system.

    Returns:
        dict: System information.
    """
    os_type = platform.system()
    if os_type == "Windows":
        result = subprocess.run(['systeminfo'], capture_output=True, text=True, shell=True)
        sys_info_raw = result.stdout
        sys_info = {line.split(": ")[0].strip(): line.split(": ")[1].strip() for line in sys_info_raw.splitlines() if ": " in line}

    elif os_type == "Linux":
        result = subprocess.run(['uname', '-a'], capture_output=True, text=True)
        uname_info = result.stdout.strip()
        result = subprocess.run(['lsb_release', '-a'], capture_output=True, text=True)
        lsb_info_raw = result.stdout.strip()
        sys_info = {"Uname Info": uname_info}
        sys_info.update({line.split(":")[0].strip(): line.split(":")[1].strip() for line in lsb_info_raw.splitlines() if ":" in line})

    else:
        return {'error': 'Unsupported operating system'}

    return sys_info


@router.get("/youtube")
async def donload_youtube():
    # TODO: Add video downloader
    return {'Action': 'video downloaded'}
