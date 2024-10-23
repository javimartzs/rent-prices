import subprocess 
import time 



def run_etl_pipeline():

    subprocess.run(['python', 'code/1_extract/01_rooms.py'], check=True)
    subprocess.run(['python', 'code/1_extract/01_rent.py'], check=True)
    subprocess.run(['python', 'code/2_transform/02_rooms.py'], check=True)
    subprocess.run(['python', 'code/2_transform/02_rent.py'], check=True) 
    subprocess.run(['python', 'code/3_load/03_loadfiles.py'], check=True)


if __name__ == '__main__':
    start_time = time.time()
    run_etl_pipeline()
    end_time = time.time()
    print(f"Pipeline ejecutada en {(end_time - start_time) / 3600} horas")