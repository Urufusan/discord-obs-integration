import subprocess
import multiprocessing
print("starting chat overlay")
def run_command(command):
    subprocess.call(command, shell=True)

if __name__ == "__main__":
    command1 = "python3 testflask.py"
    command2 = "python3 discordaggregator.py"

    # Create two processes for each command
    process1 = multiprocessing.Process(target=run_command, args=(command1,))
    process2 = multiprocessing.Process(target=run_command, args=(command2,))

    # Start both processes
    process1.start()
    process2.start()

    try:
        # Keep the script running until interrupted
        process1.join()
        process2.join()
    except KeyboardInterrupt:
        # If interrupted, terminate both processes
        process1.terminate()
        process2.terminate()
