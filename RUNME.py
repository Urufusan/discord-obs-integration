import subprocess
import multiprocessing
print("starting chat overlay")
def run_command(command):
    subprocess.call(command, shell=True)

if __name__ == "__main__":
    #TODO: Make a nice little automated thing for starting the main files, list them out in a json file and the files are automatically found and ran, PWD set ofc.
    command1 = """sh -c "cd src/server/ && python3 web_server_main.py" """.strip()
    command2 = """sh -c "cd src/aggregator/ && python3 discord_aggregator.py" """.strip()

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
