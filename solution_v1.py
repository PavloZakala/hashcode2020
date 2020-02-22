import numpy as np
import os

def read_data(name):
    path = os.path.join("dataset", name)

    data_info = {}
    with open(path) as f:

        info = f.readline().split()
        data_info["b_len"] = int(info[0])
        data_info["l_len"] = int(info[1])
        data_info["d_len"] = int(info[2])

        scores = [int(sc) for sc in f.readline().split()]

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
                "sc":sc
            }

            i += 1

    return data_info

def get_out(data, name_out):
    path = os.path.join("out", "{}.txt".format(name_out))

    sort_order = list(range(data["l_len"]))
    # t = [data[i]["sc"] for i in range(data["l_len"])]
    # s = sorted(zip(sort_order, t), key=lambda x: -x[1])
    #
    # d = {}
    # for (idx, sc) in s:
    #     if sc in d:
    #         d[sc].append((idx, sc))
    #     else:
    #         d[sc] = [(idx, sc)]
    #
    # for k in d.keys():
    #     t = [data[idx]["b"] for (idx, sc) in d[k]]
    #     s = sorted(zip(d[k], t), key=lambda x: x[1])
    #     d[k] = [a for (a, b) in s]
    t = [data[i]["sc"] / data[i]["sign"] for i in range(data["l_len"])]
    s = sorted(zip(sort_order, t), key=lambda x: -x[1])
    new_order = [idx for (idx, sc) in s]
    # new_order = []
    # for k in d.keys():
    #     new_order = d[k] + new_order

    with open(path, "w") as f:

        idx_books = {k: True for k in range(data["b_len"])}

        for num, i in enumerate(new_order):

            ord = data[i]["order"]
            new_book_order = []
            for (o, _) in ord:
                if idx_books[o]:
                    new_book_order.append(o)
                    idx_books[o] = False
            if len(new_book_order) == 0:
                break

        if len(new_order) == num+1:
            f.write("{}\n".format(data["l_len"]))
            print(data["l_len"])
        else:
            f.write("{}\n".format(num))
            print(num)

        idx_books = {k: True for k in range(data["b_len"])}

        for num, i in enumerate(new_order):

            ord = data[i]["order"]
            new_book_order = []
            for (o, _) in ord:
                if idx_books[o]:
                    new_book_order.append(o)
                    idx_books[o] = False
            if len(new_book_order) == 0:
                break
            else:
                f.write("{} {}\n".format(i, len(new_book_order)))
                f.write(" ".join([str(c) for c in new_book_order]))
                f.write("\n")


data_name = {
    # # "a": "a_example.txt",
    # "b": "b_read_on.txt",
    # "c": "c_incunabula.txt",
    # "d": "d_tough_choices.txt",
    # "e": "e_so_many_books.txt",
    "f": "f_libraries_of_the_world.txt"
}

if __name__ == '__main__':
    for k in data_name.keys():
        print(k)
        data = read_data(data_name[k])
        get_out(data, k)