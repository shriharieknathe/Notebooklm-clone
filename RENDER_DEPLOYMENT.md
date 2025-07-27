# Render Backend Deployment Guide

## Prerequisites

- GitHub repository with your code
- OpenAI API key
- Render account (free at [render.com](https://render.com))

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

Make sure your backend folder structure looks like this:
```
backend/
├── main.py
├── config.py
├── models.py
├── pdf_processor.py
├── vector_store.py
├── llm_service.py
├── requirements.txt
├── build.sh
└── uploads/ (will be created automatically)
```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Verify your email address

### Step 3: Create New Web Service

1. **Click "New +"** in your Render dashboard
2. **Select "Web Service"**
3. **Connect your GitHub repository**
4. **Choose your repository** from the list

### Step 4: Configure the Web Service

Fill in the following details:

#### **Basic Settings:**
- **Name**: `pdf-chat-backend` (or any name you prefer)
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: `backend` (important!)

#### **Build & Deploy Settings:**
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### **Environment Variables:**
Click "Advanced" and add these environment variables:

```
OPENAI_API_KEY=your_actual_openai_api_key_here
FRONTEND_URL=https://your-frontend-url.com
CHROMA_DB_PATH=./chroma_db
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.7
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### Step 5: Deploy

1. **Click "Create Web Service"**
2. **Wait for the build to complete** (usually 5-10 minutes)
3. **Check the logs** for any errors

### Step 6: Test Your Deployment

1. **Get your backend URL** from the Render dashboard
   - It will look like: `https://your-app-name.onrender.com`

2. **Test the health endpoint:**
   ```
   https://your-app-name.onrender.com/health
   ```

3. **Check API documentation:**
   ```
   https://your-app-name.onrender.com/docs
   ```

## Important Configuration Notes

### Environment Variables Explained

- **OPENAI_API_KEY**: Your OpenAI API key (required for chat functionality)
- **FRONTEND_URL**: Your frontend URL (for CORS configuration)
- **CHROMA_DB_PATH**: Where to store the vector database
- **UPLOAD_DIR**: Where to store uploaded PDFs
- **MAX_FILE_SIZE**: Maximum PDF file size (10MB default)
- **MODEL_NAME**: OpenAI model to use
- **TEMPERATURE**: AI response creativity (0.0-1.0)
- **CHUNK_SIZE**: How to split PDF text
- **CHUNK_OVERLAP**: Overlap between text chunks

### File Structure Requirements

Your `backend/` folder must contain:
- `main.py` - FastAPI application
- `requirements.txt` - Python dependencies
- `build.sh` - Build script (executable)
- All other Python modules

## Troubleshooting

### Common Issues

#### 1. **Build Fails**
- Check if `build.sh` is executable
- Verify all dependencies are in `requirements.txt`
- Check the build logs for specific errors

#### 2. **Runtime Errors**
- Check the deployment logs
- Verify environment variables are set correctly
- Ensure all required files are present

#### 3. **CORS Errors**
- Make sure `FRONTEND_URL` is set correctly
- Check if your frontend URL is accessible

#### 4. **API Key Issues**
- Verify your OpenAI API key is valid
- Check if you have sufficient credits

### Checking Logs

1. Go to your Render dashboard
2. Click on your web service
3. Go to "Logs" tab
4. Check for any error messages

### Making Changes

1. **Update your code** in GitHub
2. **Push to main branch**
3. **Render will automatically redeploy**
4. **Check the logs** for any issues

## Performance Considerations

### Free Tier Limitations
- **750 hours/month** (about 31 days)
- **512MB RAM**
- **Shared CPU**
- **Sleeps after 15 minutes of inactivity**

### Upgrading (if needed)
- **Starter Plan**: $7/month
- **Standard Plan**: $25/month
- **Pro Plan**: $85/month

## Security Best Practices

1. **Never commit API keys** to your repository
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** (automatic on Render)
4. **Set up proper CORS** configuration

## Next Steps

After successful backend deployment:

1. **Deploy your frontend** to Vercel/Netlify
2. **Update frontend environment variable** with your backend URL
3. **Test the complete application**
4. **Monitor usage** and performance

## Support

If you encounter issues:
1. Check the Render documentation
2. Review the deployment logs
3. Verify your configuration
4. Contact Render support if needed

Your backend will be available at: `https://your-app-name.onrender.com` 