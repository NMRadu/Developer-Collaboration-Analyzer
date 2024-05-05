# Developer Collaboration Analyzer

This project analyzes the collaboration patterns between developers in a GitHub repository, identifying pairs of developers who frequently contribute to the same files or modules.

## Project Structure

- **dev_analyzer.py**: Main script to parse command-line arguments and execute the analysis.
- **commit_handler.py**: Contains the `CommitHandler` class that fetches commit data and identifies frequent developer pairs.
- **output_formatter.py**: Contains the `OutputFormatter` class to prettify and display the pairs of developers.


## Dependencies

The project requires Python 3.6+ and the following external libraries:
- `requests`: For accessing the GitHub API.

Install dependencies via pip:
```bash
pip install requests
```

# Usage
Run the dev_analyzer.py script to analyze the GitHub repository. The script accepts the following command-line arguments:

-r or --repository: The full name of the GitHub repository in username/repository format (required).
-t or --token: (Optional) GitHub API token for authentication. Useful for repositories with many commits or for private repositories.
-non_unique_dev: Set to True to include non-unique developer pairs. If omitted, the flag defaults to False.
-modules: Set to True to analyze contributions at the module (directory) level rather than the file level.
-commit_num: (Optional) The number of recent commits to analyze. If not set then all of the commits will be considered

# Explanation
To determine pairs of developers who most frequently contribute to the same files/modules in a GitHub repository, we first start requesting commit information from the repository (this is done in the `fetch_commit_details` method of the `CommitHandler` class). Following this, we determine how many times a pair of developers contribute to the same file/module and sort the list in descending order. Iterating through the sorted list, we take only pairs that are the most frequent collaborators for both developers will be included, however, if the `non_unique_dev` flag is set then pairs will be included if they are the most frequent for at least one of the developers (this is done in the `frequent_developer_pair` method of the `CommitHandler` class). Lastly, the list with the most frequent pairs is formatted and then printed (this is done in the `prettify_developer_pairs` method of the `OutputFormatter` class).


# Example Output
## Example 1:
### Input:
```bash
python3 dev_analyzer.py -r microsoft/vscode -commit_num 15
```
### Output:
```bash
Developer Pair                  | Count
------------------------------------------
Daniel Imms & Rob Lourens       |     4
Aaron Munger & Michael Lively   |     1
```
## Example 2:
### Input:
```bash
python3 dev_analyzer.py -r microsoft/vscode -non_unique_dev -commit_num 15
```
### Output:
```bash
Developer Pair                                | Count
--------------------------------------------------------
Daniel Imms & Rob Lourens                     |     4
Aaron Munger & Rob Lourens                    |     1
Aaron Munger & Michael Lively                 |     1
Rob Lourens & Tyler James Leonhardt           |     1
```
## Example 3:
### Input:
```bash
python3 dev_analyzer.py -r microsoft/vscode -commit_num 15 -modules
```
### Output:
```bash
Developer Pair                  | Count
------------------------------------------
Daniel Imms & Rob Lourens       |     3
Aaron Munger & Michael Lively   |     2
```

