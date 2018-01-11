def singleton(cls, param_list=None):
    instances = {}

    def get_instances():
        if cls not in instances:
            if param_list is None:
                instances[cls] = cls()
            else:
                instances[cls] = cls(*param_list)
        return instances[cls]

    return get_instances
