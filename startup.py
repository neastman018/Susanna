"""
Pretty Sure this is not needed anymore, replaced wiht docker-compose.yaml
"""
from subprocess import run
from threading import Thread
from datetime import datetime

def run_script(script_name):
    run(script_name, shell=True)

if __name__ == "__main__":
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"{current_time}.txt", "w") as file:
        file.write("This file was created at " + current_time + "\n")


    t1 = Thread(target=run_script, args=("cd backend && uvicorn app.server:app --host 0.0.0.0 --port 4000 --reload",))
    t2 = Thread(target=run_script, args=("cd frontend && npm run dev",))

    t1.start()
    t2.start()
    t1.join()
    t2.join()



    

