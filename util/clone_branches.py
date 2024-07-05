# How to clone:
# 1. Enable caching of git credentials with (default 15 min)
# git config --global credential.helper cache
# 2. Login with username and token after the first clone
# 3. Copy & Paste the remaining commands
print(f"tr -d '\\n' < ~/token.txt | xargs -0 -I {{}} git clone 'https://oauth2:{{}}@github.scch.at/ConTest/TrainTicket.git' --branch master --single-branch master")
branches = [f"ts-error-F{i}" for i in range(1, 23)]
branches.append("ts-error-cleaned")
branches.append("master")
for b in branches:
    # print(f"tr -d '\\n' < ~/token.txt | xargs -0 -I {{}} git clone 'https://oauth2:{{}}@github.scch.at/ConTest/TrainTicket.git' --branch {b} --single-branch {b};")
    print(f"tr -d '\\n' < ~/token.txt | xargs -0 -I {{}} git clone 'https://oauth2:{{}}@github.scch.at/ConTest/TrainTicket.git' --branch {b} --single-branch {b}; cd ./{b}; git lfs fetch --all;cd ..")

# Build maven. Hint: execute in multiple terminals for speedup
for b in branches:
    print(f"cd {b};mvn -DskipTests=true clean package;cd ..; ")
# Build and push docker images. Hint: execute in multiple terminals for speedup
for b in branches:
    print(f'''cd ./{b}; ./script/publish-docker-images.sh  containers.github.scch.at/contest/trainticket {b}; cd ..''')
# Build and push docker images. Hint: execute in multiple terminals for speedup
for b in branches:
    print(f'''cd ./{b}; ./PersistenceInit/publish-persinit-image.sh; cd ..''')
# Cleanup
for b in branches:
    print(f"cd {b};mvn  clean;cd ..; ")
# Delete
for b in branches:
    print(f"rm -rf {b}")

# All build steps combined
for b in branches:
    print(f"cd {b};mvn -DskipTests=true clean package;cd ..; ")
    print(f'''cd ./{b}; ./script/publish-docker-images.sh  containers.github.scch.at/contest/trainticket {b}; cd ..''')
    print(f"cd {b};mvn clean;cd ..; ")

print("\n\n")
# Build and push docker images. Hint: execute in multiple terminals for speedup
for b in branches:
    print(f'''cd ./{b}; ./script/publish-docker-images.sh  containers.github.scch.at/contest/trainticket {b}; cd ..''')
for b in branches:
    print(f'''cd ./{b}; ./PersistenceInit/publish-persinit-image.sh  containers.github.scch.at/contest/trainticket {b}; cd ..''')





for i in range(1, 23):
    print(f"tr -d '\\n' < ~/token.txt | xargs -0 -I {{}} git clone 'https://oauth2:{{}}@github.scch.at/ConTest/TrainTicket.git' --branch ts-error-F{i} --single-branch ts-error-F{i}")

for i in range(1, 23):
    print(f"rm -rf ts-error-F{i}")


# Build maven. Hint: execute in multiple terminals for speedup
for i in range(1, 23):
    print(f"cd ts-error-F{i};mvn -DskipTests=true clean package;cd ..; ")
# Build and push docker images. Hint: execute in multiple terminals for speedup
for i in range(1, 23):
    print(f'''cd ./ts-error-F{i}; ./script/publish-docker-images.sh  containers.github.scch.at/contest/trainticket ts-error-F{i}; cd ..''')
# Cleanup
for i in range(1, 23):
    print(f"cd ts-error-F{i};mvn  clean;cd ..; ")

# All build steps combined
for i in range(1, 23):
    print(f"cd ts-error-F{i};mvn -DskipTests=true clean package;cd ..; ")
    print(f'''cd ./ts-error-F{i}; ./script/publish-docker-images.sh  containers.github.scch.at/contest/trainticket ts-error-F{i}; cd ..''')
    print(f"cd ts-error-F{i};mvn clean;cd ..; ")

print("\n\n")
# Build and push docker images. Hint: execute in multiple terminals for speedup
for i in range(1, 23):
    print(f'''cd ./ts-error-F{i}; ./script/publish-docker-images.sh  containers.github.scch.at/contest/trainticket ts-error-F{i}; cd ..''')
for i in range(1, 23):
    print(f'''cd ./ts-error-F{i}; ./PersistenceInit/publish-persinit-image.sh  containers.github.scch.at/contest/trainticket ts-error-F{i}; cd ..''')

