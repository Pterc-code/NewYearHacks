import time
from gateway import get, save


# every input grabbed will be stored in this class
class Inputs:
    def __init__(self):
        self.inputs = get()  # tuples in list

    def add(self, new_input):
        localtime = time.asctime(time.localtime(time.time()))
        self.inputs.append((new_input, localtime))
        save(self.inputs)

    def edit(self, old_input, new_input):
        i = self.grab_index(old_input)
        localtime = time.asctime(time.localtime(time.time()))
        self.inputs[i] = (new_input, localtime)
        save(self.inputs)

    def delete(self, old_input):
        i = self.grab_index(old_input)
        # print(i)
        self.inputs.pop(i)
        save(self.inputs)

    # helper method
    def grab_index(self, given_input) -> int:
        for i in range(len(self.inputs)):
            # print(self.inputs[i][0])
            if self.inputs[i][0] == given_input:
                return i


if __name__ == "__main__":
    oi = Inputs()
    print(get())
    oi.add("halo")
    oi.add("bye")
    print(get())
    time.sleep(1)
    oi.edit("bye", "friend")
    print(get())
    oi.delete("halo")
    oi.delete('friend')
    print(get())
