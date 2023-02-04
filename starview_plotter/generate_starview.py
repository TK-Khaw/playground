#!/usr/bin/python3
import argparse
import json
import math
import functools
import matplotlib.pyplot as plt

SPHERE_RADIUS = 1.0
MAX_BRIGHT = 5
BRIGHT_SCALE = 50

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

    def inplane_vector(self, normal, mode):
        """
        returns in-plane 3d vector wrt normal passed in.
        """
        return {
            'ortho' : self.inplane_ortho_vector,
            'stereo' : self.inplane_stereo_vector,
        }.get(mode, self.inplane_ortho_vector)(normal)

    def inplane_coordinate(self, normal, bases, mode):
        """
        returns in-plane coordinate wrt normal and the unit bases passed in. 2d vector.
        """
        ip_vec = self.inplane_vector(normal, mode)

        return [ dot(b,ip_vec) for b in bases ]

    def inplane_ortho_vector(self, normal):
        # Out of plane.
        oop_vec_length = dot(normal, self.coordinate)
        return [ 
            self.coordinate[i] - normal[i] * oop_vec_length for i in range(3) 
        ]

    def inplane_stereo_vector(self, normal):
        # Centre of projection to coordinate on sphere.
        cop_to_coord = [ self.coordinate[i] + SPHERE_RADIUS*normal[i] for i in range(3) ]

        # Component along normal.
        cop_to_coord_normal_length = dot(normal, cop_to_coord)

        # cotangent ratio to get our component along plane to the right size.
        cot = SPHERE_RADIUS *2 / cop_to_coord_normal_length

        # Component along plane.
        return [ 
            (cop_to_coord[i] - normal[i] * cop_to_coord_normal_length)*cot  for i in range(3) 
        ]

class View:
    """ View class
    View plane that contains all the stars.
    """
    def __init__(self, stars = None, mode = 'ortho'):
        """
        mode is one of the values in { ortho, stereo, }
        """
        self._mode = mode
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
        b1 = normalize(self._stars[0].inplane_vector(self.normal, self._mode))
        self._bases = [
            b1,
            cross(self.normal, b1),
        ]
        return self._bases

    def save(self, out_filename):
        """
        Generate the plot of stars in this view and print to `out_filename`.
        """
        fig, ax = plt.subplots(
            figsize = [15,15],
            layout = 'tight'
        )

        xs = list()
        ys = list()
        s = list()
        n = list()
        for star in self._stars:
            x, y = star.inplane_coordinate(self.normal, self.bases, self._mode)
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

    view = View(
        stars = sky['stars'], 
        mode = 'stereo'
    )
    view.save('stereo_triangle_2.png')
    
if __name__ == '__main__':
    main()
