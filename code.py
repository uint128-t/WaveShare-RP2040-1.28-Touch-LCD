import board,os,gc,microcontroller

print(f"ID: {board.board_id}")
print(f"Board: {os.uname().machine}")
print(f"Chip: {os.uname().sysname}")
print(f"CPy Ver: {os.uname().release}")
print(f"Serial: {microcontroller.cpu.uid}")
print(f"Memory: {gc.mem_alloc()+gc.mem_free()/1024} MB")
print(f"CPU Freq: {microcontroller.cpu.frequency/1024/1024} MHz")
print(f"CPU Temp: {microcontroller.cpu.temperature} C")

import programs,ui