from git import *
from date import *
from numpy import *
from bug_finder import get_bug_dict
import datetime
import pickle



def get_dico(repo_path, branch, last_release_commit_id):
    """
    arg: repo_path -> path to the git repository
         branch -> name of the branch to be analysed
         last_release_commit_id -> last commit of the release to be alaysed
    return: dictionary where the key is a filename and the value is another dictionary of the type:
                {"size":size, "churn": churn,"minor":minor, "major":major, "total":total , "ownership":ownership}
    """
    repo = Repo(repo_path)
    commits  = repo.iter_commits()
    dico = {}
    dico_sizechurn = {}

    for commit in repo.iter_commits(branch):

        if not (between_beginning_2016_RL(commit)): continue


        contributor_name = commit.author.name
        changes = commit.stats.files

        for file in changes:

            file_name = str(file)
            churn = changes[file]['deletions']+changes[file]['insertions']

            if file_name in dico:
                if contributor_name in dico[file_name]:
                    dico[file_name][contributor_name] += 1
                else:
                    dico[file_name][contributor_name] = 1
            else:
                dico[file_name] = {contributor_name: 1}

            if file_name in dico_sizechurn:
                dico_sizechurn[file_name]["churn"] += churn
            else :
                dico_sizechurn[file_name] = {"churn" : churn, "size" : 0}

    deletedFiles = []

    for filename in dico_sizechurn:

        try:
            size = 0
            for commit, lines in repo.blame(last_release_commit_id, filename):
                size += len(lines)
            dico_sizechurn[filename]["size"]=size


        except :
            #the file named filename doesn't exist in the last release of 2016
            deletedFiles.append(filename)
            pass

    for file in deletedFiles:
            del dico[file]
            del dico_sizechurn[file]

    return(dico, dico_sizechurn)


def metrics(dico):
    """
    arg: dico ->dictionary where the keys are file names and the values are dictionaries with authors as keys and number of contributions as values

    return: dictionary that contains the metrics major, minor, total, ownership for each file
    """
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



def write_results(X,y,dict):

    file  = open("results.tsv", "w")
    file.write("filename\tsize\tchurn\tminor\tmajor\ttotal\townership\tbugs\n")
    i = 0

    for filename in dict:
        file.write(filename+"\t"+str(X[i,0])+"\t"+str(X[i,1])+"\t"+str(X[i,2])+"\t"+str(X[i,3])+"\t"+str(X[i,4])+"\t"+str(X[i,5])+"\t"+str(y[i])+"\n")
        i+=1

    file.close()


def vectorization(dict, dict_sizechurn, dict_bugs):
    X = []
    y = []

    for filename in dict:
        d = dict[filename]
        d_sizechurn = dict_sizechurn[filename]

        if filename in dict_bugs :
            bugs = dict_bugs[filename]
        else :
            bugs = 0

        X.append( [d_sizechurn["size"],d_sizechurn["churn"],d["minor"],d["major"],d["total"],d["ownership"]])

        y.append(bugs)

    return (array(X), array(y))


def save_data(X, y, path):
    pickle.dump([X,y], open(path, "wb"))


def load_data(path):
    data = pickle.load(open(path, "rb"))
    return data[0], data[1]


def main():
    path = "/Users/vahagn/bootstrap"
    dict_contributors, dict_sizechurn = get_dico(path, 'v4-dev', 'b5890e0608ad2262cde4a38e90afa19f1cb5d852')
    dict_metrics = metrics(dict_contributors)
    dict_bugs = get_bug_dict(Repo(path), 'v4-dev')

    (X, y) = vectorization(dict_metrics, dict_sizechurn, dict_bugs)
    write_results(X,y, dict_contributors)

    save_data(X,y,"/home/guillaume/Documents/Athens TUD18/save_bootstrap.pkl")



if __name__ == "__main__":
    main()
