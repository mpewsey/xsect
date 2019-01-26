from __future__ import division
import numpy as np
from ..data import query_aisc
from .multi import multi_section_summary

__all__ = ['CrossSection']


class CrossSection():
    """
    A class representing a member cross section.

    Parameters
    ----------
    name : str
        The name of the cross section.
    width, height : float
        The width and height of the cross section in the x and y directions.
    area : float
        The cross sectional area.
    unit_weight : float
        The unit weight of the cross section.
    inertia_x, inertia_y : float
        The moment of inertias about the x and y axes.
    inertia_z : float
        The moment of inertia about the weak principal axis.
    inertia_j : float
        The polar moment of inertia.
    inertia_t : float
        The torsional moment of inertia.
    gyradius_x, gyradius_y : float
        The radius of gyration about the x and y axes.
    gyradius_z : float
        The radius of gyration about the weak principal axis.
    elast_sect_mod_x, elast_sect_mod_y : float
        The elastic section modulus about the x and y axes.
    elast_sect_mod_z : float
        The elastic section modulus about the weak principal axis.
    plast_sect_mod_x, plast_sect_mod_y : float
        The plastic section modulus about the x and y axes.
    is_round : bool
        If True, the member represents a round cross section, such as a round
        or pipe.
    kwargs
        Additional keyword arguments for secondary section properties that
        will be stored in the object's meta dictionary property.

    Examples
    --------
    The dictionaries returned by the various section summary functions
    included in this package may be passed to the initializer using the
    dictionary unwrapper as shown below. This can assist in the more rapid
    creation of cross section objects.

    >>> from xsect import angle_summary
    >>> odict = angle_summary(8, 8, 1.125)
    >>> CrossSection('L8x8x1.125', **odict)
    CrossSection(name='L8x8x1.125', ...)
    """
    def __init__(self, name, area, width=0, height=0, unit_weight=None,
                 inertia_x=None, inertia_y=None, inertia_z=None,
                 inertia_j=None, inertia_t=None,
                 gyradius_x=None, gyradius_y=None, gyradius_z=None,
                 elast_sect_mod_x=None, elast_sect_mod_y=None, elast_sect_mod_z=None,
                 plast_sect_mod_x=None, plast_sect_mod_y=None,
                 is_round=False, **kwargs):
        self.name = name
        self.width = width
        self.height = height
        self.area = area
        self.unit_weight = unit_weight
        self.inertia_x = inertia_x
        self.inertia_y = inertia_y
        self.inertia_z = inertia_z
        self.inertia_j = inertia_j
        self.inertia_t = inertia_t
        self.gyradius_x = gyradius_x
        self.gyradius_y = gyradius_y
        self.gyradius_z = gyradius_z
        self.elast_sect_mod_x = elast_sect_mod_x
        self.elast_sect_mod_y = elast_sect_mod_y
        self.elast_sect_mod_z = elast_sect_mod_z
        self.plast_sect_mod_x = plast_sect_mod_x
        self.plast_sect_mod_y = plast_sect_mod_y
        self.is_round = is_round
        self.meta = dict(**kwargs)

    def __repr__(self):
        attrs = [
            'name', 'area', 'width', 'height', 'unit_weight',
            'inertia_x', 'inertia_y', 'inertia_z', 'inertia_j', 'inertia_t',
            'gyradius_x', 'gyradius_y', 'gyradius_z',
            'elast_sect_mod_x', 'elast_sect_mod_y', 'elast_sect_mod_z',
            'plast_sect_mod_x', 'plast_sect_mod_y', 'is_round', 'meta'
        ]

        s = ['{}={!r}'.format(k, getattr(self, k)) for k in attrs]
        return '{}({})'.format(type(self).__name__, ', '.join(s))

    @classmethod
    def from_points(cls, name, add, subtract=[], is_round=False,
                    include_meta=True, **kwargs):
        """
        Initializes a cross section from boundary points.

        Parameters
        ----------
        add : list
            A list of arrays of (x, y) coordinates for shapes composing the
            cross section.
        subtract : list
            A list of arrays of (x, y) coordinates for shapes subtracting
            from the cross section.
        is_round : bool
            If True, the member represents a round cross section, such as a
            round or pipe.
        include_meta : bool
            If True, secondary properties will be written to the object meta
            dictionary. Otherwise, no values will be written to the meta
            dictionary. This saves memory if data from the meta dictionary
            is not needed.

        Examples
        --------
        >>> from xsect import cruciform_points
        >>> add = cruciform_points(8, 8, 1.125)
        >>> CrossSection.from_points('4L8x8x1.125', add)
        CrossSection(name='4L8x8x1.125', ...)
        """
        odict = multi_section_summary(add, subtract)
        odict['name'] = name
        odict['is_round'] = is_round
        odict.update(kwargs)

        xsect = cls(**odict)

        if not include_meta:
            xsect.meta.clear()

        return xsect


    @classmethod
    def from_aisc(cls, name, metric=False, version=None, include_meta=True):
        """
        Initializes a cross section from the properties in the AISC database.

        Parameters
        ----------
        name : str
            The name of the member.
        metric : bool
            If True, searches for the name in the metric shape database.
            Otherwise, searches for the name in the imperial shape database.
        version : str
            The version of the shape database to query. If None, the latest
            version will be used.
        include_meta : bool
            If True, secondary properties in the database will be written
            to the object meta dictionary. Otherwise, no values will be written
            to the meta dictionary. This saves memory if data from the
            meta dictionary is not needed.

        Examples
        --------
        >>> CrossSection.from_aisc('L8x8x1-1/8')
        CrossSection(name='L8X8X1-1/8', area=16.8, unit_weight=56.9, ...)
        """
        odict = query_aisc(name, metric, version)
        odict['inertia_j'] = odict['inertia_x'] + odict['inertia_y']

        if odict['type'] == 'PIPE':
            odict['is_round'] = True

        xsect = cls(**odict)

        if not include_meta:
            xsect.meta.clear()

        return xsect
