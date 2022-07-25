from matplotlib import pyplot as plt


#name = input("NAME OF FILE : ")

f = open("original_data.txt")
data = f.readlines()
f.close()


f = open("simulation_data.txt")
data1 = f.readlines()
f.close()


points = []
for i in data:
    points.append(float(i.replace("\n", "")))
    
points1 = []
for i in data1:
    points1.append(float(i.replace("\n", "")))

print("Plotting data")

# plot data
plt.plot(points, 'r')
plt.plot(points1, 'b')
plt.show()
