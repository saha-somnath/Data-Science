__author__ = 'somnath'

import os,sys
import math
from points import Point
import matplotlib.pyplot as plt


class KMeans:

    def __init__(self, points=[], centroids=[]):
        self.points      = points
        self.centroids   = centroids
        self.cluster     = [ [] for index in range(len(self.centroids))]
        self.points_type = 2



    def addPoint(self, P):
        if self.points:
            if len(P.getCoordinates()) == self.points_type:
                self.points.append(P)
            else:
                print("ERROR: Wrong type {} of points being added. Only add {} points".format(P.getType(), str(self.points_type) + "D"))
        else:
            self.points_type = len(P.getCoordinates())
            self.points.append(P)

    # Return all points
    def getPoints(self):
        return self.points

    def setCentroids(self,centroids=[]):
        self.centroids = centroids
        self.cluster = [ [] for index in range(len(self.centroids))]

    def getCentroids(self):
        return self.centroids

    def getEucledianDistance(self, P1, P2):

        distance = 0
        P1_coordinates = P1.getCoordinates()
        P2_coordinates = P2.getCoordinates()
        if len(P1_coordinates) == len(P2_coordinates):
            square_distance = 0
            for index in range(len(P1_coordinates)):
                if P1_coordinates[index] != P2_coordinates[index]:
                    square_distance += math.pow((P1_coordinates[index] - P2_coordinates[index]), 2)

            distance = math.sqrt(square_distance)
        else:
            print("ERROR: Wrong points")

        return distance


    def isCentroidChanged(self, cen_old, cen_new):
        coordinates_old = cen_old.getCoordinates()
        coordinates_new = cen_new.getCoordinates()
        for index in range(len(coordinates_new)):
            if coordinates_new[index] != coordinates_old[index]:
                return True
        return False



    def reassignCentroid(self):

        flag =  False
        if self.centroids:
            index = 0

            for cen in self.centroids:
                coordinates_sum = [0] * self.points_type
                for p in self.cluster[index]:
                    coordinates = p.getCoordinates()
                    for c_index in range(len(coordinates)):
                        coordinates_sum[c_index] += coordinates[c_index]


                for csum_index in range(len(coordinates_sum)):
                    coordinate = float(coordinates_sum[csum_index]) / len(self.cluster[index])
                    coordinates_sum[csum_index] =  round(coordinate,2)


                # update new centroid in the centroid list
                if self.isCentroidChanged(self.centroids[index], Point(coordinates_sum)):
                    self.centroids[index] = Point(coordinates_sum)
                    flag = True
                index += 1

        return flag

    def resetCluster(self):
        self.cluster     = [ [] for index in range(len(self.centroids))]
    # Create cluster
    def createCluster(self):

        for P in self.points:
            #cluster_points = [[]]
            min_eucledian_distance   = sys.maxint
            centroid_index  = 0
            for cen in self.centroids:
                #p_coordinates = P.getCoordinates()
                #cen_coordinates = cen.getCoordinates()
                e_distance = self.getEucledianDistance(P,cen)
                if min_eucledian_distance > e_distance:
                    min_eucledian_distance = e_distance
                    centroid_index = self.centroids.index(cen)

            self.cluster[centroid_index].append(P)



    def getCluster(self):
        return self.cluster

    def displayCluster(self):
        for cen in self.centroids:
            print("CENTROID: ({})".format(cen.display()))
            #cen.display()
            index = self.centroids.index(cen)
            for P in self.cluster[index]:
                print("\t\t Point:({})".format(P.display()))

    # Plotting points
    def plot(self):
        """
        Plot the points in 2D space
        color: 'b' = blue
               'r' = red
               'g' = green
               'y' = yellow
               'k' = black
               'm' = magenta
        :return: None
        """
        color = ['b','g','y','k','r']
        # Add points to the display

        axis_centroids =  [ [] for index in range(self.points_type)]

        for index in range(len(self.cluster)):
            axis_points = [ [] for idx in range(self.points_type)]
            for P in self.cluster[index]:
                coordinates = P.getCoordinates()
                for index in range(len(coordinates)):
                    axis_points[index].append(coordinates[index])

            plt.scatter(axis_points[0],axis_points[1], c=color[index])
            axis_points = []

        for P in self.centroids:
            coordinates = P.getCoordinates()
            for index in range(len(coordinates)):
                axis_centroids[index].append(coordinates[index])


        plt.scatter(axis_centroids[0],axis_centroids[1], c='r')

        plt.show()


def processPoints(input_lines):
    points = []
    index = 0
    for P in input_lines:
        P = P.strip()
        P =  [ round(float(pts.strip()),2) for pts in P.split()]
        points.append(Point(P))
        points[index].display()
        index += 1
    return points



def processInput(input_file):
    centroids = []
    points    = []
    try:
        with open(input_file, "r") as FH:
            lines     = FH.readlines()
            centroid_number = int(lines.pop(0))
            centroids = processPoints(lines[:centroid_number])
            points    = processPoints(lines[centroid_number:])
    except Exception as e:
        print("EXCEPTION:{}".format(e))

    print("Centroids:{}\n Points:{}".format(centroids,points))
    return ( points, centroids )



def main():
    points, centroids = processInput("Input.txt")
    KM = KMeans(points, centroids)

    #KM.setCentroids()
    KM.createCluster()
    KM.displayCluster()
    KM.plot()
    # K-Means algo
    index = 0
    while(KM.reassignCentroid()):
        print("Interation:{}".format(index))
        KM.resetCluster()
        KM.createCluster()
        index +=1
        KM.plot()
    print("K-Means Cluster: ... ")
    KM.displayCluster()
    KM.plot()



    centroids = KM.getCentroids()


if __name__ == "__main__":
    main()






