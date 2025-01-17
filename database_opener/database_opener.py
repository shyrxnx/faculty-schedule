import subprocess
import platform
import os

def find_xampp_path():
    """Try to find the XAMPP path automatically or ask the user."""
    possible_paths = [
        r"C:\xampp",                # Common path on Windows
        r"D:\xampp",                # Alternate drive
        "/opt/lampp",               # Common path on Linux/macOS
    ]
    
    # Check if any of the common paths exist
    for path in possible_paths:
        if os.path.exists(path):
            return path

    # Prompt the user if no common path is found
    print("Could not find XAMPP automatically. Please enter the XAMPP path:")
    user_path = input("Enter XAMPP installation path: ").strip()
    if os.path.exists(user_path):
        return user_path
    else:
        raise FileNotFoundError("The specified XAMPP path does not exist.")

def start_apache_mysql():
    """Start Apache and MySQL specifically."""
    system = platform.system()
    try:
        xampp_path = find_xampp_path()
        if system == "Windows":
            apache_cmd = os.path.join(xampp_path, "apache_start.bat")
            mysql_cmd = os.path.join(xampp_path, "mysql_start.bat")

            subprocess.Popen([apache_cmd], creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
            print("Apache server started.")
            subprocess.Popen([mysql_cmd], creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
            print("MySQL server started.")
        elif system in ["Linux", "Darwin"]:
            # Assuming lampp is in /opt/lampp
            xampp_script = os.path.join(xampp_path, "lampp")
            subprocess.run(["sudo", xampp_script, "startapache"], shell=True, check=True)
            print("Apache server started.")
            subprocess.run(["sudo", xampp_script, "startmysql"], shell=True, check=True)
            print("MySQL server started.")
        else:
            print("Unsupported operating system.")
    except Exception as e:
        print(f"Error starting services: {e}")

def stop_apache_mysql():
    """Stop Apache and MySQL specifically (forcefully)."""
    system = platform.system()
    try:
        if system == "Windows":
            # Kill Apache and MySQL processes by task name
            subprocess.Popen(["taskkill", "/F", "/IM", "httpd.exe"], shell=True)  # Apache (httpd)
            subprocess.Popen(["taskkill", "/F", "/IM", "mysqld.exe"], shell=True)  # MySQL (mysqld)
            print("Apache and MySQL servers stopped.")
        
        elif system in ["Linux", "Darwin"]:
            # Linux/macOS: Forcefully stop Apache and MySQL using pkill
            subprocess.Popen(["sudo", "pkill", "apache2"], shell=True)  # Apache on Linux
            subprocess.Popen(["sudo", "pkill", "mysql"], shell=True)   # MySQL on Linux
            print("Apache and MySQL servers stopped.")
        else:
            print("Unsupported operating system.")
    except Exception as e:
        print(f"Error stopping services: {e}")

