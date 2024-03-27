import sys
import subprocess
import multiprocessing
from discord_OBS_overlay_config import runner_modules
import pprint

class TerminalColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    ORANGE = '\033[33m'

    @staticmethod
    def terminalpaint(color):
        if isinstance(color, str):
            if color.startswith("#"):
                color = color[1:]
            r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        elif isinstance(color, tuple) and len(color) == 3:
            r, g, b = color
        else:
            raise ValueError("Invalid color format")
        
        color_code = f"\x1b[38;2;{r};{g};{b}m"
        return color_code

    def print_ctext(self, _text, color="#964bb4"):
        color_code = self.terminalpaint(color)
        # _str_io_buf = StringIO()
        # pprint.pprint(object=_text, stream=_str_io_buf)
        # _raw_pp_str = _str_io_buf.getvalue()
        # del _str_io_buf
        _raw_pp_str = pprint.pformat(object=_text)
        _raw_pp_str = _raw_pp_str.strip()
        if _raw_pp_str:
            if _raw_pp_str.endswith("'"):
                _raw_pp_str = _raw_pp_str.strip("'")
            elif _raw_pp_str.endswith("\""):
                _raw_pp_str = _raw_pp_str.strip("\"")

            print(f"{self.terminalpaint(color)}{_raw_pp_str}{self.ENDC}")

tc = TerminalColors()

def run_command(command):
    subprocess.call(command, shell=True)

if __name__ == "__main__":    
    # Create processes for each command
    print("Starting D-ObS components...")

    processes = []
    filtered_args = []
    if len(sys.argv) > 1:
        filtered_args = sys.argv[1:]
    # print(filtered_args)
    # exit() 
    for cmd in runner_modules:
        if filtered_args:
            if cmd['label'] not in filtered_args:
                tc.print_ctext(f"Skipped loading [{cmd['label']}]", "#eba525")
                continue
        command = f'sh -c "cd {cmd["dir"]} && python3 {cmd["file"]}"'
        process = multiprocessing.Process(target=run_command, args=(command,))
        processes.append(process)
        tc.print_ctext(f"Loaded [{cmd['label']}]", "#37f026")
    
    # Start all processes
    for process in processes:
        process.start()

    try:
        # Keep the script running until interrupted
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        # If interrupted, terminate all processes
        for process in processes:
            process.terminate()
