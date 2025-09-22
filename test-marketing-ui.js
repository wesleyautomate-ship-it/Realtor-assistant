// Simple Playwright test for Marketing page UI
const { chromium } = require('playwright');

async function testMarketingUI() {
  console.log('🎭 Starting Marketing page UI test...');
  
  const browser = await chromium.launch({ 
    headless: false,
    devtools: true 
  });
  
  const page = await browser.newPage();
  
  try {
    // Navigate to Marketing page
    console.log('📱 Navigating to Marketing page...');
    await page.goto('http://localhost:5175/');
    
    // Click on Marketing button
    await page.click('text=Marketing');
    await page.waitForTimeout(2000);
    
    // Take screenshot
    console.log('📸 Taking screenshot...');
    await page.screenshot({ 
      path: 'screenshots/marketing-page-test.png',
      fullPage: true 
    });
    
    // Check for key elements
    console.log('🔍 Checking UI elements...');
    
    const voiceButton = await page.locator('button[aria-label*="microphone"], button[aria-label*="record"]').first();
    const hasVoiceButton = await voiceButton.isVisible();
    console.log(`✅ Voice button visible: ${hasVoiceButton}`);
    
    const samplePrompts = await page.locator('text=Sample Prompts').first();
    const hasSamplePrompts = await samplePrompts.isVisible();
    console.log(`✅ Sample prompts visible: ${hasSamplePrompts}`);
    
    const header = await page.locator('h2:has-text("Marketing")').first();
    const hasCorrectHeader = await header.isVisible();
    console.log(`✅ Marketing header visible: ${hasCorrectHeader}`);
    
    // Test responsive design
    console.log('📱 Testing responsive design...');
    
    // Mobile view
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ 
      path: 'screenshots/marketing-mobile.png',
      fullPage: true 
    });
    console.log('📸 Mobile screenshot saved');
    
    // Desktop view
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.screenshot({ 
      path: 'screenshots/marketing-desktop.png',
      fullPage: true 
    });
    console.log('📸 Desktop screenshot saved');
    
    console.log('✅ Marketing page UI test completed!');
    console.log('📁 Screenshots saved in /screenshots/ folder');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  } finally {
    await browser.close();
  }
}

testMarketingUI();
