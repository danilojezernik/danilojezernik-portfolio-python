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
async def shut_down_pc(sleep: Sleep):
    """
    Shutdowns the computer after a specified sleep time.

    Args:
        sleep (Sleep): Sleep time in seconds.

    Returns:
        dict: Shutdown action confirmation.
    """
    os.system(f'shutdown /s /t {sleep.number}')

    return {'Action': f'computer shutdown was in {sleep.number}s'}


# Get system information
@router.get("/sysinfo")  # Defines a route to retrieve system information
async def sys_info():  # Defines a function to fetch system information asynchronously
    """
    Retrieves system information based on the operating system.

    Returns:
        dict: System information.
    """
    os_type = platform.system()  # Detects the operating system type

    if os_type == "Windows":  # Checks if the operating system is Windows
        result = subprocess.run(['systeminfo'], capture_output=True, text=True,
                                shell=True)  # Executes a command to get system information on Windows
        sys_info_raw = result.stdout  # Stores the raw system information output

        sys_info = {}  # Initializes an empty dictionary to store processed system information
        for line in sys_info_raw.splitlines():  # Iterates through each line of the raw system information
            if ": " in line:  # Checks if the line contains a colon followed by a space
                key, value = line.split(": ", 1)  # Splits the line into key-value pairs based on the colon and space
                sys_info[
                    key.strip()] = value.strip()  # Adds the key-value pair to the sys_info dictionary after stripping whitespace

    elif os_type == "Linux":  # Checks if the operating system is Linux
        result = subprocess.run(['uname', '-a'], capture_output=True,
                                text=True)  # Executes a command to get system information on Linux
        uname_info = result.stdout.strip()  # Stores the raw output of the uname command

        result = subprocess.run(['lsb_release', '-a'], capture_output=True,
                                text=True)  # Executes a command to get system information on Linux using lsb_release
        lsb_info_raw = result.stdout.strip()  # Stores the raw output of the lsb_release command

        sys_info = {"Uname Info": uname_info}  # Initializes the sys_info dictionary with uname information
        for line in lsb_info_raw.splitlines():  # Iterates through each line of the raw lsb_release output
            if ":" in line:  # Checks if the line contains a colon
                key, value = line.split(":", 1)  # Splits the line into key-value pairs based on the colon
                sys_info[
                    key.strip()] = value.strip()  # Adds the key-value pair to the sys_info dictionary after stripping whitespace

    else:  # Executes if the operating system is not Windows or Linux
        return {
            'error': 'Unsupported operating system'}  # Returns an error message indicating that the operating system is not supported

    return sys_info  # Returns the processed system information dictionary


@router.get("/youtube")
async def donload_youtube():
    # TODO: Add video downloader
    return {'Action': 'video downloaded'}
