from PIL import Image
import numpy as np
import pprint
import csv
import sys

colour_array = iter([
   (230, 190, 255),
   (170, 110, 40),
   (255, 250, 200),
   (128, 0, 0),
   (170, 255, 195),
   (128, 128, 0),
   (255, 215, 180),
   (0, 0, 128),
   (128, 128, 128),
   (255, 255, 255),
   (230, 25, 75),
   (60, 180, 75),
   (255, 225, 25),
   (0, 130, 200),
   (245, 130, 48),
   (145, 30, 180),
   (70, 240, 240),
   (240, 50, 230),
   (210, 245, 60),
   (250, 190, 190),
   (0, 128, 128)
])

mem_arr = [None for i in range(1920 * 1080)]
task_arr = {} 
heap_min = 671160072
with open("teraterm.log") as f:
    log_reader = csv.DictReader(f)

    for row_no, row in enumerate(log_reader):
        #try:
            task = row['Task']
            addr = int(row['Addr'], base=16) - heap_min
            if row['Action'] == 'M':
                #Malloc
                size = int(row['Size'], base=16)
                if task not in task_arr:
                    task_arr[task] = np.array(next(colour_array), 'uint8') 
                for i in range(size):
                    if mem_arr[i + addr]:
                        print("Memory collision")
                        sys.exit(0)
                    if(i == 0):
                        mem_arr[addr + i] = (size, task_arr[task])
                    else:
                        mem_arr[addr + i] = task_arr[task]

            elif row['Action'] == 'F':
                if(None == mem_arr[addr]):
                    print(f"{row} - Double Free")
                else:
                    if type(mem_arr[addr]) != tuple:
                        print("Incorrect type")
                    size = mem_arr[addr][0]
                    for i in range(size):
                        mem_arr[addr + i] = None 
            else:
                raise ValueError("Row format incorrect")
#        except Exception as err:
 #           print(f"{row_no} - {err}")

pprint.pprint(task_arr)

for index, m in enumerate(mem_arr):
    if m is None:
        mem_arr[index] = np.array([0,0,0], 'uint8')
    elif type(m) == tuple:
        mem_arr[index] = m[1]

bmp = np.reshape(mem_arr, (1080,1920,3))
im = Image.fromarray(bmp, 'RGB')

im.save("output.bmp")
