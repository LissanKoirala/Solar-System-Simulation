from matplotlib import pyplot as plt


name = input("NAME OF FILE : ")

f = open(f"{name}.txt")
data = f.readlines()
f.close()

print("Plotting data")

# get rolling average of data and plot it
