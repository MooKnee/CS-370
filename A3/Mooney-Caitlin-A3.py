import sys, getopt, os, random, itertools
from os import path


class Data_Point:

    def __init__(self, features, classifier):
        self.features = features
        self.featureCount = len(features.attributes)
        self.classifier = classifier


class Vector():
    def __init__(self, list):
        self.attributes = list
    def __init__(self):
        self.attributes = []

    def vector_subtraction(self, vector):
        if len(self.attributes) != len(vector.attributes):
            return 0

        newVector = Vector()
        for i in range(len(self.attributes)):
            newVector.attributes.append(self.attributes[i] - vector.attributes[i])

        return newVector

    def vector_addition(self, vector):
        if len(self.attributes) != len(vector.attributes):
            return 0

        newVector = Vector()
        for i in range(len(self.attributes)):
            newVector.attributes.append(self.attributes[i] + vector.attributes[i])

        return newVector

    def vector_scalar(self, scalar):
        newVector = Vector()
        for attribute in self.attributes:
            newVector.attributes.append(attribute * scalar)

        return newVector

def distSquared(features_point_x, features_point_y):
    if len(features_point_x.attributes) != len(features_point_y.attributes):
        return 0
    # diffs = vectorsubtraction(point, point_y)
    distance_total = 0
    # for diff in diffs:
    #for diff in Vector.vector_subtraction(self.point_x, self.point_y):
    for diff in features_point_x.vector_subtraction(features_point_y).attributes:
        distance_total += pow(diff, 2)
    average_distance = distance_total
    return average_distance



def classification_phase(point, averages_e):
    r_G__Y__ = -1
    closestExemplar = ""
    for closestE in averages_e:
        average = averages_e[closestE]
        point_distance = distSquared(point.features, average)
        if r_G__Y__ == -1 or r_G__Y__ > point_distance:
            r_G__Y__ = point_distance
            closestExemplar = closestE
    return closestExemplar

def close_centroid_set(points, averages):
    preds = []
    for point in points:
        prediction = classification_phase(point, averages)
        preds.append(prediction)
    return preds


def init_centeroid_exemplars(t_v_set):
    centeroid_avgs = {}
    centeroid_avgs_sum = {}
    for point in t_v_set:
        if point.classifier not in centeroid_avgs:
            centeroid_avgs[point.classifier] = []
            centeroid_avgs_sum[point.classifier] = 0
            for count in range(point.featureCount):
                centeroid_avgs[point.classifier].append(0.0)
        for count in range(point.featureCount):
            centeroid_avgs[point.classifier][count] += point.features.attributes[count]
        centeroid_avgs_sum[point.classifier] += 1
    exemplar_avgs = {}
    for key in centeroid_avgs:
        exemplar_avgs[key] = Vector()
        for total in centeroid_avgs[key]:
            exemplar_avgs[key].attributes.append(total / centeroid_avgs_sum[key])

    return exemplar_avgs

def init_random_exemplars(points, numOfClassifAttri):
    e_vectors = {}
    for point in points:
        if point.classifier not in e_vectors:
            e_vectors[point.classifier] = Vector()
    for i in range(numOfClassifAttri):
        min_constraint = None
        max_constraint = None
        for point in points:
            if min_constraint == None or min_constraint > point.features.attributes[i]:
                min_constraint = point.features.attributes[i]
            if max_constraint == None or max_constraint < point.features.attributes[i]:
                max_constraint = point.features.attributes[i]
        for key in e_vectors:
            e_vectors[key].attributes.append(random.uniform(min_constraint, max_constraint))
    return e_vectors


def computeAccuracy(training_set_pts, u_X_Vect):
    nearby = 0
    sum_a = 0
    for (pt_T, u_x) in zip(training_set_pts, u_X_Vect):
        sum_a += 1
        if pt_T.classifier == u_x:
            nearby += 1
    accuracy = float(nearby * 100) / float(sum_a)
    return accuracy


