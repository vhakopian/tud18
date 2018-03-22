from date import *
from git import *

EMPTY_TREE_SHA   = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

def get_bug_dict(repo, branch):
    """
    arg: repo -> repository to be analysed
         branch -> branch to be analysed
    return : dictionary where the key is the file name and the value is the number of errors
    """
    bug_dict = {}
    commits_one_year = 0
    commits_six_months = 0
    bugs_found = 0
    commits_avant = 0
    for commit in repo.iter_commits(branch):
        #check if the commit was made after less that 12 months after the release
        if( one_year(commit)):
            commits_one_year+=1
        if(six_months(commit)):
            commits_six_months+=1
        if(between_beginning_2016_RL(commit)):
            commits_avant += 1
        if( not one_year(commit)):

            continue
        #check whether the commit was a bug fix or not
        if( not is_bug_fix(commit)):
            continue
        bugs_found+=1
        #adds the bugs fixed by the commit to the dictionary
    #    valid_bugs(bug_dict,commit,repo)
    print("one year:" + str(commits_one_year) + " six months: " + str(commits_six_months) + " bugs found: " + str(bugs_found) + " commits avant : " + str(commits_avant))
    return bug_dict


def valid_bugs(bug_dict, commit,repo) :
    """
    arg: bug_dict -> dictionary where the bugs will be added. The keys are file names and the values are number of errors in the file
         commit -> commit that fixed the errors
         repo -> repository to be analysed
    return: nothing
    """
    #initialize the parent commit, if the commit has no parent, we give if the SHA of an empty tree
    parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
    #look at each file that commit changed
    for item in commit.diff(parent):
        breaker = False #variable just to stop many loop at once
        try:
            #look at each line that was present in the commit's parent
            for commit_blamed, lines in repo.blame(parent,item.a_path):
                nline = 0
                #check if the line "bug" was added in the six months after the release
                if(not six_months(commit_blamed)):
                    continue
                #look at every line that was changed by the commit_blamed
                for line in lines:
                    nline +=1
                    #if the line was added in the first 6 months after the release and deleted in the bug fix commit, it introduces a bug
                    if(was_deleted(commit,line,commit_blamed,item.a_path,repo)):
                        #if the filename is already a key in the dictionary, we increment the value
                        #else, we introduce the filename as a key
                        if item.a_path in bug_dict:
                            bug_dict[item.a_path] += 1
                        else:
                            bug_dict[item.a_path] = 1
                        breaker = True
                        break
                if breaker:
                    break
        except:
            continue

def was_deleted(commit,searched_line,searched_line_commit,file_path,repo):
    """
    arg: commit -> commit to be analysed
        searched_line -> line of code to be searched in 'commit'
        searched_line_commit -> commit that added the searched line
        file_path -> file that contained the line
        repo -> repository to be analysed
    return: True if searched_line was deleted in 'commit'
            False if searched_line wasn't deleted in 'commit'
    """
    try:
        #look at every line in the commit
        for c,lines in repo.blame(commit,file_path):
            #if the line is in commit, it was included by the same commit in both files
            if c.hexsha == searched_line_commit.hexsha:
                if( searched_line in lines):
                    return False
    except:
        return False
    return True

def is_bug_fix(commit):
    """
    arg: commit -> commit to be tested
    return: True if a commit is a bug fix and False if it isn't
    """
    for key_word in ["fix", "bug", "defect"]:
        if(key_word in commit.message):
            return True
    return False

"""
    main function to test the module
"""
def main():
    path = "/Users/danielmendonca/git/bootstrap"
    repo = Repo(path)
    bug_dict = get_bug_dict(repo, 'master')
    print(bug_dict)
    print("hello" )

if __name__ == "__main__":
    main()
