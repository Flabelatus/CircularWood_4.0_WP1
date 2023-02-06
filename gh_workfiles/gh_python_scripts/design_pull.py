"""__author__ = "Javid Jooshesh, j.jooshesh@hva.nl"
__version__ = "v1"
"""
import ghpythonlib.treehelpers as th
import rhinoscriptsyntax as rs
import Grasshopper.Kernel.Data as ghp
import Grasshopper.Kernel.Geometry.Plane as gh_plane


class Blocks:
    """_Class representing the wood plank geometries from the database_
    Attributes:
        source (DataTree[Breps]) : The list of box breps as a Grasshopper
            datatree
    Methods:
        explode_polysrf: ...
        explode_srf: ...
        get_block_length: ...
        get_block_width: ...
    """

    def __init__(self, source):
        """_Constructor of the class_
        Args:
            source (DataTree[objectid]) : The list of box breps
                as a Grasshopper datatree
        """

        self.source = source

    def __str__(self):
        return "A Class to Represent the Functions of " \
               "Form-Fitting for the Circular Wood Blocks from Scanned Database"

    def explode_polysrf(self):
        """Explode a brep object into the NURBS untrimmed surfaces"""
        p = []
        for i in range(len(self.source)):
            trimmed_srf = rs.ExplodePolysurfaces(self.source[i])
            blocks = []
            for srf in trimmed_srf:
                blocks.append(srf)
            p.append(blocks)
        data = th.list_to_tree(p, source=[0])
        return data

    def explode_srf(self):
        """Explode the surface into line segments"""
        p = []
        listed_tree = th.tree_to_list(self.explode_polysrf())
        curve = None
        for i in range(len(listed_tree)):
            curve_segments = []
            for j in range(len(listed_tree[i])):
                curve = rs.DuplicateEdgeCurves(listed_tree[i][j])
                curve_segments.append(curve)
            p.append(curve_segments)
        data = th.list_to_tree(p, source=[0])
        return data

    def get_block_length(self, position=2):
        """Return the length of the block as float. BigO(n^2)
            (not the most efficient way but it works for now)
        """
        list_of_lengths = []
        curves = th.tree_to_list(self.explode_srf())
        for i in range(len(curves)):
            blocks = []
            for j in range(len(curves[i])):
                lengths = []
                for k in range(len(curves[i][j])):
                    l = rs.CurveLength(curves[i][j][k])
                    lengths.append(l)
            blocks.append(sorted(lengths)[position])
            list_of_lengths.append(blocks)

        lengths_data_tree = th.list_to_tree(list_of_lengths, source=[0])
        return lengths_data_tree

    def get_block_width(self, position=1):
        """Return the width of the block as float"""
        widths = self.get_block_length(position=position)
        return widths
        
    def get_block_height(self, position=3):
        heights = self.get_block_length(position=position)
        return heights
    
    
class DesignModel:
    """_Class representing the design object and methods to fit the wood planks
    that are varaible in dimensions, within the boundary of the design_

    Attributes:
        design_region (DesignRegion) : The boundary of design
        blocks (Blocks) : The box breps representing the wood planks from the
            database
    Methods:
        orient: ...
        fit_blocks: ...
    """

    def __init__(self, design_region, blocks, heights, srf_index):
        """_Constructor method_"""

        self.region = DesignRegion(design_region, 0)
        self.srf_index = srf_index
        self.blocks = Blocks(blocks)
        self.blocks_length = self.blocks.get_block_length()
        self.blocks_width = self.blocks.get_block_width()
        self.blocks_height = heights
        self.index_list = []
        self.selection = []
        self.flatten_values()
    
    def flatten_values(self):
        """_Flatten the Length, Width and Height values_"""
        
        flatten_path_width = ghp.GH_Path(0)
        self.blocks_width.Flatten(flatten_path_width)
        flatten_path_length = ghp.GH_Path(0)
        self.blocks_length.Flatten(flatten_path_length)
        flatten_path_height = ghp.GH_Path(0)
        self.blocks_length.Flatten(flatten_path_height)


