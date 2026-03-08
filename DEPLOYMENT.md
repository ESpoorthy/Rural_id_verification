# RuralGuard AI - Deployment Guide

## AWS Amplify Deployment

Your frontend is deployed at: https://main.d34ttefjam3p7q.amplifyapp.com

### Current Setup

The frontend is now configured to work with AWS Amplify. The `amplify.yml` file tells Amplify to serve files from the `frontend/` directory.

### Files Structure

```
Rural_id_verification/
├── frontend/           # Original frontend files
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── index.html         # Root copy for Amplify
├── app.js             # Root copy for Amplify
├── styles.css         # Root copy for Amplify
└── amplify.yml        # Amplify build configuration
```

### Important Notes

1. **Frontend Only**: Currently only the frontend is deployed on Amplify
2. **Backend Required**: The app needs the backend API to function fully
3. **Demo Mode**: When backend is unavailable, a notice is shown

## Deploying the Backend

To make the app fully functional, you need to deploy the backend API. Here are your options:

### Option 1: AWS Lambda + API Gateway (Recommended)

1. **Package the backend:**
   ```bash
   cd backend
   pip install -r requirements.txt -t package/
   cp demo_api.py package/
   cd package
   zip -r ../backend.zip .
   ```

2. **Create Lambda Function:**
   - Go to AWS Lambda Console
   - Create new function
   - Upload `backend.zip`
   - Set handler to `demo_api.handler`
   - Add API Gateway trigger

3. **Update Frontend:**
   - Edit `app.js` line 4
   - Replace with your API Gateway URL:
   ```javascript
   const API_BASE_URL = 'https://your-api-id.execute-api.region.amazonaws.com/prod/api/v1';
   ```

### Option 2: AWS Elastic Beanstalk

1. **Install EB CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize and Deploy:**
   ```bash
   cd backend
   eb init -p python-3.12 ruralguard-api
   eb create ruralguard-api-env
   eb deploy
   ```

3. **Get URL and update frontend**

### Option 3: Keep Backend Local (For Demo)

If you're just demoing locally:

1. **Start backend:**
   ```bash
   python backend/demo_api.py
   ```

2. **Use ngrok to expose locally:**
   ```bash
   ngrok http 8000
   ```

3. **Update app.js with ngrok URL**

## Amplify Configuration

The `amplify.yml` file is configured to:
- Serve static files from the `frontend/` directory
- No build process (pure HTML/CSS/JS)
- Deploy on every push to main branch

### Updating Amplify Settings

1. Go to AWS Amplify Console
2. Select your app
3. Go to "Build settings"
4. Verify `amplify.yml` is being used
5. Set base directory to `frontend` if needed

## Testing Deployment

1. **Frontend Only:**
   - Visit: https://main.d34ttefjam3p7q.amplifyapp.com
   - You should see the UI
   - Backend features won't work without API

2. **With Backend:**
   - Deploy backend first
   - Update API_BASE_URL in app.js
   - Push changes to trigger Amplify rebuild
   - Test full verification flow

## Troubleshooting

### Issue: "Page Not Found" on Amplify

**Solution:** 
- Check `amplify.yml` is in root directory
- Verify `baseDirectory: frontend` is set
- Ensure index.html exists in frontend/

### Issue: API Calls Failing

**Solution:**
- Check API_BASE_URL in app.js
- Verify backend is deployed and accessible
- Check CORS settings on backend
- Verify API Gateway configuration

### Issue: Amplify Build Fails

**Solution:**
- Check Amplify build logs
- Verify amplify.yml syntax
- Ensure all frontend files are committed

## Quick Deploy Checklist

- [ ] Frontend files in `frontend/` directory
- [ ] `amplify.yml` in root directory
- [ ] Root copies of HTML/CSS/JS (backup)
- [ ] Backend deployed (Lambda/EB/other)
- [ ] API_BASE_URL updated in app.js
- [ ] CORS enabled on backend
- [ ] Changes committed and pushed to GitHub
- [ ] Amplify rebuild triggered
- [ ] Test the deployed URL

## Cost Considerations

- **Amplify Hosting**: ~$0.15/GB served + $0.01/build minute
- **Lambda + API Gateway**: ~$0.20/million requests
- **Total Estimated**: < $5/month for demo usage

## Support

For issues:
1. Check Amplify build logs in AWS Console
2. Review browser console for errors
3. Test API endpoints directly
4. Check GitHub repository: https://github.com/ESpoorthy/Rural_id_verification

---

**Note:** For hackathon demo, you can run everything locally and use screen sharing instead of deploying the backend.
