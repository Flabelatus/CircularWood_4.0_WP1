import rhinoscriptsyntax as rs
from ghpythonlib import components
from Grasshopper import Kernel
from math import floor
from ghpythonlib import treehelpers as th


class MatchMaker:

    def __init__(
            self,
            stool_parts,
            wood_ids,
            stool_pt_lengths,
            lengths_from_db,
            stool_parts_widths,
            widths_from_db,
            woods,
            tolerance,
            verbose=False
    ):

        self.stool_parts = stool_parts
        self.list_length = len(stool_parts)
        self.lengths_from_db = lengths_from_db
        self.stool_pt_lengths = stool_pt_lengths
        self.stool_parts_widths = stool_parts_widths
        self.widths_from_db = widths_from_db
        self.wood_ids = wood_ids
        self.verbose = verbose
        self.woods = woods
        self.tolerance = tolerance

        self.filtered_ids = []
        self.longest_ids = []
        self.longest_lenghts = []
        self.ape = []

        self.matched_stool_part_length = []
        self.removed_ids = []
        self.removed_lengths = []
        self.selected_ape = []
        self.updated_lengths = []

    def run(self):
        count = 0
        iteration = 0
        list_length = len(self.stool_parts)
        while len(self.stool_parts) > 0:
            for i in range(len(self.stool_parts)):
                sub_ = []
                for j in range(len(self.wood_ids)):
                    if self.stool_pt_lengths[i] < self.lengths_from_db[j] and self.stool_parts_widths[i] < \
                            self.widths_from_db[j]:
                        sub_.append(self.wood_ids[j])
                self.filtered_ids.append(sub_)

            if len(self.filtered_ids) > 0:
                for i in range(len(self.filtered_ids)):
                    self.longest_ids.append(self.wood_ids[i])
                    self.longest_lenghts.append(self.lengths_from_db[i])

            for i in range(len(self.longest_lenghts)):
                apes = []
                for j in range(len(self.stool_pt_lengths)):
                    apes.append(floor(self.longest_lenghts[i] / self.stool_pt_lengths[j]))
                self.ape.append(apes)

            selected_ape = [a for a in self.ape[count]][count]
            selected_length = self.longest_lenghts[count]
            x = self.stool_pt_lengths[count:int(selected_ape) + count]

            if x:
                self.matched_stool_part_length.append(x)
                self.removed_ids.append(self.longest_ids[0])
                self.longest_ids.remove(self.longest_ids[0])
                self.removed_lengths.append(self.longest_lenghts[0])
                self.longest_lenghts.remove(self.longest_lenghts[0])
                self.selected_ape.append(selected_ape)

            if count < list_length - 1:
                count += int(selected_ape)
                iteration += 1

            try:
                for i in range(count):
                    chunck_lengths = []
                    self.stool_parts.remove(self.stool_parts[i])
                    chunck_lengths.append(x[i])
            except:
                pass

            if self.verbose:
                print("Iteration: ", iteration)
                print("list length (stool parts): ", len(self.stool_parts))
                #                print("Longest IDs: ", self.longest_ids[0])
                print("stool part lengths: ", x, "INDEX: ", self.removed_ids[-1])
                print("APE: ", selected_ape)
        print("-" * 80)
        print("Successfully matched design and database parts...")

    def get_ape_series(self):
        apes_list = components.MassAddition(self.selected_ape)["partial_results"]
        apes_list.insert(0, 0)

        weave = []
        p_1 = apes_list[:-1]
        p_2 = apes_list[1:]

        for i in range(len(self.selected_ape)):
            weave.append(range(p_1[i], p_2[i]))
        print("Successfully created series of design element indecies...")
        if self.verbose:
            print("-" * 80)
            print(weave)
        return weave

    def evaluate_on_db_wood(self):
        series = self.get_ape_series()
        sum_of_stool_pt_lengths = []
        indecies = []

        for i in range(len(series)):
            o = []
            length_sums = []
            for j in series[i]:

                if j < self.list_length:
                    o.append(j)
                    length_sums.append(self.stool_pt_lengths[j])
            indecies.append(o)
            sum_of_stool_pt_lengths.append(sum(length_sums) + (self.tolerance * len(length_sums)))

        selection_guids = [self.woods[index - 1] for index in self.removed_ids]
        breps = [rs.coercebrep(s) for s in selection_guids]
        exploded = [components.DeconstructBrep(brep) for brep in breps]
        curves = [w.edges[0] for w in exploded]

        updated_lengths_list = []
        for i in range(len(self.removed_lengths)):
            updated_lengths_list.append(self.removed_lengths[i] - sum_of_stool_pt_lengths[i])

        print("Successfully updated the database wood lengths...")
        if self.verbose:
            print("-" * 80)
            print("New lengths: ", updated_lengths_list)
            print("Updated IDs: ", self.removed_ids)

        return th.list_to_tree(updated_lengths_list, 0)


def main():
    global removed_ids
    global removed_lengths
    global matched_stool_part_length
    global amount_per_element
    global updated_lengths

    d = MatchMaker(
        stool_parts=stool_parts,
        wood_ids=wood_ids,
        stool_pt_lengths=stool_pt_lengths,
        lengths_from_db=lengths_from_db,
        stool_parts_widths=stool_parts_widths,
        widths_from_db=widths_from_db,
        woods=woods,
        tolerance=tolerance,
        verbose=verbose
    )

    d.run()
    #    d.get_ape_series()
    updated_lengths = d.evaluate_on_db_wood()

    removed_ids = d.removed_ids
    removed_lengths = d.removed_lengths
    matched_stool_part_length = th.list_to_tree(d.matched_stool_part_length, 0)
    amount_per_element = th.list_to_tree(d.selected_ape, 0)


if __name__ == "__main__":
    main()
