# Adding GitHub Actions to Your Repository

## What This Does

The GitHub Actions workflow automatically tests your code every time you push changes or create a pull request. It:

1. **Tests on multiple Python versions** (3.8 through 3.13)
2. **Verifies mlx-lm can be installed and imported**
3. **Runs your test_installation.py script**
4. **Checks code syntax for errors**
5. **Runs optional code quality checks** (linting, security scanning)

## How to Add It

After you've pushed your initial code to GitHub:

```bash
# Make sure you're in your project directory
cd /mnt/user-data/outputs

# Add the GitHub Actions workflow
git add .github/workflows/test.yml

# Commit and push
git commit -m "Add GitHub Actions CI/CD workflow"
git push
```

## View Test Results

1. Go to your repository on GitHub
2. Click the "Actions" tab at the top
3. You'll see workflows running automatically on each push

Green checkmark = tests passed  
Red X = tests failed (click to see details)

## Adding a Status Badge

Once your first workflow runs, add this to the top of your README.md:

```markdown
![Tests](https://github.com/YOUR_USERNAME/mlx-quantize-gui/actions/workflows/test.yml/badge.svg)
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Workflow Triggers

The workflow runs automatically when:
- You push code to `main` or `develop` branches
- Someone creates a pull request to `main`

## Customizing the Workflow

Edit `.github/workflows/test.yml` to:
- Change which Python versions to test
- Add more test steps
- Modify branch triggers
- Add deployment steps

## What If Tests Fail?

Common reasons for test failures:
- **mlx-lm installation fails** - This is expected on non-macOS runners, but our workflow runs on macOS
- **Python version incompatibility** - We test 3.8-3.13 to catch these
- **Syntax errors** - The workflow will catch these before they reach users

Click on the failed workflow in GitHub Actions to see detailed logs and fix the issue.

## Cost

GitHub Actions is free for public repositories with generous usage limits. Your workflow uses minimal resources, so you won't hit any limits.

## Disabling Actions

If you don't want automated testing:
1. Go to repository Settings
2. Click "Actions" in the sidebar
3. Select "Disable Actions"

Or simply don't add the `.github/workflows/test.yml` file to your repository.
