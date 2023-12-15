from itertools import count


class Observations:
    instance_count = 0

    def __init__(self, var_1, var_2, cluster_tag):
        self.var_1 = var_1
        self.var_2 = var_2
        self.cluster_tag = cluster_tag
        Observations.instance_count += 1

    def __str__(self):
        return str(self.var_1)

    def see_object(self):
        print(f"(x = {self.var_1}, y = {self.var_2}, tag = {self.cluster_tag})")