class DesignRegion:
    def __init__(self, brep, index):
        self.brep = brep
        self.index = index

    def explode(self):
        return rs.ExplodePolysurfaces(self.brep)

    def select_lowest_face(self):
        """Sort the faces of the Brep according to lowest `z` value of the
            centroids
        """
        exploded_surfaces = self.explode()
        z_coords = list()
        lowest_srf = None
        for i in range(len(exploded_surfaces)):
            centriod = rs.SurfaceAreaCentroid(exploded_surfaces[i])
            z_values = centriod[0][2]
            z_coords.append(z_values)
            if z_values == min(z_coords):
                lowest_srf = exploded_surfaces[i]
        return lowest_srf
    
    def select_custom_face(self, selected_index):
        exploded_surfaces = self.explode()
        for index, item in enumerate(exploded_surfaces):
            if index == selected_index:
                return item
    
    def find_edge(self, edge_index, surface_index):
        """Get the edge to populate blocks across within the design boundary"""
        selected_face = self.select_custom_face(surface_index)
        for index, item in enumerate(rs.DuplicateEdgeCurves(selected_face)):
            if index == edge_index:
                return item
                

class LinearElement:
    def __init__(self, line, blocks, used_blocks_index):
        self.blocks = Blocks(blocks)
        self.line = []
        for l in line:
            self.line.append(l)

        self.length = [rs.CurveLength(l) for l in self.line]
        self.start_point = [rs.CurvePoints(l)[0] for l in self.line]
        self.end_point = [rs.CurvePoints(l)[1] for l in self.line]
        self.normal_axis = []
        self.normal = []

        for i in range(len(self.start_point)):
            self.normal_axis.append(rs.VectorCreate(self.end_point[i], self.start_point[i]))
            self.normal.append(rs.PlaneFromNormal(self.start_point[i], self.normal_axis[i]))
        self.selection = []
        self.index_list = []
        self.used_index = used_blocks_index
        self.base = None
            
    def filter_used_blocks(self):
        unused_indexes = []
        for index in range(len(self.blocks.source)):
            if index in self.used_index:
                continue
            unused_indexes.append(index)
        return unused_indexes
    
    def pick_element(self, available_length, tolerane, r_tolerance):
        """_Select elements to build linear parts. Check the ratio
            of width and height as well_"""

        blocks_dict = {}    # blocks_dict = {lengths: blocks}
        lengths = th.tree_to_list(self.blocks.get_block_length())   # Python list
        
        filtered_blocks = self.filter_used_blocks()
        list_of_available_blocks = [self.blocks.source[i] for i in filtered_blocks]

        self.base = [rs.ExplodePolysurfaces(b)[1] for b in list_of_available_blocks]
        heights = [rs.SurfaceDomain(b, 1)[1] for b in self.base]
        widths = [rs.SurfaceDomain(b, 0)[1] for b in self.base]

        ratio = [widths[i] / heights[i] for i in range(len(heights))]

        for i in range(len(list_of_available_blocks)):
            if 0.5 < ratio[i] < r_tolerance:
                length = lengths[i][0]
                blocks_dict[length] = list_of_available_blocks[i]

        length_range = [range(int(l - (tolerane * 2)), int(l + (tolerane * 2))) for l in available_length]
        print(blocks_dict)
        block_list = []
        for i in range(len(length_range)):
            inner = []
            for key, value in blocks_dict.items():
                if int(key) in length_range[i]:
                    inner.append((value, key))
                    
                    self.selection.append(value)
                    del blocks_dict[key]
                    for index, item in enumerate(list_of_available_blocks):
                        if item == value:
                            self.index_list.append(index)
            block_list.append(inner)
#            print(inner)
        return th.list_to_tree(block_list[:], source=[0])


def main():
    global ratios
    global all_blocks
    global normal
    global linear_indecies
    global available_length
    
    test = DesignModel(design_boundary, wood_from_db, heights, 5)
    print(test)
    all_blocks = test.blocks.source
    packed_indecies = test.index_list
    packed_selection = test.selection

    normal = []
    li = []

    a = LinearElement(line_segment, wood_from_db, packed_indecies)
    available_length = []
        
    for i in line_segment:
        available_length.append(rs.CurveLength(i))

    ratios = a.pick_element(available_length, tolerane, ratio_tolerance)
    normal.append(a.normal)
    li.append(a.index_list)

    linear_indecies = th.list_to_tree(li, source=[0])
    linear_selection = a.selection
    normal = th.list_to_tree(normal, source=[0])


if __name__ == "__main__":
    main()

