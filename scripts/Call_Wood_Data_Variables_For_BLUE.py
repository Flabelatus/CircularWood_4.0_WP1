import requests
import json

class Call_Wood_Data:

    def write_string_to_file(self,step_data, filename):
        with open(filename, 'w') as step_file:
            step_file.write(step_data)

    def get_sub_wood(self,w_id=0):
        url = "https://robotlab-residualwood.onrender.com/subwood/wood/{0}".format(w_id)
        resp = requests.get(url=url)
        if resp.status_code == 200:
            return resp.json()

    def countDigits(self,num):
        count = 0

        while num != 0:
            num //= 10
            count += 1
        return count

    def parse_to_JSON(self,input):
        d = dict()
        d["P_AMOUNT"] = str(len(input))

        for i in range(0, len(input)):
            field_name = f"P{str(i + 1)}L"
            d[field_name] = str(int(input[i]))
            field_name = f"P{str(i + 1)}L_len"
            d[field_name] = str(self.countDigits(input[i]))

        json_str = json.dumps(d)
        return json_str
        # return json.loads(JSON)

    def get_wood_data_from_id(self,input_id):

        lengths_list = []

        id_ = input_id
        data = self.get_sub_wood(id_)

        for sub_wood in data:
            lengths = sub_wood["length"]
            lengths_list.append(lengths)
        new_lengths_list = lengths_list

        temp = 0
        for i in range(0, len(lengths_list)):
            temp += lengths_list[i]
            new_lengths_list[i] = temp

        new_lengths_list_JSON = self.parse_to_JSON(new_lengths_list)

        return new_lengths_list_JSON