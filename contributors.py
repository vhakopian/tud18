from git import *
from date import *
import datetime




def get_dico(repo_path):
    repo = Repo(repo_path)

    commits  = repo.iter_commits()
    dico = {}
    dico_sizechurn = {}
    c=0
    
    for commit in repo.iter_commits('v4-dev'):
        
        year = int(datetime.datetime.fromtimestamp(commit.committed_date).strftime('%Y'))
        if(year >2016):
            continue
        c+=1
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
        print(c)
     
  
    for filename in dico_sizechurn:
        try:
            size = 0
            for commit, lines in repo.blame('HEAD', filename):
                size += len(lines)
            dico_sizechurn[filename]["size"]=size
            
            print(size)
            
        except :
            pass 
            
    return(dico, dico_sizechurn)


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



def write_results(dict, dict_sizechurn):

    file  = open("results.tsv", "w")
    file.write("filename\tminor\tmajor\ttotal\townership\tsize\tchurn\n")
    for filename in dict:
        d = dict[filename]
        d_sizechurn = dict_sizechurn[filename]

        file.write(filename + "\t" + str(d['minor'])+"\t"+str(d['major'])+"\t"+str(d['total'])+"\t"+str(d['ownership'])+"\t"+str(d_sizechurn['size'])+"\t"+str(d_sizechurn['churn'])+ "\n")

    file.close()

def main():
    path = "/Users/vahagn/bootstrap"
    dico, dico_sizechurn = get_dico(path)
    m = metrics(dico)
    write_results(m, dico_sizechurn)


if __name__ == "__main__":
    main()
