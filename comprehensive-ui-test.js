// Comprehensive UI Test for Marketing Page
const { chromium } = require('playwright');

async function comprehensiveUITest() {
  console.log('🎨 Starting Comprehensive UI Test for Marketing Page...');
  
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
     
    // Take initial screenshot
    console.log('📸 Taking initial screenshot...');
    await page.screenshot({ 
      path: 'screenshots/marketing-initial.png',
      fullPage: true 
    });
    
    // UI Element Analysis
    console.log('\n🔍 UI Element Analysis:');
    
    // Check voice interface
    const voiceButton = await page.locator('button').filter({ hasText: /microphone|record|voice/i }).first();
    const voiceButtonVisible = await voiceButton.isVisible();
    console.log(`✅ Voice button visible: ${voiceButtonVisible}`);
    
    if (voiceButtonVisible) {
      const voiceButtonSize = await voiceButton.boundingBox();
      console.log(`📏 Voice button size: ${voiceButtonSize?.width}x${voiceButtonSize?.height}`);
    }
    
    // Check header
    const header = await page.locator('h2:has-text("Marketing")').first();
    const headerVisible = await header.isVisible();
    console.log(`✅ Marketing header visible: ${headerVisible}`);
    
    // Check sample prompts
    const samplePrompts = await page.locator('text=Sample Prompts').first();
    const samplePromptsVisible = await samplePrompts.isVisible();
    console.log(`✅ Sample prompts visible: ${samplePromptsVisible}`);
    
    // Check text input
    const textInput = await page.locator('textarea, input[type="text"]').first();
    const textInputVisible = await textInput.isVisible();
    console.log(`✅ Text input visible: ${textInputVisible}`);
    
    // Check submit button
    const submitButton = await page.locator('button').filter({ hasText: /submit|send|generate/i }).first();
    const submitButtonVisible = await submitButton.isVisible();
    console.log(`✅ Submit button visible: ${submitButtonVisible}`);
    
    // Responsive Design Testing
    console.log('\n📱 Responsive Design Testing:');
    
    const viewports = [
      { name: 'Mobile', width: 390, height: 844 },
      { name: 'Tablet', width: 768, height: 1024 },
      { name: 'Desktop', width: 1920, height: 1080 }
    ];
    
    for (const viewport of viewports) {
      console.log(`📱 Testing ${viewport.name} view (${viewport.width}x${viewport.height})...`);
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.waitForTimeout(1000);
      
      await page.screenshot({ 
        path: `screenshots/marketing-${viewport.name.toLowerCase()}.png`,
        fullPage: true 
      });
      
      // Check if elements are still visible and properly sized
      const voiceButtonResponsive = await voiceButton.isVisible();
      const headerResponsive = await header.isVisible();
      
      console.log(`  ✅ Voice button: ${voiceButtonResponsive ? 'Visible' : 'Hidden'}`);
      console.log(`  ✅ Header: ${headerResponsive ? 'Visible' : 'Hidden'}`);
    }
    
    // Accessibility Testing
    console.log('\n♿ Accessibility Testing:');
    
    // Check for alt text on images
    const images = await page.locator('img').all();
    console.log(`🖼️ Found ${images.length} images`);
    
    for (let i = 0; i < images.length; i++) {
      const alt = await images[i].getAttribute('alt');
      console.log(`  Image ${i + 1}: ${alt ? 'Has alt text' : 'Missing alt text'}`);
    }
    
    // Check button accessibility
    const buttons = await page.locator('button').all();
    console.log(`🔘 Found ${buttons.length} buttons`);
    
    for (let i = 0; i < buttons.length; i++) {
      const ariaLabel = await buttons[i].getAttribute('aria-label');
      const text = await buttons[i].textContent();
      console.log(`  Button ${i + 1}: ${ariaLabel || text ? 'Accessible' : 'Needs accessibility'}`);
    }
    
    // Performance Testing
    console.log('\n⚡ Performance Testing:');
    
    const startTime = Date.now();
    await page.reload();
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - startTime;
    
    console.log(`⏱️ Page load time: ${loadTime}ms`);
    
    // Console Error Check
    console.log('\n🐛 Console Error Check:');
    
    const errors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });
    
    await page.waitForTimeout(2000);
    console.log(`❌ Console errors found: ${errors.length}`);
    
    if (errors.length > 0) {
      errors.forEach((error, index) => {
        console.log(`  Error ${index + 1}: ${error}`);
      });
    }
    
    // Final Summary
    console.log('\n📊 Test Summary:');
    console.log('✅ Screenshots captured for all viewports');
    console.log('✅ UI elements analyzed');
    console.log('✅ Responsive design tested');
    console.log('✅ Accessibility checked');
    console.log('✅ Performance measured');
    console.log('✅ Console errors monitored');
    
    console.log('\n📁 Screenshots saved:');
    console.log('  - marketing-initial.png (Initial state)');
    console.log('  - marketing-mobile.png (Mobile view)');
    console.log('  - marketing-tablet.png (Tablet view)');
    console.log('  - marketing-desktop.png (Desktop view)');
    
    console.log('\n🎯 Recommendations:');
    if (!samplePromptsVisible) {
      console.log('  - Consider adding sample prompts for better UX');
    }
    if (errors.length > 0) {
      console.log('  - Fix console errors for better performance');
    }
    console.log('  - Review screenshots for visual improvements');
    console.log('  - Test voice functionality manually');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  } finally {
    await browser.close();
  }
}

comprehensiveUITest();
