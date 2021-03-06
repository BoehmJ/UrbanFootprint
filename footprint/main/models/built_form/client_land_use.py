from model_utils.managers import InheritanceManager
from footprint.main.models.built_form.built_form import BuiltForm

__author__ = 'calthorpe_associates'


class ClientLandUse(BuiltForm):
    """
        A generic class describing land use for clients to subclass. This is used by the API to deliver client-specific BuiltForm classes
    """
    objects = InheritanceManager()
    class Meta(object):
        abstract = True
        app_label = 'main'