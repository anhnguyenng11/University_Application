A very simplified coding session workflow

Step 1: Make sure you are in the main branch and pull (update) the newest version
git checkout main
git pull --rebase

Step 2: Quick check on the new version to see if there is anything new you should know (eg. new functions on the code)

Step 3: Create a new branch for your own function
git checkout -b [feature]

Step 4: Write some code like you normally do. Add some non-obvious comments if you can (to describe what that function does, or describe a line of code that seems hard to understand)

Step 5: Add and commit
git add .
git commit -m "[Commit description]"

Step 6: Push (publish) your code
git push -u origin feature/brief-description

Step 7 (Optional): Go to GitHub and merge your code. Resolve merge conflicts if needed.

Step 8: Go back to main branch and start over
git checkout main