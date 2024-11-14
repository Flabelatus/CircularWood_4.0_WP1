import requests
import json

class Call_Wood_Data:

    def write_string_to_file(self,step_data, filename):
        """
        Writes a string to a file.

        Args:
            step_data (str): The data to be written to the file.
            filename (str): The name of the file to write to.
        """
        with open(filename, 'w') as step_file:
            step_file.write(step_data)

    def get_sub_wood(self,w_id=0):
        """
        Fetches sub-wood data from a web API.

        Args:
            w_id (int): The ID of the wood to retrieve sub-wood data for.

        Returns:
            dict: A dictionary containing the sub-wood data if successful, None otherwise.
        """
        url = "https://robotlab-residualwood.onrender.com/subwood/wood/{0}".format(w_id)
        resp = requests.get(url=url)
        if resp.status_code == 200:
            return resp.json()

    def countDigits(self,num):
        """
        Counts the number of digits in a number.

        Args:
            num (int): The number to count the digits of.

        Returns:
            int: The number of digits in the input number.
        """
        count = 0

        while num != 0:
            num //= 10
            count += 1
        return count

    def parse_to_JSON(self,input):
        """
        Converts a list of integers representing wood lengths into a JSON string.

        Args:
            input (list): A list of integers representing wood lengths.

        Returns:
            str: A JSON string containing the processed wood length data.
        """
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
        """
        Retrieves and processes wood data from a specified ID.

        Args:
            input_id (int): The ID of the wood to retrieve data for.

        Returns:
            str: A JSON string containing the processed wood length data.
        """
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