def gradDescent(training_set_T_points, numOfClassifAttri, exemplar_v_c, stepSize, epsilon, M, verbose_opt):
    previousCost = 10000000000
    PrevCost = 10000000000
    # u(X) = vector of predictive attributes
    PrevAccuracy = computeAccuracy(training_set_T_points, close_centroid_set(training_set_T_points, exemplar_v_c))

    iteration = 0
    # initialize vectors to the centroid of their respective categories
    while True:
        exemplar_n = {}
        for key in exemplar_v_c:
            # n is a vector
            exemplar_n[key] = Vector()
            for count in range(numOfClassifAttri):
                exemplar_n[key].attributes.append(0.0)

        TotalCost = 0
        # for each datapoint Y in T
        for datapoint in training_set_T_points:
            # v = Y.c
            guess = classification_phase(datapoint, exemplar_v_c)
            #find g_w closest to u(Y)
            if datapoint.classifier != guess:
                # if d^2[g_v, u(Y)] - d^2[r_G_(Y), u(Y)] is zero, then G correctly classifies Y
                # else, then error cost with Y for classifying G
                # Cost_G_(Y) = min(M, d^2[g_v, u(Y)] - d^2[r_G_(Y), u(Y)])
                # u(Y) = vector of predictive attributes of Y
                u_Y = datapoint.features
                # d^2[g_v, u(Y)]
                # distSquared(g_v, u(Y))
                # g_v =
                g_v = exemplar_v_c[datapoint.classifier]

                # d^2[r_G_(Y), u(Y)]
                # distSquared(u(Y), g_w)
                # d^2(r_G_(Y), u(Y))
                # r_G_(Y) = closest exemplar vector to Y
                # r_G_Y = g_w
                g_w = exemplar_v_c[guess]

                # Cost = distSquared(g_v, u(Y)) - distSquared(u(Y), g_w)
                #Cost = distSquared(g_v, u_Y) - distSquared(u_Y, g_w)
                Cost = distSquared(g_v, u_Y) - distSquared(u_Y, g_w)
                if Cost < M:
                    # n_v += u(Y) - g_v
                    # u(Y) - g_v
                    # n_v +=
                    # n_w += g_w - u(Y)
                    # g_w - u(Y)
                    # n_w +=

                    corr_classi = u_Y.vector_subtraction(g_v)
                    exemplar_n[datapoint.classifier] = exemplar_n[datapoint.classifier].vector_addition(corr_classi)

                    w_classi = g_w.vector_subtraction(u_Y)
                    exemplar_n[guess] = exemplar_n[guess].vector_addition(w_classi)

                    TotalCost += Cost
                else:
                    TotalCost += M
        if verbose_opt:
            for doot in exemplar_v_c:
                print(doot + ": " + str(exemplar_v_c[doot].attributes))
            print("Accuracy: " + str(PrevAccuracy))

        # if TotalCost < epsilon
        if TotalCost < epsilon:
            # training complete
            return exemplar_v_c, PrevAccuracy
        # if TotalCost > (1 - epsilon) * previousCost
        if TotalCost > (1 - epsilon) * PrevCost:
            # improvement too small
            return exemplar_v_c, PrevAccuracy
        # for v = 1 to c
        exemplar_h_v = {}
        for key in exemplar_v_c:
            # h_v = g_v + step_size * n_v
            # h_v =
            exemplar = exemplar_v_c[key]
            # step_size * n_v
            step_size_times_n_v = exemplar_n[key].vector_scalar(stepSize)
            g_v_plus_step_size_times_n_v = exemplar.vector_addition(step_size_times_n_v)
            h_v = g_v_plus_step_size_times_n_v
            exemplar_h_v[key] = h_v
        NewAccuracy = computeAccuracy(training_set_T_points, close_centroid_set(training_set_T_points, exemplar_h_v))
        if NewAccuracy < PrevAccuracy:
            return exemplar_v_c, PrevAccuracy
        for key in exemplar_v_c:
            exemplar_v_c[key] = exemplar_h_v[key]
        PrevCost = TotalCost
        PrevAccuracy = NewAccuracy
        iteration += 1

def main(trainingSetFile, stepSize, epsilon, M, random_restarts, verbose_opt):
    # Get training points
    f = open(trainingSetFile, "r")  # Input file
    t_v = []
    numOfClassifAttri = 0
    for line in f.readlines():
        parts = line.split(",")
        # point, numOfClassifAttri = getAttributes(parts, numOfClassifAttri)
        features = Vector()
        numOfClassifAttri = len(parts) - 1
        for i in range(numOfClassifAttri):
            features.attributes.append(float(parts[i].replace("\n", "")))

        point = Data_Point(features, parts[numOfClassifAttri].replace("\n", ""))
        t_v.append(point)

        # t_v.append(point)

    averages = init_centeroid_exemplars(t_v)
    closest_exemplar = None
    closest_accuracy = 0
    for i in range(random_restarts):
        if verbose_opt:
            print("Iterator: " + str(i))

        exemplar_v_c, accuracy = gradDescent(t_v, numOfClassifAttri, averages, stepSize, epsilon, M, verbose_opt)

        if accuracy > closest_accuracy:
            closest_exemplar = exemplar_v_c
            closest_accuracy = accuracy

        averages = init_random_exemplars(t_v, numOfClassifAttri)

    print("Closest Exemplar Values: ")
    for key in closest_exemplar:
        print(key + ": " + str(closest_exemplar[key].attributes))
    print("Closest Acccuracy Values: " + str(closest_accuracy))

# name of file for training set
trainingSetFile = str(sys.argv[1])
# double stepSize
stepSize = float(sys.argv[2])
# double epsilon
epsilon = float(sys.argv[3])
# double M
M = float(sys.argv[4])
# number of random restarts
random_restarts = int(sys.argv[5])
if len(sys.argv) > 6:
    # optionally -v
    verboseChoice = str(sys.argv[6])
    # if verboseChoice == "-v":
    verbose_opt = True
else:
    verbose_opt = False

main(trainingSetFile, stepSize, epsilon, M, random_restarts, verbose_opt)