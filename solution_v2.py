import numpy as np
import os
from matplotlib import pyplot as plt

def read_data(name):
    path = os.path.join("dataset", name)

    data_info = {}
    with open(path) as f:

        info = f.readline().split()
        data_info["b_len"] = int(info[0])
        data_info["l_len"] = int(info[1])
        data_info["d_len"] = int(info[2])

        scores = np.array([int(sc) for sc in f.readline().split()])

        lib_data = f.readlines()
        i = 0
        while len(lib_data) > 2 * i:

            lib = [int(c) for c in lib_data[2 * i].split()]
            order = [int(c) for c in lib_data[2 * i + 1].split()]

            sc = 0.0
            for o in order:
                sc += scores[o]

            data_info[i] = {
                "b": lib[0],
                "sign": lib[1],
                "scan_day": lib[2],
                "order": sorted([(o, scores[o]) for o in order], key=lambda x: -x[1],),
                "sc": sc
            }
            i += 1

    return data_info

def get_lib_list(data):

    sort_order = list(range(data["l_len"]))
    score_for_sort = [data[i]["sc"] / (data[i]["sign"] ** 1.2) for i in range(data["l_len"])]
    s = sorted(zip(sort_order, score_for_sort), key=lambda x: x[1], reverse=True)
    new_order = [idx for (idx, sc) in s]

    idx_books = {k: True for k in range(data["b_len"])}
    new_data = {}
    new_data["b_len"] = data["b_len"]
    new_data["l_len"] = data["l_len"]
    new_data["d_len"] = data["d_len"]

    for num, i in enumerate(new_order):

        ord = data[i]["order"]
        new_book_order = []
        new_sc = 0
        for (o, sc) in ord:
            if idx_books[o]:
                new_book_order.append((o, sc))
                idx_books[o] = False
                new_sc += sc
        if len(new_book_order) == 0:
            break

        new_data[i] = {
                "b": len(new_book_order),
                "sign": data[i]["sign"],
                "scan_day": data[i]["scan_day"],
                "order": new_book_order,
                "sc": new_sc
            }

    if len(new_order) == num + 1:
        new_data["l_len"] = data["l_len"]
        print(data["l_len"])
    else:
        new_data["l_len"] = num
        print(num)
        new_order = new_order[:num]

    return new_data, new_order

def get_lib_order(data, new_order):

    t = [data[i]["sc"] / data[i]["sign"] for i in new_order]
    s = sorted(zip(new_order, t), key=lambda x: -x[1])

    return np.array([idx for (idx, _) in s])

def get_out(data, name_out):
    (data, new_order) = data
    path = os.path.join("out", "{}.txt".format(name_out))

    # new_order = get_lib_order(data, new_order)

    with open(path, "w") as f:

        f.write("{}\n".format(data["l_len"]))

        for num, i in enumerate(new_order):

            ord = data[i]["order"]

            f.write("{} {}\n".format(i, data[i]["b"]))
            f.write(" ".join([str(c) for (c, _) in ord]))
            f.write("\n")


data_name = {
    "a": "a_example.txt",
    "b": "b_read_on.txt",
    "c": "c_incunabula.txt",
    "d": "d_tough_choices.txt",
    "e": "e_so_many_books.txt",
    "f": "f_libraries_of_the_world.txt"
}

if __name__ == '__main__':
    for k in data_name.keys():
        print(k)
        data = read_data(data_name[k])
        data = get_lib_list(data)
        get_out(data, k)
