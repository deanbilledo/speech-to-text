import os
import sys
import zipfile
import requests
import shutil
import subprocess
import tempfile

def install_ffmpeg():
    """Download and install FFmpeg for Windows"""
    print("Downloading FFmpeg...")
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    
    # Create installation directory
    install_dir = os.path.join(os.path.expanduser("~"), "ffmpeg")
    if not os.path.exists(install_dir):
        os.makedirs(install_dir)
    
    # Download zip file
    zip_path = os.path.join(tempfile.gettempdir(), "ffmpeg.zip")
    try:
        response = requests.get(ffmpeg_url, stream=True)
        response.raise_for_status()
        
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
            print(f"Downloaded FFmpeg to {zip_path}")
        
        # Extract zip file
        print(f"Extracting to {install_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get the name of the top-level directory in the zip
            top_dir = zip_ref.namelist()[0].split('/')[0]
            zip_ref.extractall(tempfile.gettempdir())
            
            # Move extracted directory to install location
            extracted_path = os.path.join(tempfile.gettempdir(), top_dir)
            if os.path.exists(install_dir):
                shutil.rmtree(install_dir)
            shutil.move(extracted_path, install_dir)
        
        # Add to PATH (temporary for this session)
        bin_dir = os.path.join(install_dir, "bin")
        os.environ["PATH"] = bin_dir + os.pathsep + os.environ["PATH"]
        
        # Test if FFmpeg is now available
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True)
            if result.returncode == 0:
                print("FFmpeg installed and working!")
                print(f"FFmpeg version: {result.stdout.splitlines()[0]}")
                
                # Instructions for permanent PATH setup
                print("\n==== IMPORTANT: TO MAKE FFMPEG AVAILABLE PERMANENTLY ====")
                print(f"Add this directory to your system PATH: {bin_dir}")
                print("1. Right-click on 'This PC' or 'My Computer' and select 'Properties'")
                print("2. Click on 'Advanced system settings'")
                print("3. Click on 'Environment Variables'")
                print("4. Under 'System variables', find 'Path', select it and click 'Edit'")
                print("5. Click 'New' and add this path:")
                print(f"   {bin_dir}")
                print("6. Click 'OK' on all dialogs to save changes")
                print("7. Restart your terminal or IDE")
                print("=======================================================\n")
                return True
            else:
                print("FFmpeg installation may have failed. Check the error below:")
                print(result.stderr)
                return False
        except Exception as e:
            print(f"Error testing FFmpeg: {e}")
            return False
            
    except Exception as e:
        print(f"Error installing FFmpeg: {e}")
        return False
    finally:
        # Clean up the zip file
        if os.path.exists(zip_path):
            os.remove(zip_path)

if __name__ == "__main__":
    if sys.platform != "win32":
        print("This script is designed for Windows only.")
        print("For other platforms, please install FFmpeg using your package manager.")
        sys.exit(1)
        
    print("FFmpeg Installer for Windows")
    print("============================")
    install_ffmpeg()