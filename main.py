import math
from typing import Dict, Any

from Observations import Observations
from random import randint

how_many_observation_by_tag = {}

if __name__ == '__main__':

    x1 = Observations(var_1=4, var_2=2, cluster_tag="")
    x2 = Observations(var_1=6, var_2=4, cluster_tag="")
    x3 = Observations(var_1=5, var_2=1, cluster_tag="")
    x4 = Observations(var_1=10, var_2=6, cluster_tag="")
    x5 = Observations(var_1=11, var_2=8, cluster_tag="")
    x6 = Observations(var_1=25, var_2=31, cluster_tag="")
    x7 = Observations(var_1=22, var_2=13, cluster_tag="")

    objects = (x1, x2, x3, x4, x5, x6, x7)

    e_array = []
    means_dict = {}
    k = 3
    tags = [f"c{i + 1}" for i in range(k)]  # generates tags how much tags require [c1,c2,c3 ...]
    is_there_any_of_tags_changed = False
    iteration_count = 0


    def count_how_many_observation_by_tag(obj):
        global how_many_observation_by_tag

        how_many_observation_by_tag = {key: 0 for key in tags}  # for ex c1 : 3 c2 : 2 ...
        for i in obj:
            how_many_observation_by_tag[i.cluster_tag] += 1


    def add_tags_to_object(obj):
        for i in obj:
            i.cluster_tag = f"c{randint(1, k)}"

        count_how_many_observation_by_tag(objects)

        for value in how_many_observation_by_tag.values():
            if value <= 1:
                add_tags_to_object(objects)


    def calculate_means(obj):

        count_how_many_observation_by_tag(objects)

        global means_dict
        cluster_means = {f"m{i + 1}": 0 for i in range(k)}  # 2 is attribute count

        for i in range(k):
            var1 = 0
            var2 = 0
            for each_obj in obj:
                if each_obj.cluster_tag == f"c{i + 1}":
                    var1 += each_obj.var_1
                    var2 += each_obj.var_2
            cluster_means[f"m{i + 1}"] = [var1 / how_many_observation_by_tag[f"c{i + 1}"],
                                          var2 / how_many_observation_by_tag[f"c{i + 1}"]]

        for key, value in cluster_means.items():
            cluster_means[key] = [value[0].__round__(2), value[1].__round__(2)]
        means_dict = cluster_means


    def calculate_e(obj):

        errors_for_each_cluster = []
        for i in range(k):
            e = 0
            for each_obj in obj:
                if each_obj.cluster_tag == f"c{i + 1}":
                    e += (pow(each_obj.var_1 - means_dict[f"m{i + 1}"][0], 2) +
                          pow(each_obj.var_2 - means_dict[f"m{i + 1}"][1], 2))
            errors_for_each_cluster.append(e.__round__(2))

        return sum(errors_for_each_cluster)


    def redeploy_tag(obj):
        global is_there_any_of_tags_changed
        is_there_any_of_tags_changed = False

        distance_dict = {f"m{key + 1}": [] for key in range(k)}

        for i in range(k):
            for each_object in obj:
                distance = math.sqrt(pow(means_dict[f"m{i + 1}"][0] - each_object.var_1, 2) +
                                     pow(means_dict[f"m{i + 1}"][1] - each_object.var_2, 2))
                distance_dict[f"m{i + 1}"].append(distance.__round__(2))

        # distance_dict is a structure like this {'m1': [d(m1,x1),d(m2,x2)...,'m2':[d(m2,x1),d(m2,x2)...,'m3': ...]

        #  for each object
        for i in range(Observations.instance_count):
            find_min_dict_for_each_object = {f"m{key + 1}": 0 for key in range(k)}  # m1 : 3.34 m2 : 4.72 ...
            # adds all distances belong to each object x1 -> 3.33 , 4.72 , ... x2 -> 0.67 , 2.06 , ...
            for means in range(k):
                find_min_dict_for_each_object[f"m{means + 1}"] = distance_dict[f"m{means + 1}"][i]
            #  after second loop finish we have a structure like {'m1': 3.34, 'm2': 4.72}
            #  now we need to find which m is lower but min(find_min_dict_for_each_object) is not worked correct
            #  : so I made my own min founder
            temp = [x for x in find_min_dict_for_each_object.values()]
            for key, value in find_min_dict_for_each_object.items():
                before = objects[i].cluster_tag
                if value == min(temp):
                    #  tags changing in here
                    objects[i].cluster_tag = f"c{key[1:]}"
                after = objects[i].cluster_tag

                if before != after:
                    is_there_any_of_tags_changed = True

        count_how_many_observation_by_tag(objects)


    def k_means():
        global iteration_count

        calculate_means(objects)  # Means calculated and stored in means_dict
        e_array.append(calculate_e(objects))  # e calculated and stored in e_array
        redeploy_tag(objects)  # Tags redeploy
        iteration_count += 1


    try:
        add_tags_to_object(objects)  # Tags randomly attached to the objects
        k_means()
        while is_there_any_of_tags_changed:
            k_means()
    except Exception as e:
        print(e)
        print("Try to change cluster amount")

    print(e_array)
    for i in objects:
        i.see_object()
