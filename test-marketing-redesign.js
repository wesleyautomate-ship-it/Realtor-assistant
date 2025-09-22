// Test Marketing Page Redesign
const { chromium } = require('playwright');

async function testMarketingRedesign() {
  console.log('🎨 Testing Marketing Page Redesign...');
  
  const browser = await chromium.launch({ 
    headless: false,
    devtools: true 
  });
  
  const page = await browser.newPage();
  
  try {
    // Navigate to Marketing page
    console.log('📱 Navigating to Marketing page...');
    await page.goto('http://localhost:5173/');
    
    // Click on Marketing button
    await page.click('text=Marketing');
    await page.waitForTimeout(3000);
    
    // Take screenshot of redesigned page
    console.log('📸 Taking screenshot of redesigned Marketing page...');
    await page.screenshot({ 
      path: 'screenshots/marketing-redesign-v1.png',
      fullPage: true 
    });
    
    // Test responsive design
    console.log('📱 Testing responsive design...');
    
    // Mobile view
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ 
      path: 'screenshots/marketing-redesign-mobile-v1.png',
      fullPage: true 
    });
    
    // Desktop view
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.screenshot({ 
      path: 'screenshots/marketing-redesign-desktop-v1.png',
      fullPage: true 
    });
    
    // Check for key elements
    console.log('🔍 Checking redesigned elements...');
    
    const voiceButton = await page.locator('button[aria-label*="Start recording"], button[aria-label*="Stop recording"]').first();
    const hasVoiceButton = await voiceButton.isVisible();
    console.log(`✅ Voice button visible: ${hasVoiceButton}`);
    
    const header = await page.locator('h2:has-text("Marketing")').first();
    const hasHeader = await header.isVisible();
    console.log(`✅ Marketing header visible: ${hasHeader}`);
    
    const toggleButtons = await page.locator('button:has-text("Voice Input"), button:has-text("Text Input")').all();
    console.log(`✅ Toggle buttons found: ${toggleButtons.length}`);
    
    // Check for modern styling elements
    const gradientBackground = await page.locator('.bg-gradient-to-br').first();
    const hasGradient = await gradientBackground.isVisible();
    console.log(`✅ Gradient background: ${hasGradient}`);
    
    const roundedElements = await page.locator('.rounded-3xl, .rounded-2xl').all();
    console.log(`✅ Modern rounded elements: ${roundedElements.length}`);
    
    const shadowElements = await page.locator('.shadow-xl, .shadow-2xl').all();
    console.log(`✅ Enhanced shadows: ${shadowElements.length}`);
    
    console.log('✅ Marketing page redesign test completed!');
    console.log('📁 Screenshots saved:');
    console.log('  - marketing-redesign-v1.png (Initial redesign)');
    console.log('  - marketing-redesign-mobile-v1.png (Mobile view)');
    console.log('  - marketing-redesign-desktop-v1.png (Desktop view)');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  } finally {
    await browser.close();
  }
}

testMarketingRedesign();
