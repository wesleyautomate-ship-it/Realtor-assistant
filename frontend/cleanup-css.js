#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// List of CSS files to remove (redundant after unified design system)
const filesToRemove = [
  'src/App.css',
  'src/index.css',
  'src/styles/modern-design-system.css',
  'src/components/ModernChat.css',
  'src/components/ModernPropertyManagement.css',
  'src/components/EnhancedFileUpload.css',
  'src/components/AdminDashboard.css',
  'src/components/AdminDataManagement.css',
  'src/components/AdminRAGMonitoring.css',
  'src/components/ModernFileUpload.css',
  'src/components/FileUpload.css',
  'src/components/PropertyManagement.css',
  'src/auth/LoginForm.css',
  'src/auth/RegisterForm.css'
];

console.log('🧹 Cleaning up redundant CSS files...\n');

let removedCount = 0;
let errorCount = 0;

filesToRemove.forEach(filePath => {
  const fullPath = path.join(__dirname, filePath);
  
  try {
    if (fs.existsSync(fullPath)) {
      fs.unlinkSync(fullPath);
      console.log(`✅ Removed: ${filePath}`);
      removedCount++;
    } else {
      console.log(`⚠️  Not found: ${filePath}`);
    }
  } catch (error) {
    console.error(`❌ Error removing ${filePath}:`, error.message);
    errorCount++;
  }
});

console.log(`\n📊 Cleanup Summary:`);
console.log(`   ✅ Files removed: ${removedCount}`);
console.log(`   ❌ Errors: ${errorCount}`);
console.log(`   📁 Total files processed: ${filesToRemove.length}`);

if (errorCount === 0) {
  console.log('\n🎉 CSS cleanup completed successfully!');
  console.log('📝 All styling is now managed through the unified design system.');
} else {
  console.log('\n⚠️  Cleanup completed with some errors. Please check the output above.');
}
