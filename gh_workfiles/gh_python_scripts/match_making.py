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
            verbose=False
    ):

        self.stool_parts = stool_parts
        self.lengths_from_db = lengths_from_db
        self.stool_pt_lengths = stool_pt_lengths
        self.stool_parts_widths = stool_parts_widths
        self.widths_from_db = widths_from_db
        self.wood_ids = wood_ids
        self.verbose = verbose

        self.filtered_ids = []
        self.longest_ids = []
        self.longest_lenghts = []
        self.ape = []

        self.matched_stool_part_length = []
        self.removed_ids = []
        self.removed_lengths = []
        self.selected_ape = []

    def run(self):
        count = 0
        index = 0

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

            selected_ape = [a[0] for a in self.ape][index]
            selected_length = self.longest_lenghts[count]

            x = self.stool_pt_lengths[count:int(selected_ape) + count]

            if x:
                self.matched_stool_part_length.append(x)

                self.removed_ids.append(self.longest_ids[0])
                self.longest_ids.remove(self.longest_ids[0])

                self.removed_lengths.append(self.longest_lenghts[0])
                self.longest_lenghts.remove(self.longest_lenghts[0])

                self.selected_ape.append(selected_ape)

            count += int(selected_ape)
            index += 1

            try:
                for i in range(count):
                    chunck_lengths = []
                    self.stool_parts.remove(self.stool_parts[i])
                    chunck_lengths.append(x[i])
            except:
                pass

            if self.verbose:
                print("---------------------------------------------------")
                print("list length (stool parts): ", len(self.stool_parts))
                #                print("Longest IDs: ", self.longest_ids[0])
                print("stool part lengths: ", x, "INDEX: ", self.removed_ids[-1])
                print("APE: ", selected_ape)

        print("Successfully matched design and database parts...")


if __name__ == "__main__":
    d = MatchMaker(
        stool_parts=stool_parts,
        wood_ids=wood_ids,
        stool_pt_lengths=stool_pt_lengths,
        lengths_from_db=lengths_from_db,
        stool_parts_widths=stool_parts_widths,
        widths_from_db=widths_from_db,
        verbose=verbose
    )

    d.run()

    removed_ids = d.removed_ids
    removed_lengths = d.removed_lengths
    matched_stool_part_length = th.list_to_tree(d.matched_stool_part_length, 0)
    amount_per_element = th.list_to_tree(d.selected_ape, 0)