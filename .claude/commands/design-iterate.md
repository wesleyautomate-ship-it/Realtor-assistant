# Design Iteration Command

## Command: `/design-iterate`

### Purpose
Iterative design improvement using Playwright MCP for visual feedback and validation.

### Usage
```
/design-iterate [component] [goal]
```

### Examples
```
/design-iterate marketing "improve voice interface prominence"
/design-iterate dashboard "make buttons more accessible"
/design-iterate voice-input "enhance waveform animation"
```

## Iterative Workflow

### 1. Initial State Capture
1. Navigate to the component
2. Take baseline screenshot
3. Document current issues
4. Set improvement goals

### 2. Design Analysis
1. Compare against PropertyPro AI design principles
2. Identify specific visual problems
3. Check responsive behavior
4. Validate accessibility compliance

### 3. Code Modifications
1. Make targeted improvements
2. Focus on one issue at a time
3. Follow design system guidelines
4. Maintain voice-first philosophy

### 4. Visual Validation
1. Take new screenshot
2. Compare with baseline
3. Check for regressions
4. Validate improvements

### 5. Iteration Loop
1. If issues remain, repeat steps 3-4
2. If satisfied, move to responsive testing
3. Document final state
4. Provide improvement summary

## Design Principles to Follow

### Voice-First Interface
- Large, prominent microphone button (20x20)
- Reactive waveform with 50 bars
- Clear timer display (00:00 format)
- Real-time audio level monitoring

### Natural Language Input
- Single prompt field (no complex forms)
- Helpful sample prompts
- Actionable results (Approve, Copy, Delete)
- No preview cards

### Visual Consistency
- Blue primary color (#3B82F6)
- Green secondary color (#10B981)
- 4px grid spacing system
- Consistent button styles
- Proper hover states

### Mobile-First Design
- Responsive from 390px width
- Touch-friendly button sizes
- Readable typography
- No horizontal scrolling

## Output Format

### Iteration Report
```
## 🔄 Design Iteration Report: [Component]

### 🎯 Goal
[Improvement objective]

### 📸 Before/After Screenshots
- Before: [Screenshot]
- After: [Screenshot]

### ✅ Improvements Made
- [List of specific changes]

### 📱 Responsive Validation
- Mobile: [Status]
- Tablet: [Status]
- Desktop: [Status]

### 🎨 Design Compliance
- [Check against design principles]

### 🔧 Code Changes
- [Summary of modifications]

### 📈 Results
- [Quantifiable improvements]
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

## Success Metrics
- Visual improvement in screenshots
- Better accessibility scores
- Improved responsive behavior
- Faster loading times
- Reduced console errors
- Enhanced user experience

## Common Iteration Patterns

### Voice Interface Enhancement
- Increase microphone button size
- Improve waveform animation
- Add better visual feedback
- Enhance timer display

### Button Improvements
- Add proper hover states
- Improve touch targets
- Enhance visual hierarchy
- Better color contrast

### Layout Optimization
- Fix spacing inconsistencies
- Improve responsive breakpoints
- Better content organization
- Enhanced visual flow

### Accessibility Improvements
- Better color contrast
- Improved focus states
- Screen reader compatibility
- Keyboard navigation

Remember: Each iteration should be validated with screenshots and tested across devices!
