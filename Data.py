def add_data(train=350, test=175):
    f = open('cancer2.dt', 'r')
    train_data = []
    test_data = []
    for i in range(train):
        line = f.readline()
        line = line.replace('\n', '')
        train_data.append(line.split(' '))
    for i in range(test):
        line = f.readline()
        line = line.replace('\n', '')
        test_data.append(line.split(' '))

    return train_data, test_data
