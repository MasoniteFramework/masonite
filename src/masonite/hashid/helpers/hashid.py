from hashids import Hashids


def hashid(*values, decode=False, min_length=7):
    hash_class = Hashids(min_length=min_length)
    if type(values[0]) == dict and decode:
        new_dict = {}
        for key, value in values[0].items():
            if hasattr(value, "value"):
                value = value.value

            if value and hash_class.decode(value):
                value = hash_class.decode(value)

            if type(value) == tuple:
                value = value[0]
            new_dict.update({key: value})
        return new_dict

    if not decode:
        if isinstance(values[0], dict):
            new_dic = {}
            for key, value in values[0].items():
                if hasattr(value, "value"):
                    value = value.value
                if str(value).isdigit():
                    new_dic.update({key: hash_class.encode(int(value))})
                else:
                    new_dic.update({key: value})
            return new_dic

        return hash_class.encode(*values)

    return Hashids().decode(*values)
