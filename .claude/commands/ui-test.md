# UI/UX Testing Command

## Command: `/ui-test`

### Purpose
Comprehensive UI/UX testing for PropertyPro AI components using Playwright MCP.

### Usage
```
/ui-test [component-name] [options]
```

### Options
- `--screenshot`: Take screenshots of current state
- `--responsive`: Test across different device sizes
- `--accessibility`: Check accessibility compliance
- `--performance`: Analyze loading performance
- `--full`: Complete testing suite

### Examples
```
/ui-test marketing --screenshot
/ui-test dashboard --responsive
/ui-test voice-interface --full
```

## Workflow

### 1. Initial Assessment
1. Navigate to the specified component/page
2. Take initial screenshot
3. Check for console errors
4. Verify basic functionality

### 2. Visual Design Review
1. Compare against design principles in claude.md
2. Check color consistency
3. Verify typography and spacing
4. Validate button styles and hover states
5. Ensure voice interface prominence

### 3. Responsive Testing
1. Test mobile view (390x844)
2. Test tablet view (768x1024)
3. Test desktop view (1920x1080)
4. Take screenshots at each breakpoint
5. Check for layout issues

### 4. User Experience Validation
1. Test voice input functionality
2. Verify natural language processing
3. Check sample prompts
4. Validate actionable results
5. Test navigation flow

### 5. Technical Quality Check
1. Monitor console for errors
2. Check network requests
3. Validate performance metrics
4. Test loading states
5. Verify accessibility compliance

## Output Format

### Test Report
```
## 🧪 UI/UX Test Report: [Component Name]

### 📸 Visual Screenshots
- [Screenshot links]

### ✅ Passed Tests
- [List of successful validations]

### ❌ Failed Tests
- [List of issues found]

### 📱 Responsive Results
- Mobile: [Status]
- Tablet: [Status]
- Desktop: [Status]

### 🎯 Recommendations
- [Specific improvement suggestions]

### 🔧 Next Steps
- [Action items for fixes]
```

## Browser Configuration
```json
{
  "browser": "chromium",
  "headless": false,
  "devtools": true,
  "viewport": { "width": 1280, "height": 720 }
}
```

## Success Criteria
- No console errors
- Visual consistency with design system
- Proper responsive behavior
- Accessible interface
- Fast loading performance
- Voice-first interaction working
- Natural language input functional

## Common Issues to Check
- Voice interface not prominent enough
- Buttons missing hover states
- Inconsistent spacing
- Mobile layout problems
- Console errors
- Slow loading times
- Accessibility violations
- Brand inconsistency

Remember: Always take before/after screenshots to validate improvements!
