import pickle

filename = r'C:\Users\Peter\PycharmProjects\NYHackathon\input.dat'


def save(inputs: list):
    # save the list into the file
    my_file = open(filename, "wb")
    pickle.dump(inputs, my_file)
    my_file.close()


def get() -> list:
    my_file = open(filename, "rb")
    try:
        inputs = pickle.load(my_file)
    except EOFError:
        inputs = []
    my_file.close()
    return inputs
