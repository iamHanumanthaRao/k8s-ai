import subprocess

# Input the command you want to execute
command = input("Enter the command you want to run: ")

# Use subprocess to run the command
try:
    result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("Command Output:")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Error occurred: {e}")