rm -rf ./output/
pelican ./content/ 
for i in `ls ../bingoarun.github.io`; do rm -rf ../bingoarun.github.io/$i; done
cp -r output/* ../bingoarun.github.io/
cd ../bingoarun.github.io/
git status
git add .
git commit -m "Automated commit - Changes made in pelican-github-site project"
git push
