from git import *
import datetime


EMPTY_TREE_SHA   = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

def get_dico(repo_path):
    repo = Repo(repo_path)

    commits  = repo.iter_commits()
    dico = {}
    c=0
    for commit in repo.iter_commits('v4-dev'):
    #    print(commit.committed_date)
        year = int(datetime.datetime.fromtimestamp(commit.committed_date).strftime('%Y'))
        if(year >2016):

            continue
        c+=1
        contributor_name = commit.author.name
        parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
        #print(contributor_name)
        for item in commit.diff(parent):
            file_name = item.a_path
        #    print(file_name)
            if dico.has_key(file_name):
                if dico[file_name].has_key(contributor_name):
                    dico[file_name][contributor_name] += 1
                else: dico[file_name][contributor_name] = 1
            else:
                dico[file_name] = {contributor_name: 1}

#        print(c)
#    print(dico)
    return(dico)


def metrics(dico):
    output= {}
    for file in dico:
        contributions=0
        major=0
        minor=0
        ownership=0
        for user in dico[file]:
            contributions += dico[file][ user]
        for user in dico[file]:
            prop = dico[file][ user]/float(contributions)
            if prop>=0.05:
                major+=1
            else:
                minor+=1
            if prop > ownership:
                ownership = prop
        dico_file = {'total' : minor+major, 'major':major, 'minor':minor, 'ownership':ownership}
        output[file]= dico_file
    return(output)



def write_results(dict):

    file  = open("results.tsv", "w")
    file.write("filename\tminor\tmajor\ttotal\townership\n")
    for filename in dict:
        d = dict[filename]
        file.write(filename + "\t" + str(d['minor'])+"\t"+str(d['major'])+"\t"+str(d['total'])+"\t"+str(d['ownership'])+ "\n")

    file.close()

def main():
    path = "/Users/danielmendonca/git/bootstrap"
    dico = get_dico(path)
    m = metrics(dico)
    write_results(m)


if __name__ == "__main__":
    main()
