from contributors import *

EMPTY_TREE_SHA   = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

def is_bug_fix(commit):
    for key_word in ["fix", "bug", "defect"]:
        if(key_word in commit.message):
            return True
    return False

def get_bug_dict(repo):
    bug_dict = {}
    for commit in repo.iter_commits('v4-dev'):
        if( not one_year(commit)):
            continue
        if( not is_bug_fix(commit)):
            continue
        valid_bugs(bug_dict,commit,repo)
    return bug_dict


def valid_bugs(bug_dict, commit,repo) :
    parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
    for item in commit.diff(parent):
        breaker = False
        for commit_blamed, lines in repo.blame(parent,item.a_path):
            for line in lines:
                if(was_deleted(commit,line,commit_blamed,item.a_path,repo)):
                    if(six_months(commit_blamed)):
                        if bug_dict.has_key(item.a_path):
                            bug_dict[item.a_path] += 1
                        else:
                            bug_dict[item.a_path] = 1
                        breaker = True
                        break
            if breaker:
                break

def was_deleted(commit,searched_line,searched_line_commit,file_path,repo):
    for c,lines in repo.blame(commit,file_path):
        if c.hexsha == searched_line_commit.hexsha:
            if( searched_line in lines):
                return False
    return True


def main():
    path = "/Users/danielmendonca/git/bootstrap"
    dico = get_dico(path)
    bug_dict = get_bug_dict(dico)
    print(bug_dict)
