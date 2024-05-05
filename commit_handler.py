import requests
import os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

class CommitHandler:
    
    def __init__(self, repo, token = None, commit_num=None):
        """
        Initialize the CommitHandler with a GitHub repository, an authentication token and the number of commits to be proccessed.
        
        :param repo: str - Full repository name (e.g., 'username/reponame')
        :param token: str - GitHub API token for authentication
        :param commit_num: int - number of commits to be proccessed
        """
        self.base_url = f"https://api.github.com/repos/{repo}/commits"
        self.headers = {'Authorization': f'token {token}'} if token else {}
        self.commits = []
        self.commit_num = commit_num


        self.fetch_commits()

    
    def fetch_commit_details(self, commit_url):
        """
        Fetch detailed information for a single commit.

        :param commit_url: str - commit url to request additional information
        """
        response = requests.get(commit_url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve commit: {response.status_code} - {response.text}")
            return None
        

    def fetch_commits(self):
        """
        Fetch all commits from the repository with pagination, using multithreading for efficiency.
        """
        commits_url = self.base_url + "?per_page=100"
        while commits_url:
            response = requests.get(commits_url, headers=self.headers)

            if response.status_code == 200:
                page_commits = response.json()
                
                if self.commit_num and len(self.commits) + len(page_commits) > self.commit_num:
                    keep = len(page_commits) - (len(self.commits) + len(page_commits) - self.commit_num)
                    page_commits = page_commits[:keep]

                with ThreadPoolExecutor() as executor:

                    future_to_commit = {executor.submit(self.fetch_commit_details, commit['url']): commit for commit in page_commits}

                    for future in as_completed(future_to_commit):
                        detailed_commit = future.result()
                        if detailed_commit:
                            self.commits.append(detailed_commit)
                  
                if 'next' in response.links and (not self.commit_num or len(self.commits) < self.commit_num):
                    commits_url = response.links['next']['url']
                else:
                    break

            else:
                print(f"Failed to retrieve commits: {response.status_code} - {response.text}")
                break

    def frequent_developer_pair(self, non_unique_dev = False, on_modules=False):
        """
        Crates a list of pairs of developers who most frequently contribute to the same files or modules

        :param unique_dev : bool, optional
        If True (default), only pairs that are the most frequent collaborators for both developers will be included.
        If False, pairs will be included if they are the most frequent for at least one of the developers.
        
        :param on_modules : bool, optional
        If True, contributions will be grouped by the highest-level module (directory) rather than individual files.
        If False (default), contributions will be checked at the file level.
        """
        dev_dev_map = {}
        file_dev_map = {}
        for commit in self.commits:
            author = commit['commit']['author']['name']
            files = commit.get('files', [])
            for file in files:
                name = file['filename']

                if on_modules:
                    directory = os.path.dirname(name)
                    if directory != "":
                        name = directory

                
                if name in file_dev_map:
                    file_dev_map[name].add(author)
                else:
                    file_dev_map[name] = {author}

        pair_count = Counter()

        for devs in file_dev_map.values():   
            devs_list = list(devs)
            length = len(devs_list)

            for dev1 in range(length):
                for dev2 in range(dev1 + 1, length):
                    if devs_list[dev1] < devs_list[dev2] :
                        first = devs_list[dev1]
                        second = devs_list[dev2]
                    else:
                        first = devs_list[dev2]
                        second = devs_list[dev1]
                    
                    pair_count[(first, second)] += 1 

        sorted_pairs = sorted(pair_count.items(), key=lambda x: x[1], reverse=True)
        
        dev_marked = {}
        freq_pairs = []
        
        prev_count = 0
        mark_queue = set()

        for pair, count in sorted_pairs:
            
            if (count != prev_count):
                for dev in mark_queue:
                    dev_marked[dev] = 1
                mark_queue = set()
                prev_count = count

            dev_pair_num = 0 
            
            for dev in pair:
                if dev not in dev_marked:
                    mark_queue.add(dev)
                else:
                    dev_pair_num += 1

            if (not non_unique_dev and dev_pair_num == 0) or (non_unique_dev and dev_pair_num <= 1):
                freq_pairs.append((pair, count))
    
        return freq_pairs

    
    

   
    def print_commit_info(self):
        """
        Print author and commit message for each commit.
        """
        for commit in self.commits:
            author = commit['commit']['author']['name']
            print(f"Author: {author}")