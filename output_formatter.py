
class OutputFormatter:
    def __init__(self):
        pass

    def prettify_developer_pairs(self, pairs_list):
        """
        Print the developer pairs and their collaboration count in a formatted table.
        
        :param pairs_list: list of tuples - Each tuple contains a pair of developer names and their collaboration count.
        """
        if len(pairs_list) == 0:
            print("No pairs have been found")
            return

        max_length = max(len(dev) for pair in pairs_list for dev in pair[0])
        max_length = max(max_length, len("Developer Pair"), len("Count"))

        print(f"{'Developer Pair':<{max_length * 2 + 3}} | {'Count':>5}")
        print("-" * (max_length * 2 + 14))

        for pair, count in pairs_list:
            dev_pair = f"{pair[0]} & {pair[1]}"
            print(f"{dev_pair:<{max_length * 2 + 3}} | {count:>5}")
