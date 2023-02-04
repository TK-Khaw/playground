#!/usr/bin/python3
import argparse
import json
import math
import functools
import matplotlib.pyplot as plt

SPHERE_RADIUS = 10000.0
MAX_BRIGHT = 5
BRIGHT_SCALE = 100

def parse_angle(angle_in_deg):
    """ 
    Parse angle from degree-minute representation to 
    radian representation.
    """
    l = angle_in_deg.split(':')
    return (
        float(l[0] or 0) + 
        float(l[1] or 0)/60 + 
        float(l[1] or 0)/3600
    ) * math.pi / 180

def normalize(vec):
    """
    normalize vector.
    """
    length = math.sqrt(functools.reduce(lambda a,b : a + b*b , vec))
    return [
        x/length for x in vec
    ]

def dot(vec1, vec2):
    """
    dot product.
    """
    return vec1[0] * vec2[0] + \
        vec1[1] * vec2[1] + \
        vec1[2] * vec2[2]

def cross(vec1, vec2):
    """
    cross product.
    """
    return [
        vec1[1] * vec2[2] - vec1[2]*vec2[1],
        vec2[0] * vec1[2] - vec2[2]*vec1[0],
        vec1[0] * vec2[1] - vec1[1]*vec2[0],
    ]

class Star:
    """ Star class
    This class represents a star.
    """
    def __init__(self, name, azimuth, altitude, magnitude):
        self._name = name
        self._azimuth = parse_angle(azimuth)
        self._altitude = parse_angle(altitude)
        self._magnitude = magnitude

    @property
    def coordinate(self):
        """
        returns Cartesian coordinate of the star. 3d vector.
        """
        if hasattr(self, '_cart_coord'):
            return self._cart_coord

        self._cart_coord = [
            SPHERE_RADIUS * math.cos(self._altitude) * math.cos(self._azimuth),
            SPHERE_RADIUS * math.cos(self._altitude) * math.sin(self._azimuth),
            SPHERE_RADIUS * math.sin(self._altitude)
        ]

        return self._cart_coord

    def inplane_vector(self, normal):
        """
        returns in-plane 3d vector wrt normal passed in.
        """
        # Out of plane.
        oop_vec_length = dot(normal, self.coordinate)
        return [ 
            self.coordinate[i] - normal[i] * oop_vec_length for i in range(3) 
        ]

    def inplane_coordinate(self, normal, bases):
        """
        returns in-plane coordinate wrt normal and the unit bases passed in. 2d vector.
        """
        ip_vec = self.inplane_vector(normal)

        return [ dot(b,ip_vec) for b in bases ]

class View:
    """ View class
    View plane that contains all the stars.
    """
    def __init__(self, stars = None):
        if stars:
            self._stars = list()
            for star in stars:
                self._stars.append(Star(**star))

    @property
    def normal(self):
        """
        Normal vector of the plane in Cartesian coordinate.
        Implemented as the vector from center of sphere to the center of mass of the star group,
        assuming equal weight.
        TODO: implement flush.
        """
        if hasattr(self, '_normal'):
            return self._normal
        
        num_of_stars = len(self._stars)
        self._normal = normalize([
            functools.reduce(
                lambda a,b : a + b.coordinate[i], self._stars, 0
            ) / num_of_stars for i in range(3)
        ])
        
        return self._normal

    @property
    def bases(self):
        """
        returns unit bases for the view.
        takes the inplane vector of the first star and the cross product
        of it with normal of the plane.
        """
        if hasattr(self, '_bases'):
            return self._bases
        b1 = normalize(self._stars[0].inplane_vector(self.normal))
        self._bases = [
            b1,
            cross(b1, self.normal),
        ]
        return self._bases

    def save(self, out_filename):
        """
        Generate the plot of stars in this view and print to `out_filename`.
        """
        fig, ax = plt.subplots()

        xs = list()
        ys = list()
        s = list()
        n = list()
        for star in self._stars:
            x, y = star.inplane_coordinate(self.normal, self.bases)
            xs.append(x)
            ys.append(y)
            s.append(BRIGHT_SCALE*(MAX_BRIGHT - star._magnitude))
            n.append(star._name)

        ax.scatter(x=xs, y=ys, s = s)
        for i, name in enumerate(n):
            ax.annotate(name, (xs[i], ys[i]))

        fig.savefig(out_filename)


def main():
    parser = argparse.ArgumentParser(description='Plot the night sky with mathematics! ;)')
    parser.add_argument('star_file', type=str, help='JSON file containing stars to plot')

    args = parser.parse_args()

    with open(args.star_file, 'r') as f:
        sky = json.load(f)

    view = View(stars = sky['stars'])
    view.save('outfile.png')
    
if __name__ == '__main__':
    main()
