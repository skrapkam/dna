#!/bin/bash

# Create a clean deployment directory
echo "Creating clean deployment directory..."
rm -rf deploy/
mkdir deploy

# Copy only the necessary files for deployment
echo "Copying files for deployment..."
cp -r *.html deploy/
cp -r *.css deploy/
cp -r *.js deploy/ 2>/dev/null || true
cp -r *.jpg deploy/
cp -r *.png deploy/
cp -r *.gif deploy/
cp -r *.ico deploy/ 2>/dev/null || true
cp -r ch-en/ deploy/
cp -r WHY1_files/ deploy/ 2>/dev/null || true
cp -r WHAT_files/ deploy/ 2>/dev/null || true
cp -r YY_files/ deploy/ 2>/dev/null || true
cp -r H2_files/ deploy/ 2>/dev/null || true
cp -r ENT*-P*_files/ deploy/ 2>/dev/null || true
cp -r CHT*-P*_files/ deploy/ 2>/dev/null || true
cp -r CH-EN*-P*_files/ deploy/ 2>/dev/null || true
cp -r T*_files/ deploy/ 2>/dev/null || true

# Copy configuration files
cp vercel.json deploy/ 2>/dev/null || true
cp package.json deploy/ 2>/dev/null || true

echo "Deployment directory created at ./deploy/"
echo "Size: $(du -sh deploy/)"
echo ""
echo "To deploy:"
echo "cd deploy && vercel --prod" 