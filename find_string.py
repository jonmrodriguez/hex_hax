#! /usr/local/bin/python2.7

from __future__ import print_function
import sys

CONSTANTS = {
  "do_print_at_intervals": False,
  "print_interval": 100000,
}

RING_BUFFER_SIZE = 400
RING_BUFFER = [0 for i in range(0, RING_BUFFER_SIZE)]
# the below is cuz for some reason directly setting a global wasn't working
SETTABLE_VAR = {"RING_BUFFER_LAST_INDEX_WRITTEN": 0}

# takes a number like 58 or 255
def ringbuffer_writebyte(byte, file_index):
  ringbuffer_idx = file_index % RING_BUFFER_SIZE
  RING_BUFFER[ringbuffer_idx] = byte
  SETTABLE_VAR["RING_BUFFER_LAST_INDEX_WRITTEN"] = ringbuffer_idx

# returns a string! The byte numbers are converted to chars
def ringbuffer_readstring_last(length):
  assert length < RING_BUFFER_SIZE, "ringbuffer_readstring_last: length must be < RING_BUFFER_SIZE"
  result_string = ""
  
  RING_BUFFER_LAST_INDEX_WRITTEN = SETTABLE_VAR["RING_BUFFER_LAST_INDEX_WRITTEN"]
  
  for i in range(1, length + 1):
    ringbuffer_idx = RING_BUFFER_LAST_INDEX_WRITTEN - length + i

    while ringbuffer_idx < 0:
      ringbuffer_idx += RING_BUFFER_SIZE
    while ringbuffer_idx >= RING_BUFFER_SIZE:
      ringbuffer_idx -= RING_BUFFER_SIZE
    
    byte = RING_BUFFER[ringbuffer_idx]
    char = chr(byte)
    # print(ringbuffer_idx, char)
    result_string += char

  return result_string


def main_loop(disk_filename, query):
  with open(disk_filename, "rb") as fil:
    
    byte_idx = 0
    byte = fil.read(1)
    while byte != "":
      byte = ord(byte)
      ringbuffer_writebyte(byte, byte_idx)

      if CONSTANTS["do_print_at_intervals"]:
        if 0 == byte_idx % CONSTANTS["print_interval"]:
          print("... bytes[" + str(byte_idx - (len(query) - 1)) + " - " + str(byte_idx) + "] = " + ringbuffer_readstring_last(len(query)))

      # the big comparison
      # in python, strings can ==
      if ringbuffer_readstring_last(len(query)) == query:
        print('FOUND "' + query + '" AT BYTE OFFSET: ' + str(byte_idx - len(query) + 1))

      # wend
      byte = fil.read(1)
      byte_idx += 1


if __name__ == "__main__":
  if len(sys.argv) < 3:
    print('usage: find_string.py diskfile.hex KEYWORD')
    sys.exit(1)
  
  disk_filename = sys.argv[1]
  print("disk: " + disk_filename)
  query = sys.argv[2]
  print("query: " + query)
  print()

  main_loop(disk_filename, query)
  print()

