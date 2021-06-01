def get_data(train=350, test=175):
    f = open('cancer2.dt', 'r')
    train_data = []
    test_data = []
    for i in range(train):
        temp_list = []
        line = f.readline()
        line = line.replace('\n', '')
        line = line.split(' ')
        for element in line:
            temp_list.append(float(element))
        train_data.append(temp_list)
    for i in range(test):
        temp_list = []
        line = f.readline()
        line = line.replace('\n', '')
        line = line.split(' ')
        for element in line:
            temp_list.append(float(element))
        test_data.append(temp_list)

    return train_data, test_data