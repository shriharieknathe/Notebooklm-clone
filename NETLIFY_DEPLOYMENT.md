# Netlify Frontend Deployment Guide

## Prerequisites

- GitHub repository with your frontend code
- Backend URL (from Render deployment)
- Netlify account (free at [netlify.com](https://netlify.com))

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

Make sure your frontend folder structure looks like this:
```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── App.js
│   ├── components/
│   ├── services/
│   └── ...
├── package.json
├── netlify.toml
└── README.md
```

### Step 2: Create Netlify Account

1. Go to [netlify.com](https://netlify.com)
2. Sign up with your GitHub account
3. Verify your email address

### Step 3: Deploy from Git

#### **Option A: Deploy from Git (Recommended)**

1. **Click "New site from Git"** in your Netlify dashboard
2. **Choose GitHub** as your Git provider
3. **Authorize Netlify** to access your GitHub repositories
4. **Select your repository** from the list

#### **Option B: Drag and Drop (Alternative)**

1. **Build your project locally:**
   ```bash
   cd frontend
   npm install
   npm run build
   ```
2. **Drag the `build` folder** to Netlify's deploy area

### Step 4: Configure Build Settings

If deploying from Git, configure these settings:

#### **Build Settings:**
- **Base directory**: `frontend` (if your repo has both frontend and backend)
- **Build command**: `npm run build`
- **Publish directory**: `build`

#### **Environment Variables:**
Click "Advanced build settings" → "Environment variables" and add:

```
REACT_APP_API_URL=https://your-backend-url.onrender.com
```

**Replace `your-backend-url.onrender.com` with your actual Render backend URL**

### Step 5: Deploy

1. **Click "Deploy site"**
2. **Wait for the build to complete** (usually 2-5 minutes)
3. **Check the build logs** for any errors

### Step 6: Test Your Deployment

1. **Get your frontend URL** from Netlify dashboard
   - It will look like: `https://your-app-name.netlify.app`
   - Or your custom domain if you set one up

2. **Test the application:**
   - Upload a PDF
   - Check if it connects to your backend
   - Test the chat functionality

## Custom Domain (Optional)

### Step 7: Set Up Custom Domain

1. **Go to "Domain settings"** in your Netlify dashboard
2. **Click "Add custom domain"**
3. **Enter your domain name**
4. **Follow the DNS configuration instructions**

## Environment Variables

### Required Variables

```
REACT_APP_API_URL=https://your-backend-url.onrender.com
```

### How to Set Environment Variables

1. **Go to Site settings** → **Environment variables**
2. **Add new variable:**
   - Key: `REACT_APP_API_URL`
   - Value: `https://your-backend-url.onrender.com`
3. **Save the variable**

### Important Notes

- **All React environment variables must start with `REACT_APP_`**
- **Changes to environment variables require a new deployment**
- **You can set different values for different branches**

## Troubleshooting

### Common Issues

#### 1. **Build Fails**
- Check if all dependencies are in `package.json`
- Verify Node.js version compatibility
- Check the build logs for specific errors

#### 2. **CORS Errors**
- Make sure your backend `FRONTEND_URL` is set correctly
- Check if your backend is accessible

#### 3. **API Connection Issues**
- Verify `REACT_APP_API_URL` is set correctly
- Check if your backend is running
- Test the backend URL directly

#### 4. **React Router Issues**
- The `netlify.toml` file includes redirects for React Router
- Make sure the redirect rule is working

### Checking Build Logs

1. Go to your Netlify dashboard
2. Click on your site
3. Go to "Deploys" tab
4. Click on any deployment to see logs

### Making Changes

1. **Update your code** in GitHub
2. **Push to main branch**
3. **Netlify will automatically redeploy**
4. **Check the build logs** for any issues

## Performance Optimization

### Built-in Optimizations

- **Automatic HTTPS**
- **Global CDN**
- **Automatic builds and deployments**
- **Asset optimization**

### Additional Optimizations

1. **Enable asset optimization** in Site settings
2. **Set up form handling** if needed
3. **Configure redirects** for better SEO
4. **Enable analytics** for monitoring

## Security Features

### Automatic Security

- **HTTPS by default**
- **DDoS protection**
- **Automatic security headers**
- **Bot protection**

### Custom Security Headers

The `netlify.toml` file includes:
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `X-Content-Type-Options: nosniff`

## Free Tier Limitations

### What's Included

- **100GB bandwidth/month**
- **300 build minutes/month**
- **Unlimited sites**
- **Custom domains**
- **Form submissions (100/month)**

### When to Upgrade

- **High traffic** (>100GB/month)
- **Many builds** (>300 minutes/month)
- **Advanced features** (password protection, etc.)

## Next Steps

After successful frontend deployment:

1. **Test the complete application**
2. **Set up monitoring** (optional)
3. **Configure custom domain** (optional)
4. **Set up analytics** (optional)

## Support

If you encounter issues:
1. Check the Netlify documentation
2. Review the build logs
3. Verify your configuration
4. Contact Netlify support if needed

Your frontend will be available at: `https://your-app-name.netlify.app` 