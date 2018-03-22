from contributors import *

EMPTY_TREE_SHA   = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

def is_bug_fix(commit):
    for key_word in ["fix", "bug", "defect"]:
        if(key_word in commit.message):
            return True
    return False

def get_bug_dict(repo):
    bug_dict = {}
    c = 0
    print(c)
    for commit in repo.iter_commits('master'):
        c += 1
        print(c)
        if( not one_year(commit)):
            continue
        if( not is_bug_fix(commit)):
            continue
        valid_bugs(bug_dict,commit,repo)
    return bug_dict


def valid_bugs(bug_dict, commit,repo) :
    parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
    for item in commit.diff(parent):
        print(item.a_path)
        breaker = False
        try:
            for commit_blamed, lines in repo.blame(parent,item.a_path):
                print("commit sha:" + str(commit_blamed))
                nline = 0
                if(not six_months(commit_blamed)):
                    continue
                for line in lines:
                    nline +=1
                    print("file:" + item.a_path + "verifying line:" + str(nline))
                    if(was_deleted(commit,line,commit_blamed,item.a_path,repo)):
                        if item.a_path in bug_dict:
                            bug_dict[item.a_path] += 1
                        else:
                            bug_dict[item.a_path] = 1
                        breaker = True
                #        print("aa")
                        break
                if breaker:
                    break
        except:
            continue

def was_deleted(commit,searched_line,searched_line_commit,file_path,repo):
    try:
        for c,lines in repo.blame(commit,file_path):
            if c.hexsha == searched_line_commit.hexsha:
                if( searched_line in lines):
                    return False
    except:
        return False
    return True


def main():
    path = "/Users/danielmendonca/git/pygame"
    repo = Repo(path)
    bug_dict = get_bug_dict(repo)
    print(bug_dict)
    print("hello" )

if __name__ == "__main__":
    main()
