import geopandas
from shapely import box

from model.IFilter import IFilter


class LKObjectTypeFilter(IFilter):

    def execute_filter(self) -> any:
        areas = geopandas.read_file(self.dataset, layer='lkflaeche')
        lines = geopandas.read_file(self.dataset, layer='lklinie')
        points = geopandas.read_file(self.dataset, layer='lkpunkt')
        return {
            'area_objects': areas,
            'line_objects': lines,
            'point_objects': points
        }


class RangeConstraintFilter(IFilter):
    def execute_filter(self) -> any:
        # Filter Attribute is the given Range in the format of clipsrc[xmin ymin xmax ymax]
        bbox = box(self.filter_attribute[0], self.filter_attribute[1], self.filter_attribute[2],
                   self.filter_attribute[3])
        dataframe_in_range = {
            'lkflaeche': self.dataset['area_objects'].cx[bbox.bounds[0]:bbox.bounds[2],
                         bbox.bounds[1]:bbox.bounds[3]],
            'lklinie': self.dataset['line_objects'].cx[bbox.bounds[0]:bbox.bounds[2],
                       bbox.bounds[1]:bbox.bounds[3]],
            'lkpunkt': self.dataset['point_objects'].cx[bbox.bounds[0]:bbox.bounds[2],
                       bbox.bounds[1]:bbox.bounds[3]]
        }
        return dataframe_in_range


class GroupingToDictionaryFilter(IFilter):
    def execute_filter(self) -> any:
        object_dictionary = {'lkobject_type': self.filter_attribute}
        for index, row in self.dataset[self.filter_attribute].iterrows():
            object_dictionary[row.obj_id] = {}
            object_dictionary[row.obj_id]['object_type'] = row.objektart
            object_dictionary[row.obj_id]['object_owner'] = row.eigentuemer
            object_dictionary[row.obj_id]['geometry'] = row.geometry.__geo_interface__['coordinates']
        return object_dictionary
