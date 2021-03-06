# coding=utf-8
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager

__author__ = 'calthorpe_associates'

from footprint.main.mixins.name import Name
from django.db import models
from footprint.main.models.keys.keys import Keys

class BuildingUseDefinition(Name):
    """
        BuildingUseDefinition describes the possible general types of uses for a building
    """
    objects = GeoInheritanceManager()

    category = models.ForeignKey('BuildingUseDefinition', null=True)

    class Meta(object):
        app_label = 'main'

    def get_attributes(self):
        return self.averaged_attributes() + self.summed_attributes()

    def averaged_attributes(self):
        return ['efficiency', 'square_feet_per_unit', 'vacancy_rate', 'floor_area_ratio'] + \
            (['household_size'] if self.name in Keys.ALL_RESIDENTIAL_USES else [])

    def summed_attributes(self):
        return ['unit_density', 'net_built_up_area', 'gross_built_up_area']

    def clean(self):
        use_category_dict = Keys.BUILDING_USE_DEFINITION_CATEGORIES
        category = BuildingUseDefinition.objects.get(Name=use_category_dict[self.name]) or None
        self.category = category or 'Unknown'
