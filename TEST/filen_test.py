import matplotlib.pyplot as plt

def plot(amplitudes):
    time_points = list(range(1, len(amplitudes) + 1))
    plt.plot(time_points, amplitudes, marker='o', linestyle='-', color='b')
    plt.title(f'Vågform, frekvens: {str(freq)}')
    plt.xlabel('Tid')
    plt.ylabel('Amplitud')
    plt.savefig('resultat.png')

def read_data(file_name_1, file_name_2):
    global freq
    file = open(file_name_1, mode = 'r', encoding = 'UTF-8')
    data = file.read()
    data_2 = data.split(',')
    data_2.pop()
    file.close()
    x_files = open(file_name_2, mode = 'r', encoding = 'UTF-8')
    freq = x_files.read()
    print(str(freq))
    for i in range(len(data_2)):
        data_float.append(float(data_2[i]))
    return data_float

freq = 0
data = []
data_float = []
data_2=[]

# läser data från en fil som ges som argument
read_data('amplituder.csv', 'frekvens.csv')
# gör en plot av lista som ges som argument
plot(data_float)
