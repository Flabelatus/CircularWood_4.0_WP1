import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import *


# TODO: Add the method to dispatch routes
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
            "crud": {
                "endpoints": [
                    "/wood",             
                    "/wood/<int:wood_id>",      
                ]
            },
            "function_handler": {
                "endpoints": [
                    "/wood/used/<int:wood_id>",
                    "/wood/reserve/<int:wood_id>",
                    "/wood/unreserve/<int:wood_id>"
                ]
            },
            "tablename": WoodModel.__tablename__
        },
    
        "sub_wood": {
            "crud": {
                "endpoints": [
                    "/subwood",
                    "/subwood/<int:subwood_id>",
                ]
            },
            "relation": {
                "endpoints": [                                
                    "/subwood/wood/<int:wood_id>",
                    "/subwood/design/<int:design_id>"
                ]
            },
            "tablename": SubWoodModel.__tablename__
        },

        "production": {
            "crud": {
                "endpoints": [
                    "/production",
                    "/production/<int:production_id>",
                ]
            },
            "relation": {
                "endpoints":[
                    "/production/wood/<int:wood_id>"
                ],
            },
            "tablename": ProductionModel.__tablename__
        },
        
        "project": {
            "crud": {
                "endpoints": [
                    "/projects",
                    "/projects/<int:project_id>",
                ]
            },
            "tablename": ProjectModel.__tablename__
        },

        "design_geometry": {
            "crud": {
                "endpoints": [
                    "/design_geometries",
                    "/design_geometries/<int:geometry_id>",
                ]
            },
            "relation": {
                "endpoints": [
                    "/design_geometries/project/<int:project_id>"
                ]
            },
            "tablename": DesignGeometryModel.__tablename__
        },
        
        "requirements": {
            "crud": {
                "endpoints": [
                    "/design/client",
                    "/design/client/<int:requirement_id>",
                ],
            },
            "function_handler": {
                "endpoints": [
                    "/wood/link/<int:wood_id>/design/<int:requirement_id>",
                    "/wood/unlink/<int:wood_id>/design/<int:requirement_id>",
                ],
            },
            "relation": {
                "endpoints": [
                    "/design/wood/<int:wood_id>",
                    "/design/client/project/<string:project_id>",

                ],
            },
            "tablename": DesignRequirementsModelFromClient.__tablename__
        },

        "history":  {
            "crud": {
                "endpoints": [
                    "/history",
                    "/history/<int:history_id>"
                ],
            },
            "relation": {
                "endpoints": [
                    "/history-by-wood-id/<int:wood_id>",
                ],
            },
            "tablename": HistoryModel.__tablename__
        },

        "image":  {
            "function_handler": {
                "endpoints": [
                    "/image/upload/<int:wood_id>",
                    "/image/<int:wood_id>"
                ],
            },
            "tablename": None
        },

        "idemat":  {
            "crud": {
                "endpoints": [
                    "/impact",
                    "/impact/<int:impact_id>"
                ],
            },
            "relation": {
                "endpoints": [
                    "/impact/wood/<int:wood_id>",
                ],
            },
            "tablename": ImpactModel.__tablename__
        },
        
        "point_cloud":  {
            "crud": {
                "endpoints": [
                    "/pointcloud",
                    "/pointcloud/<int:pcd_id>"
                ],
            },
            "relation": {
                "endpoints": [
                    "/pointcloud/wood/<int:wood_id>",
                ],
            },
            "tablename": PointCloudModel.__tablename__
        },

        "taglist":  {
           "crud": {
               "endpoints": [
                    "/tags",
                    "/tag/<int:tag_id>",
                ],
           },
           "function_handler": {
               "endpoints": [
                    "/wood/<int:wood_id>/tag/<int:tag_id>",
                    "/woods_tags/<int:woods_tag_id>",
                    "/woods_tags/tag/<int:tag_id>",
                ],
           },
           "relation": {
               "endpoints": [
                    "/tag/<string:tag_name>",
                    "/wood/tag/<string:tag_name>"
                ],
           },

            "tablename": TagModel.__tablename__
        },

        "users":  {
            "crud": {
                "endpoints": [
                    "/user/<int:user_id>"
                ],
            },
            "function_handler": {
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
    
    def endpoints_by_field(self, field, scope='crud'):
        assert field in self.__routes__, "The specified field is not among the resources"
        return self.__routes__[field][scope]['endpoints']
    
    def tablename_by_field(self, field):
        assert field in self.__routes__, "The specified field is not among the resources"
        return self.__routes__[field]["tablename"]
    

