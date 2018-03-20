from github import Github

def get_dico(user, password):
    g = Github(user, password)
    repo_name = "pygame/pygame"
    repo = g.get_repo(repo_name)
    commits  = repo.get_commits()
    dico = {}
    c=0
    for commit in commits:
        c+=1
        contributor_name = commit.author.name
        for file in commit.files:
            file_name = file.filename
            if dico.has_key(file_name):
                if dico[file_name].has_key(contributor_name):
                    dico[file_name][contributor_name] += 1
                else: dico[file_name][contributor_name] = 1
            else:  
                dico[file_name] = {contributor_name: 1}
        print(c)
    return(dico)


def metrics(dico):
    
    output= {}
    
    for file in dico:
        
        total=0
        major=0
        minor=0
        ownership=0
        
        total_contributions=0
        
        for user in dico[file]:
            total_contributions += dico[file][user]
            
        for user in dico[file]:
            prop = dico[file][user]/total_contributions
            if prop>=0.05:
                major+=1    
            else:
                minor+=1
            if prop > ownership:
                ownership = prop 
                
        total = major + minor
        
        dico_file = {'total' : total, 'major':major, 'minor':minor, 'ownership':ownership}
    
        output[file]= dico_file
        
    return(output)
    
    

def write_results(dict): 
   
    file  = open("results.tsv", "w")
    file.write("filename\tminor\tmajor\ttotal\townership\n")
    for filename in dict:
        d = dict[filename]
        file.write(filename + "\t" + str(d['minor'])+"\t"+str(d['major'])+"\t"+str(d['total'])+"\t"+str(d['ownership'])+"\n")
    
    file.close()

def main():
    username = "*****"
    password = "*****"
    dico = get_dico(username, password)
    m = metrics(dico)
    write_results(m)


if __name__ == "__main__":
    main()
