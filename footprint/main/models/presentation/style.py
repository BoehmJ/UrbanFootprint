# coding=utf-8
# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
#  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
from footprint.main.mixins.key import Key
from footprint.main.mixins.name import Name
from model_utils.managers import InheritanceManager
from django.db import models

__author__ = 'calthorpe_associates'


class Style(Key, Name):
    """
        Represents a style class that is applied a geographic table column (currently via PresentationMedium).
        Style inherits the properties of Medium. It might be better at some point to make Style a sibling of Medium
        instead.
    """

    objects = InheritanceManager()

    identifier = models.TextField()
    target = models.TextField()
    style_property = models.TextField()

    class Meta(object):
        app_label = 'main'