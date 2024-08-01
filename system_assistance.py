import tkinter as tk
import socket

import numpy as np
import wmi
import psutil
import platform
import subprocess

from matplotlib import pyplot as plt
from tabulate import tabulate


class SystemMonitor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("System Monitor")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the title
        title_frame = tk.Frame(self, bg="blue", padx=10, pady=10)
        title_frame.pack(fill="x")

        title_label = tk.Label(title_frame, text="System Monitor", font=("Helvetica", 24, "bold"), fg="white",
                               bg="blue")
        title_label.pack()

        # Create frames for each section
        cpu_frame = self.create_section("CPU", 100, 100, self.show_cpu_info)
        battery_frame = self.create_section("Battery", 300, 100, self.show_battery_info)
        system_info_frame = self.create_section("System Information", 500, 100, self.show_system_info)
        updates_frame = self.create_section("System Updates", 100, 300, self.show_system_updates_info)
        disk_usage_frame = self.create_section("Disk Usage", 300, 300, self.show_disk_usage_info)
        security_frame = self.create_section("Security", 500, 300, self.show_security_info)


    def create_section(self, title, x, y, command=None):
        frame = tk.Frame(self, relief="raised", bd=2)
        frame.place(x=x, y=y, width=200, height=150)

        label = tk.Label(frame, text=title, font=("Helvetica", 14, "bold"))
        label.pack(pady=5)

        if command:
            button = tk.Button(frame, text="Open", command=command)
            button.pack(pady=5)

        return frame

    def show_cpu_info(self):
        cpu_window = tk.Toplevel(self)
        cpu_window.title("System Memory")
        cpu_window.geometry("400x300")

        title_label = tk.Label(cpu_window, text="System Memory", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        cpu_count_label = tk.Label(cpu_window, text=f"CPU Count: {psutil.cpu_count(logical=False)}", font=("Helvetica", 12))
        cpu_count_label.pack()

        cpu_percent_label = tk.Label(cpu_window, text=f"CPU Percent: ", font=("Helvetica", 12))
        cpu_percent_label.pack()

        main_core_count_label = tk.Label(cpu_window, text=f"Main Core Count: {psutil.cpu_count()}", font=("Helvetica", 12))
        main_core_count_label.pack()

        ram_info = psutil.virtual_memory()
        total_ram_label = tk.Label(cpu_window, text=f"Total RAM: {self.convert_bytes(ram_info.total)} GB", font=("Helvetica", 12))
        total_ram_label.pack()

        available_ram_label = tk.Label(cpu_window, text=f"Available RAM: {self.convert_bytes(ram_info.available)} GB", font=("Helvetica", 12))
        available_ram_label.pack()

        used_ram_label = tk.Label(cpu_window, text=f"Used RAM: {self.convert_bytes(ram_info.used)} GB", font=("Helvetica", 12))
        used_ram_label.pack()

        free_ram_label = tk.Label(cpu_window, text=f"Free RAM: {self.convert_bytes(ram_info.free)} GB", font=("Helvetica", 12))
        free_ram_label.pack()

        self.update_cpu_percent(cpu_percent_label)

    def show_battery_info(self):
        battery_window = tk.Toplevel(self)
        battery_window.title("Battery Information")
        battery_window.geometry("400x300")

        title_label = tk.Label(battery_window, text="Battery Information", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        self.status_label = tk.Label(battery_window, text="", font=("Helvetica", 12))
        self.status_label.pack()

        self.charge_label = tk.Label(battery_window, text="", font=("Helvetica", 12))
        self.charge_label.pack()

        self.battery_canvas = tk.Canvas(battery_window, width=200, height=50, bg="white", highlightthickness=0)
        self.battery_canvas.pack()

        self.plugged_in_label = tk.Label(battery_window, text="", font=("Helvetica", 12))
        self.plugged_in_label.pack()

        self.update_battery_info()

    def update_battery_info(self):
        battery = psutil.sensors_battery()
        if battery is None:
            self.status_label.config(text="No battery is detected.")
            self.charge_label.config(text="")
            self.plugged_in_label.config(text="")
        else:
            self.status_label.config(text=f"Status: {self.get_battery_status(battery.power_plugged)}")
            self.charge_label.config(text=f"Charge: {battery.percent}%")
            self.draw_battery(battery.percent)
            self.plugged_in_label.config(text=f"Plugged In: {battery.power_plugged}")

        self.after(1000, self.update_battery_info)

    def get_battery_status(self, plugged_in):
        return "Charging" if plugged_in else "Discharging"

    def draw_battery(self, charge_percent):
        self.battery_canvas.delete("charge")
        width = 200
        height = 50
        fill_color = "green" if charge_percent > 20 else "red"
        self.battery_canvas.create_rectangle(0, 0, width * (charge_percent / 100), height, fill=fill_color, outline="")

    def update_cpu_percent(self, label):
        cpu_percent = psutil.cpu_percent(interval=1)
        label.config(text=f"CPU Percent: {cpu_percent}%", font=("Helvetica", 12))
        self.after(1000, lambda: self.update_cpu_percent(label))

    def convert_bytes(self, bytes):
        # Function to convert bytes to GB
        return round(bytes / (1024 ** 3), 2)

    def show_system_info(self):
        system_info_window = tk.Toplevel(self)
        system_info_window.title("System Information")
        system_info_window.geometry("600x400")

        title_label = tk.Label(system_info_window, text="System Information", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Fetch system information using platform module
        os_info = platform.uname()
        os_name_label = tk.Label(system_info_window, text=f"OS Name: {os_info.system} {os_info.release}",
                                 font=("Helvetica", 12))
        os_name_label.pack()

        system_info_label = tk.Label(system_info_window, text=f"System: {os_info.node}", font=("Helvetica", 12))
        system_info_label.pack()

        system_manufacturer_label = tk.Label(system_info_window,
                                             text=f"System Manufacturer: {platform.system()} {platform.machine()}",
                                             font=("Helvetica", 12))
        system_manufacturer_label.pack()

        processor_info_label = tk.Label(system_info_window, text=f"Processor: {platform.processor()}",
                                        font=("Helvetica", 12))
        processor_info_label.pack()

        bios_info_label = tk.Label(system_info_window, text=f"BIOS Version/Date: {platform.platform()}",
                                   font=("Helvetica", 12))
        bios_info_label.pack()

        # Convert memory information to appropriate unit
        def convert_bytes(bytes, unit="GB"):
            # Function to convert bytes to MB or GB based on the unit parameter
            if unit == "MB":
                return round(bytes / (1024 ** 2), 2), "MB"
            elif unit == "GB":
                return round(bytes / (1024 ** 3), 2), "GB"
            else:
                return bytes, ""

        memory_info = psutil.virtual_memory()
        total_memory, total_memory_unit = convert_bytes(memory_info.total)
        total_memory_label = tk.Label(system_info_window,
                                      text=f"Installed Physical Memory (RAM): {total_memory} {total_memory_unit}",
                                      font=("Helvetica", 12))
        total_memory_label.pack()

        available_memory, available_memory_unit = convert_bytes(memory_info.available)
        available_memory_label = tk.Label(system_info_window,
                                          text=f"Available Physical Memory: {available_memory} {available_memory_unit}",
                                          font=("Helvetica", 12))
        available_memory_label.pack()

        virtual_memory_info = psutil.swap_memory()
        total_virtual_memory, total_virtual_memory_unit = convert_bytes(virtual_memory_info.total)
        total_virtual_memory_label = tk.Label(system_info_window,
                                              text=f"Total Virtual Memory: {total_virtual_memory} {total_virtual_memory_unit}",
                                              font=("Helvetica", 12))
        total_virtual_memory_label.pack()

        available_virtual_memory, available_virtual_memory_unit = convert_bytes(virtual_memory_info.free)
        available_virtual_memory_label = tk.Label(system_info_window,
                                                  text=f"Available Virtual Memory: {available_virtual_memory} {available_virtual_memory_unit}",
                                                  font=("Helvetica", 12))
        available_virtual_memory_label.pack()

    def show_system_updates_info(self):
        updates_window = tk.Toplevel(self)
        updates_window.title("System Updates Information")
        updates_window.geometry("800x600")

        # Fetch and display system updates information
        updates_info_label = tk.Label(updates_window, text="System Updates Information", font=("Helvetica", 16, "bold"))
        updates_info_label.pack(pady=10)

        # Execute wuauclt.exe command to get update information
        command = "wuauclt /detectnow /updatenow"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check if the command was successful
        if result.returncode == 0:
            updates_data = [["Update Name", "Status"]]  # Initialize with headers
            # You can add logic here to parse the output of wuauclt.exe and extract update information
            # For demonstration purposes, I'll just display placeholder data
            updates_data.append(["Security Update", "Pending"])
            updates_data.append(["Feature Update", "Installed"])

            # Format update information into a table using tabulate
            table = tabulate(updates_data, headers="firstrow", tablefmt="grid")

            # Display table in a label
            updates_table_label = tk.Label(updates_window, text=table, font=("Courier", 12))
            updates_table_label.pack()
        else:
            # If the command failed, display an error message
            error_label = tk.Label(updates_window, text="Error: Failed to retrieve system updates",
                                   font=("Helvetica", 12), fg="red")
            error_label.pack()

    def convert_bytes_to_gb(self, bytes):
        gb = bytes / (1024 ** 3)
        return gb
    def show_disk_usage_info(self):
        disk_partitions = psutil.disk_partitions()
        partitions = []
        total_usage = []
        used_usage = []
        free_usage = []

        for partition in disk_partitions:
            partitions.append(partition.mountpoint)
            disk_usage = psutil.disk_usage(partition.mountpoint)
            total_usage.append(self.convert_bytes_to_gb(disk_usage.total))
            used_usage.append(self.convert_bytes_to_gb(disk_usage.used))
            free_usage.append(self.convert_bytes_to_gb(disk_usage.free))

        # Plotting
        x = np.arange(len(partitions))
        width = 0.2

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width, total_usage, width, label='Total')
        rects2 = ax.bar(x, used_usage, width, label='Used')
        rects3 = ax.bar(x + width, free_usage, width, label='Free')

        ax.set_xlabel('Partition')
        ax.set_ylabel('Usage (GB)')
        ax.set_title('Disk Usage Information')
        ax.set_xticks(x)
        ax.set_xticklabels(partitions)
        ax.legend()

        # Displaying the bar chart
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def convert_bytes3(self, bytes):
        # Function to convert bytes to GB
        return round(bytes / (1024 ** 3), 2)

    def show_security_info(self):
        security_window = tk.Toplevel(self)
        security_window.title("Security Information")
        security_window.geometry("400x300")

        # Fetch and display security-related information
        security_info_label = tk.Label(security_window, text="Security Information", font=("Helvetica", 16, "bold"))
        security_info_label.pack(pady=10)

        # Fetch antivirus status using Windows Security Center (wmic command)
        antivirus_label = tk.Label(security_window, text=self.get_antivirus_status(), font=("Helvetica", 12))
        antivirus_label.pack()

        # Fetch firewall status using Windows Firewall command
        firewall_label = tk.Label(security_window, text=self.get_firewall_status(), font=("Helvetica", 12))
        firewall_label.pack()

        # Fetch open ports using netstat command
        open_ports_label = tk.Label(security_window, text=self.get_open_ports(), font=("Helvetica", 12))
        open_ports_label.pack()

    def get_antivirus_status(self):
        try:
            result = subprocess.run(
                "wmic /namespace:\\\\root\\SecurityCenter2 path AntiVirusProduct get displayName /format:value",
                capture_output=True, text=True, shell=True)
            antivirus_info = result.stdout.strip()
            return "Antivirus Status: " + antivirus_info.split('=')[1]
        except Exception as e:
            return "Failed to retrieve antivirus status."

    def get_firewall_status(self):
        try:
            result = subprocess.run("netsh advfirewall show allprofiles state", capture_output=True, text=True,
                                    shell=True)
            firewall_info = result.stdout.strip()
            return "Firewall Status: " + firewall_info
        except Exception as e:
            return "Failed to retrieve firewall status."




if __name__ == "__main__":
    app = SystemMonitor()
    app.mainloop()
