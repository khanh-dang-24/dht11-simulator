import argparse
import csv
import time
import os
from datetime import datetime
from sensor_sim import DHT11Sim

def run_sim(output_csv="readings.csv", interval=1.0, duration=0, base_temp=26.0, base_hum=60.0):
    sim = DHT11Sim(base_temp=base_temp, base_hum=base_hum)
    header = ["timestamp", "temperature_c", "humidity_pct", "status"]
    first_write = not os.path.exists(output_csv)
    with open(output_csv, "a", newline="") as f:
        writer = csv.writer(f)
        if first_write:
            writer.writerow(header)
        start = time.time()
        count = 0
        try:
            while True:
                now = datetime.utcnow().isoformat() + "Z"
                t = sim.readTemperature()
                h = sim.readHumidity()
                if t is None or h is None:
                    status = "FAIL"
                    print(f"[{now}] Failed to read from DHT sensor!")
                    writer.writerow([now, "", "", status])
                else:
                    status = "OK"
                    print(f"[{now}] Temperature: {t:.1f} °C, Humidity: {h:.1f} %")
                    writer.writerow([now, f"{t:.1f}", f"{h:.1f}", status])
                f.flush()
                count += 1
                if duration > 0 and (time.time() - start) >= duration:
                    break
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nSimulation stopped by user.")
    print(f"Total samples: {count}. Logged to {output_csv}")

def main():
    parser = argparse.ArgumentParser(description="DHT11 Simulator - prints readings and logs to CSV.")
    parser.add_argument("--csv", "-o", default="readings.csv", help="Output CSV file path")
    parser.add_argument("--interval", "-i", type=float, default=1.0, help="Interval between readings (seconds)")
    parser.add_argument("--duration", "-d", type=float, default=0, help="Duration to run in seconds (0 = infinite)")
    parser.add_argument("--temp", type=float, default=26.0, help="Base temperature (°C)")
    parser.add_argument("--hum", type=float, default=60.0, help="Base humidity (%)")
    args = parser.parse_args()
    run_sim(output_csv=args.csv, interval=args.interval, duration=args.duration, base_temp=args.temp, base_hum=args.hum)

if __name__ == "__main__":
    main()
