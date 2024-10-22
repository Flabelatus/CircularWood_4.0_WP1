import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import *


class Resources:
    
    __routes__ = {
        "wood": {
            "admin": {
                "endpoints": [
                    "/admin/wood",                    
                    "/admin/wood/<int:wood_id>",      
                    "/admin/wood/delete-record/<int:wood_id>",
                    "/admin/woods/delete-all-records"
                ]
            },
            "general": {
                "endpoints": [
                    "/wood",             
                    "/wood/<int:wood_id>",      
                    "/wood/used/<int:wood_id>",
                ]
            },
            "logged_in": {
                "endpoints": [
                    "/logged_in/wood/<int:wood_id>" 
                ]
            },
            "reservation": {
                "endpoints": [
                    "/wood/reserve/<int:wood_id>",
                    "/wood/unreserve/<int:wood_id>"
                ]
            },
            "tablename": WoodModel.__tablename__
        },
    
        "sub_wood": {
            "general": {
                "endpoints": [
                    "/subwood",
                    "/subwood/<int:subwood_id>",
                ]
            },
            "by_wood_id": {
                "endpoints": [                                
                    "/subwood/wood/<int:wood_id>",
                ]
            },
            "by_design_id": {
                "endpoints": [
                    "/subwood/design/<int:design_id>"
                ]
            },
            "tablename": SubWoodModel.__tablename__
        },

        "production": {
            "general": {
                "endpoints": [
                    "/production",
                    "/production/<int:production_id>",
                ]
            },
            "by_wood_id": {
                "endpoints":[
                    "/production/wood/<int:wood_id>"
                ],
            },
            "tablename": ProductionModel.__tablename__
        },
        
        "design_requirements": {
            "general": {
                "endpoints": [
                    "/design/client",
                    "/design/client/<int:requirement_id>",
                ],
            },
            "by_project_id": {
                "endpoints": [
                    "/design/client/project/<string:project_id>",
                ],
            },
            "link_to_wood": {
                "endpoints": [
                    "/wood/link/<int:wood_id>/design/<int:requirement_id>",
                ],
            },
            "unlink_from_wood": {
                "endpoints": [
                    "/wood/unlink/<int:wood_id>/design/<int:requirement_id>",
                ],
            },
            "by_wood_id": {
                "endpoints": [
                    "/design/wood/<int:wood_id>",
                ],
            },
            "tablename": DesignRequirementsModelFromClient.__tablename__
        },

        "history":  {
            "general": {
                "endpoints": [
                    "/history",
                    "/history/<int:history_id>"
                ],
            },
            "by_wood_id": {
                "endpoints": [
                    "/history-by-wood-id/<int:wood_id>",
                ],
            },
            "tablename": HistoryModel.__tablename__
        },

        "image":  {
            "by_wood_id": {
                "endpoints": [
                    "/image/upload/<int:wood_id>",
                    "/image/<int:wood_id>"
                ],
            },
            "tablename": None
        },

        "idemat":  {
            "general": {
                "endpoints": [
                    "/impact",
                    "/impact/<int:impact_id>"
                ],
            },
            "by_wood_id": {
                "endpoints": [
                    "/impact/wood/<int:wood_id>",
                ],
            },
            "tablename": ImpactModel.__tablename__
        },
        "point_cloud":  {
            "general": {
                "endpoints": [
                    "/pointcloud",
                    "/pointcloud/<int:pcd_id>"
                ],
            },
            "by_wood_id": {
                "endpoints": [
                    "/pointcloud/wood/<int:wood_id>",
                ],
            },
            "tablename": PointCloudModel.__tablename__
        },

        "taglist":  {
           "general": {
               "endpoints": [
                    "/tags",
                    "/tag/<int:tag_id>",
                ],
           },
           "link_to_wood": {
               "endpoints": [
                    "/wood/<int:wood_id>/tag/<int:tag_id>",
                    "/woods_tags/<int:woods_tag_id>",
                    "/woods_tags/tag/<int:tag_id>",
                ],
           },
           "by_name": {
               "endpoints": [
                    "/tag/<string:tag_name>",
                    "/wood/tag/<string:tag_name>"
                ],
           },

            "tablename": TagModel.__tablename__
        },

        "user":  {
            "general": {
                "endpoints": [
                    "/user/<int:user_id>"
                ],
            },
            "authentication": {
                "endpoints": [
                    "/login",
                    "/refresh",
                    "/logout",
                    "/register",
                ],
            },
            "tablename": UserModel.__tablename__
        }
    }

    def add_new_endpoint(self, field: str, scope: str, route: str):
        assert field in self.__routes__, "The specified field is not among the resources"
        assert scope in self.__routes__[field], "The specified scope is not among the selected field"
        self.__routes__[field][scope]["endpoints"].append(route)

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
    
    def endpoints_by_field(self, field, scope='general'):
        assert field in self.__routes__, "The specified field is not among the resources"
        return self.__routes__[field][scope]['endpoints']
    
    def tablename_by_field(self, field):
        assert field in self.__routes__, "The specified field is not among the resources"
        return self.__routes__[field]["tablename"]
    

