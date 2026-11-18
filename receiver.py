import serial
import matplotlib.pyplot as plt
import numpy as np
import time

PORT = "/dev/cu.usbserial-0001"
BAUD = 115200
INTERVAL = 0.01
RECONNECT_DELAY = 2

def main():
  samples = []
  plt.ion() # turns on interactive mode
  fig, ax = plt.subplots()
  ser = None
  freqs = None
  mag = None
  was_retrying = False

  while True:
    try:
      ser = open_serial(PORT, BAUD)
      if was_retrying:
        print()
      print("Device connected...")
      while True:
        sample = read_sample(ser)
        if sample is None:
          continue
        
        samples.append(sample)
        samples = samples[-200:]

        if len(samples) >= 200:
          freqs, mag = analyze(samples, INTERVAL)
          update_plot(ax, freqs, mag)
    except serial.SerialException:
      samples.clear()
      show_disconnected(ax)
      animate_retry(ser)
      was_retrying = True
      

def open_serial(port, baud):
  return serial.Serial(port, baud)

def read_sample(ser):
  rawData = ser.readline()
  try:
    f = float(rawData.decode().strip())
    return f
  except ValueError:
    return None

def analyze(samples, interval):
  npSamples = np.array(samples)
  npSamples = npSamples - np.mean(npSamples)

  fft = np.fft.rfft(npSamples)
  mag = np.abs(fft)
  freqs = np.fft.rfftfreq(len(npSamples), interval)
  return freqs, mag

def update_plot(ax, freqs, mag):
  ax.clear()
  ax.set_xlabel("Frequency (Hz)")
  ax.set_ylabel("Magnitude")
  ax.plot(freqs, mag)
  plt.pause(0.001)

def show_disconnected(ax):
  ax.clear()
  ax.set_title("Device disconnected - no data")
  ax.set_xlabel("Frequency (Hz)")
  ax.set_ylabel("Magnitude")
  plt.pause(0.001)

def animate_retry(ser):
  if ser is not None:
    ser.close()
  for i in range(4):
    dots = "." * i
    print(f"\r\033[KDevice disconnected, retrying{dots}", end="", flush=True)
    time.sleep(RECONNECT_DELAY / 3.0)

if __name__ == "__main__":
  main()