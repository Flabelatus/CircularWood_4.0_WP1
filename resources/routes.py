import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import *


class Resources:
    
    __routes__ = {
        "wood":  {
            "endpoints": [
                "/admin/wood",
                "/admin/wood/<int:wood_id>",
                "/admin/wood/delete-record/<int:wood_id>",
                "/admin/woods/delete-all-records",
                "/wood",
                "/wood/<int:wood_id>",
                "/wood/used/<int:wood_id>",
                "/logged_in/wood/<int:wood_id>",
                "/wood/reserve/<int:wood_id>",
                "/wood/unreserve/<int:wood_id>"
            ],
            "tablename": WoodModel.__tablename__
        },
        "sub_wood":  {
            "endpoints": [
                "/subwood",
                "/subwood/<int:subwood_id>",
                "/subwood/wood/<int:wood_id>",
                "/subwood/design/<int:design_id>",
            ],
            "tablename": SubWoodModel.__tablename__
        },
        "production": {
            "endpoints":[
                "/production",
                "/production/<int:production_id>",
                "/production/wood/<int:wood_id>"
            ],
            "tablename": ProductionModel.__tablename__

        },
        "design_requirements": {
            "endpoints": [
                "/design/client",
                "/design/client/<int:requirement_id>",
                "/design/client/project/<string:project_id>",
                "/wood/link/<int:wood_id>/design/<int:requirement_id>",
                "/wood/unlink/<int:wood_id>/design/<int:requirement_id>",
                "/design/wood/<int:wood_id>",
            ],
            "tablename": DesignRequirementsModelFromClient.__tablename__
        },

        "history":  {
            "endpoints": [
                "/history",
                "/history-by-wood-id/<int:wood_id>",
                "/history/<int:history_id>"
            ],
            "tablename": HistoryModel.__tablename__
        },

        "image":  {
            "endpoints": [
                "/image/upload/<int:wood_id>",
                "/image/<int:wood_id>"
            ],
            "tablename": None
        },

        "impact":  {
            "endpoints": [
                "/impact",
                "/impact/wood/<int:wood_id>",
                "/impact/<int:impact_id>"
            ],
            "tablename": ImpactModel.__tablename__
        },

        "point_cloud":  {
            "endpoints": [
                "/pointcloud",
                "/pointcloud/wood/<int:wood_id>",
                "/pointcloud/<int:pcd_id>"
            ],
            "tablename": PointCloudModel.__tablename__
        },

        "taglist":  {
            "endpoints": [
                "/tags",
                "/tag/<int:tag_id>",
                "/wood/<int:wood_id>/tag/<int:tag_id>",
                "/woods_tags/<int:woods_tag_id>",
                "/woods_tags/tag/<int:tag_id>",
                "/tag/<string:tag_name>",
                "/wood/tag/<string:tag_name>"
            ],
            "tablename": TagModel.__tablename__
        },

        "user":  {
            "endpoints": [
                "/login",
                "/refresh",
                "/logout",
                "/register",
                "/user/<int:user_id>"
            ],
            "tablename": UserModel.__tablename__
        }
    }

    def add_new_endpoint(self, field: str, route: str):
        assert field in self.__routes__, "The specified field is not among the resources"
        self.__routes__[field]["endpoints"].append(route)

    def add_new_tablename(self, field: str, tablename: str):
        assert field in self.__routes__, "The specified field is not among the resources"
        self.__routes__[field]["tablename"] = tablename

    def create_new_resource(self, field_name: str, routes: list, tablename: str):
        assert field_name not in self.__routes__, "The field already exist"
        
        new_field = {
            "endpoints": [],
            "tablename": tablename
        }
        
        self.__routes__[field_name] = new_field

        for route in routes:
            self.add_new_endpoint(field=field_name, route=route)
        return self.__routes__[field_name]

    @property
    def all_endpoints(self):
        endpoints = []
        for _, values in self.__routes__.items():
            endpoints.append(values["endpoints"])
        return endpoints
    
    def endpoints_by_field(self, field):
        assert field in self.__routes__, "The specified field is not among the resources"
        return self.__routes__[field]["endpoints"]
    
    def tablename_by_field(self, field):
        assert field in self.__routes__, "The specified field is not among the resources"
        return self.__routes__[field]["tablename"]
    

