# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
 # GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com
import geojson
from footprint.main.lib.functions import unique, flat_map, map_to_dict
from footprint.main.models.database.information_schema import sync_geometry_columns, InformationSchema
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from django.contrib.gis.geos import GEOSGeometry
from jsonify.templatetags.jsonify import jsonify
from django.conf import settings
from footprint.main.publishing.data_import_publishing import create_and_populate_relations
from footprint.main.publishing.import_processor import ImportProcessor
from footprint.main.utils.dynamic_subclassing import create_tables_for_dynamic_classes

__author__ = 'calthorpe_associates'

class GeoJsonProcessor(ImportProcessor):

    def __init__(self, **kwargs):
        """
            Specify seed_data in kwargs to bypass looking up geojson at the db_entity.url
        """
        super(GeoJsonProcessor, self).init()
        self.seed_data = kwargs.get('seed_data', None)

    def importer(self, config_entity, db_entity):
        """
            Creates various GeojsonFeature classes by importing geojson and saving it to the database via a dynamic subclass of GeojsonFeature
        :schema: The optional schema to use for the dynamic subclass's meta db_table attribute, which will allow the class's table to be saved in the specified schema. Defaults to public
        :data: Optional python dict data to use instead of loading from the db_entity.url
        :return: a list of lists. Each list is a list of features of distinct subclass of GeoJsonFeature that is created dynamically. To persist these features, you must first create the subclass's table in the database using create_table_for_dynamic_class(). You should also register the table as a DbEntity.
        """
        if self.seed_data:
            data = geojson.loads(jsonify(self.seed_data), object_hook=geojson.GeoJSON.to_instance)
        else:
            fp = open(db_entity.url.replace('file://', ''))
            data = geojson.load(fp, object_hook=geojson.GeoJSON.to_instance)
        feature_class_creator = FeatureClassCreator(config_entity, db_entity)
        # find all unique properties
        feature_class_configuration = feature_class_creator.feature_class_configuration_from_geojson_introspection(data)
        feature_class_creator.update_db_entity(feature_class_configuration)
        feature_class = feature_class_creator.dynamic_model_class(base_only=True)
        # Create our base table. Normally this is done by the import, but we're just importing into memory
        create_tables_for_dynamic_classes(feature_class)
        # Now write each feature to our newly created table
        for feature in map(lambda feature: self.instantiate_sub_class(feature_class, feature), data.features):
            feature.save()
        # Create the rel table too
        rel_feature_class = feature_class_creator.dynamic_model_class()
        create_tables_for_dynamic_classes(rel_feature_class)
        if InformationSchema.objects.table_exists(db_entity.schema, db_entity.table):
            # Tell PostGIS about the new geometry column or the table
            sync_geometry_columns(db_entity.schema, db_entity.table)

        # Create association classes and tables and populate them with data
        create_and_populate_relations(config_entity, db_entity)

    def instantiate_sub_class(self, feature_class, feature):
        """
            Instantiates an instance of the dynamic subclass of GeoJsonFeature based on the given feature.
        :param feature: A feature parsed django-geojson. The feature is actually reserialized to json in order to construct a GEOSGeometry instance.
        :return: An instance of the GeoJsonFeature subclass, which contains the geometry, properties of the feature, and perhaps the crs
        """
        # TODO, crs should be read from the geojson when present.
        # This crs isn't actually picked up by the GEOSGeometry constructor
        srid = settings.SRID_PREFIX.format(settings.DEFAULT_SRID)
        crs = {
            "type": "name",
            "properties": {
                "name": srid
            }
        }
        # Ironically, we have to rejsonify the data so that GEOSGeometry can parse the feature as json
        json = jsonify({'type':feature.geometry.type, 'coordinates':feature.geometry.coordinates, 'crs':crs})
        geometry = GEOSGeometry(json)
        field_dict = map_to_dict(lambda field: [field.name, feature.properties[field.name]],
                                 filter(lambda field: feature.properties.get(field.name, None), feature_class._meta.fields))
        return feature_class(wkb_geometry=geometry, **field_dict)

