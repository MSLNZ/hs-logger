import csv
import re

#open the file
file = open('G:\\Shared drives\\MSL - Humidity\\Commercial\Jobs\\2023-2024\\H96140247 Core TT loggers (615-622)\\data\\measurements.txt', 'r')
data = file.readlines()
meas = []
point = {"MAC": "", "UTC": "", "Temperature": "", "RH": "", "Light": "", "Pressure": ""}
points = []
for line in data:
    meas.append(line.strip())
match = False

for line in meas:
    # Start with "Connected to tag ".
    if line[0:17] == "Connected to tag ":
        # Extract mac address and ID.
        MAC = line[17:34]
        ID = line[38:]

    # Start with "Measurement set begins for ID ".
    elif line[0:30] == "Measurement set begins for ID ":
        # Check the IDs match. Only continue if they do.
        if line[30:] == ID:
            match = True
        else:
            match = False

    # Temperature, RH, Light, Pressure, and UTC
    elif line[0:3] == "UTC":
        point["UTC"] = line[4:]
    elif line[0:11] == "Temperature":
        point["Temperature"] = line[12:]
    elif line[0:2] == "RH":
        point["RH"] = line[3:]
    elif line[0:5] == "Light":
        point["Light"] = line[6:]
    elif line[0:8] == "Pressure":
        point["Pressure"] = line[9:]

    # Finish with "Measurement set ends"
    elif line[0:20] == "Measurement set ends":
        point["MAC"] = MAC
        match = False
        # Record the point.
        points.append(point)
        point = {"MAC": "", "UTC": "", "Temperature": "", "RH": "", "Light": "", "Pressure": ""}

    else:
        # Something we don't care about is happening here.
        pass

# Process data.
for point in points:
    i = 0
    temp = ""
    while point["UTC"][i] != "M":
        temp = temp + (point["UTC"][i])
        i = i + 1
    temp = temp + (point["UTC"][i])
    point["UTC"] = temp
    point["Temperature"] = re.sub("^[+-]?((\d+(\.\d+)?)|(\.\d+))$", "", point.get("Temperature"))
    point["RH"] = re.sub("^[+-]?((\d+(\.\d+)?)|(\.\d+))$", "", point.get("RH"))
    point["Light"] = re.sub("^[+-]?((\d+(\.\d+)?)|(\.\d+))$", "", point.get("Light"))
    point["Pressure"] = re.sub("^[+-]?((\d+(\.\d+)?)|(\.\d+))$", "", point.get("Pressure"))

# Print data to file.
titles = ["MAC", "time", "temperature", "rh", "light", "pressure"]
with open("G:\\Shared drives\\MSL - Humidity\\Commercial\Jobs\\2023-2024\\H96140247 Core TT loggers (615-622)\\data\\measurements.dat", "w+") as outfile:
    writer = csv.writer(outfile, titles, lineterminator='\n', delimiter='\t')
    writer.writerow(titles)
    for point in points:
        line = [point.get("MAC"), point.get("UTC"), point.get("Temperature"), point.get("RH"), point.get("Light"), point.get("Pressure")]
        writer.writerow(line)
