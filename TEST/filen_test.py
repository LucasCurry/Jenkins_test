import matplotlib.pyplot as plt

def plot(frequencies):
    time_points = list(range(1, len(frequencies) + 1))
    plt.plot(time_points, frequencies, marker='o', linestyle='-', color='b')
    plt.title('Vågform')
    plt.xlabel('Tid')
    plt.ylabel('Amplitud')
    plt.savefig('resultat.png')

def read_data(file_name):
    file = open(file_name, mode = 'r', encoding = 'UTF-8')
    data = file.read()
    data_2 = data.split(',')
    data_2.pop()
    file.close()
    for i in range(len(data_2)):
        data_float.append(float(data_2[i]))
    return data_float

data = []
data_float = []
data_2=[]

# läser data från en fil som ges som argument
read_data('automation_first_matvarden.csv')
# gör en plot av lista som ges som argument
plot(data_float)
