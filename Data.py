def get_data(train=525):
    f = open('cancer2.dt', 'r')
    train_data = []
    for i in range(train):
        temp_list = []
        line = f.readline()
        line = line.replace('\n', '')
        line = line.split(' ')
        for element in line:
            temp_list.append(float(element))
        train_data.append(temp_list)
    return train_data
