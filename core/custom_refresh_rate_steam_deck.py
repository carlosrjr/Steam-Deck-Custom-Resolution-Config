import subprocess
import argparse

def read_args():
    parser = argparse.ArgumentParser(description='Script to configure custom resolution.')
    parser.add_argument('-w', '--width', type=int, default=2560, help='Resolution width')
    parser.add_argument('-H', '--height', type=int, default=1080, help='Resolution height')
    parser.add_argument('-o', '--output', type=str, default='DisplayPort-0', help='Video output. Hint: You can list available outputs using the command: xrandr --listmonitors')
    parser.add_argument('-r', '--refresh_rate', type=int, default=120, help='Refresh rate')
    parser.add_argument('--manual', action='store_true', help='Use manual configuration')
    return parser.parse_args()

def confirm_execution():
    disclaimer = """
    DISCLAIMER: This operation may cause display issues or a black screen. I am not responsible for any potential hardware damage. Proceed at your own risk.
    """
    print(disclaimer)

    option = input("This operation may cause a black screen. Are you sure you want to continue? (y/n): ")
    return option.lower() in ['y', 'yes']

def execute_configuration_manually(width, height, refresh_rate, output):
    if not confirm_execution():
        print('Operation aborted.')
        return

    output_cvt = subprocess.check_output(['cvt', str(width), str(height), str(refresh_rate)]).decode()
    modeline_index = output_cvt.find("Modeline")  # Finding the index of the line starting with "Modeline"
    modeline = output_cvt[modeline_index:]
    modeline = modeline.replace("Modeline", "").replace('"', "").strip()
    modeline_args = modeline.split() 
    mode_name = f"{width}x{height}_{int(refresh_rate)}.00"
    subprocess.run(['xrandr', '--newmode'] + modeline_args)
    subprocess.run(['xrandr', '--addmode', output, mode_name])
    subprocess.run(['xrandr', '--output', output, '--mode', mode_name])

def execute_custom_resolution_configuration(width, height, output, refresh_rate):
    if not confirm_execution():
        print('Operation aborted.')
        return

    # setcustomres installation instructions
    installation_instructions = """
    # The setcustomres tool is required to configure custom resolution on the system. It is available in the AUR (Arch User Repository).
    # Make sure to have yay installed before proceeding. If you don't have yay, you can install it with the following command:
    # sudo pacman -S yay

    # Once yay is installed, you can install setcustomres using the following command:
    # yay -S setcustomres
    """

    # Command to be executed
    command = ["/usr/bin/setcustomres", "-w", str(width), "-h", str(height), "-o", output, "-r", str(refresh_rate)]

    # Checking if setcustomres is installed, if not, display installation instructions
    try:
        subprocess.run(['setcustomres', '-v'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("setcustomres is not installed. It is available in the AUR (Arch User Repository). Make sure to have yay installed before proceeding. Here are the instructions:\n")
        print(installation_instructions)
        return

    # Execute the command
    subprocess.run(command)

if __name__ == '__main__':
    args = read_args()

    if args.manual:
        execute_configuration_manually(args.width, args.height, args.refresh_rate, args.output)
    else:
        execute_custom_resolution_configuration(args.width, args.height, args.output, args.refresh_rate)