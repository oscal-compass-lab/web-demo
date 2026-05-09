# Deploying Flask App to Vercel from GitHub

This guide explains how to deploy your Flask application to Vercel directly from GitHub.

## Prerequisites

1. Your code is pushed to a GitHub repository
2. You have a Vercel account (sign up at https://vercel.com)

## Deployment Steps

### 1. Connect GitHub to Vercel

1. Go to https://vercel.com and sign in
2. Click "Add New..." → "Project"
3. Click "Import Git Repository"
4. Authorize Vercel to access your GitHub account if not already done
5. Select your repository (web-demo)

### 2. Configure the Project

Vercel should automatically detect the Python/Flask configuration from `vercel.json`. 

**Important Settings:**
- **Framework Preset**: Other (or leave as detected)
- **Root Directory**: Leave as `.` (root)
- **Build Command**: Leave empty (Vercel handles Python builds automatically)
- **Output Directory**: Leave empty
- **Install Command**: `pip install -r requirements.txt`

### 3. Environment Variables (if needed)

If your app requires environment variables:
1. In the Vercel project settings, go to "Environment Variables"
2. Add any required variables (e.g., API keys, database URLs)

### 4. Deploy

1. Click "Deploy"
2. Vercel will:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Build and deploy your Flask app
   - Provide you with a live URL (e.g., `your-project.vercel.app`)

### 5. Automatic Deployments

Once connected:
- Every push to your main/master branch triggers a production deployment
- Pull requests get preview deployments automatically
- You can view deployment logs in the Vercel dashboard

## Files Created for Vercel

The following files have been added to support Vercel deployment:

1. **vercel.json** - Vercel configuration
   - Specifies Python runtime
   - Routes all requests to app.py

2. **api/index.py** - Serverless function entry point
   - Exports the Flask app for Vercel's serverless environment

3. **.vercelignore** - Files to exclude from deployment
   - Similar to .gitignore but for Vercel

## Testing Locally

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

Visit http://localhost:5000 to verify it works.

## Vercel CLI (Optional)

You can also deploy using the Vercel CLI:

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

## Important Notes

1. **Serverless Limitations**: Vercel runs Python apps as serverless functions with:
   - 10-second execution timeout (Hobby plan)
   - 50MB deployment size limit
   - Cold starts on first request

2. **Static Files**: Your `app-config/static` and `source-data/charts` directories will be served correctly

3. **Trestle Workspace**: The `trestle-workspace` directory will be included in the deployment

4. **Large Files**: If your workspace is very large, consider:
   - Using Vercel's file size limits
   - Storing large data in external storage (S3, etc.)
   - Using Vercel's Edge Config for configuration data

## Troubleshooting

If deployment fails:

1. Check the build logs in Vercel dashboard
2. Verify all dependencies are in `requirements.txt`
3. Ensure Python version compatibility (Vercel supports Python 3.9+)
4. Check that file paths are relative and work in serverless environment

## Next Steps

After successful deployment:
- Set up custom domain in Vercel settings
- Configure environment variables for production
- Set up monitoring and analytics
- Review Vercel's Python documentation: https://vercel.com/docs/functions/runtimes/python

## Support

- Vercel Documentation: https://vercel.com/docs
- Vercel Community: https://github.com/vercel/vercel/discussions
- Flask Documentation: https://flask.palletsprojects.com/