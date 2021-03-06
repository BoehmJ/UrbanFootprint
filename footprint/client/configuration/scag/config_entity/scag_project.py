
from footprint.client.configuration.default.config_entity.default_project import DefaultProjectFixture
from footprint.main.lib.functions import merge

__author__ = 'calthorpe_associates'


class ScagProjectFixture(DefaultProjectFixture):

    def feature_class_lookup(self):
        """
            Adds mappings of custom Feature classes
        :return:
        """
        parent_fixture = self.parent_fixture
        feature_class_lookup = parent_fixture.feature_class_lookup()
        return merge(feature_class_lookup, {})

    def default_db_entities(self):
        """
            Project specific SCAG additional db_entities
        :param default_dict:
        :return:
        """
        return super(ScagProjectFixture, self).default_db_entities() + []
