from commit_handler import CommitHandler
from output_formatter import OutputFormatter
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("-t", "--token", type = str, default = None, help='API token for authentication')
parser.add_argument('-non_unique_dev', action='store_true', help='Set to True to include non-unique developers.')
parser.add_argument("-modules", action='store_true', help='Set to True to check modules rather than files.')
parser.add_argument("-commit_num", type = int, default = None, help='Number of commits to be analyzed. If not set then all of the commits will be considered')
parser.add_argument("-r", "--repository", type=str, required=True, help='Repository to be checked')
args = parser.parse_args()

commitHandler = CommitHandler(args.repository, token = args.token, commit_num = args.commit_num)

if not commitHandler.failed_requests:    
    pairs = commitHandler.frequent_developer_pair(non_unique_dev = args.non_unique_dev, on_modules = args.modules)
    output_formatter = OutputFormatter()
    output_formatter.prettify_developer_pairs(pairs)


