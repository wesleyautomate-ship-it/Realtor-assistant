# PropertyPro AI - Claude Code Design Memory

## Visual Development Workflow

**CRITICAL**: For ANY front-end task, you MUST follow these steps:

1. **After making changes**, use Playwright MCP to automatically launch the relevant page in a browser
2. **Take a screenshot** of the modified component/page
3. **Analyze the screenshot** to visually verify changes against:
   - The prompt's requirements
   - Our design principles
   - General UI/UX best practices
4. **Check browser console** for any new errors
5. **Iterate on the design** until it is pixel-perfect
6. **Repeat this process** for each significant change

**Never skip the visual validation step!** Always use Playwright to see your changes before considering them complete.

## 🎨 Design Principles & Style Guide

### Brand Identity
- **App Name**: PropertyPro AI (formerly Laura AI)
- **Purpose**: AI-powered real estate assistant for agents
- **Philosophy**: "Less buttons, more natural language and prompting"
- **Voice-First**: Primary interaction through voice commands

### Visual Design System

#### Colors
- **Primary**: Blue (#3B82F6) - Trust, professionalism
- **Secondary**: Green (#10B981) - Growth, success
- **Accent**: Orange (#F59E0B) - Energy, action
- **Background**: Gray (#F9FAFB) - Clean, modern
- **Text**: Gray (#111827) - Readability

#### Typography
- **Headers**: Bold, clean sans-serif
- **Body**: Readable, medium weight
- **UI Elements**: Clear, actionable labels

#### Layout Principles
- **Mobile-First**: Responsive design starting from mobile
- **Clean Interface**: Minimal clutter, focus on functionality
- **Consistent Spacing**: 4px, 8px, 16px, 24px grid system
- **Card-Based**: Information organized in clean cards

### UI/UX Patterns

#### Voice Interface
- **Large Microphone Button**: 20x20 size with shadow
- **Reactive Waveform**: 50 bars that respond to audio
- **Timer Display**: 00:00 format for recording
- **Real-time Audio Level**: Visual feedback during recording

#### Navigation
- **Bottom Navigation**: Primary app navigation
- **Back Buttons**: Consistent left arrow with hover states
- **Action Grid**: 2x3 grid for main features

#### Content Generation
- **Natural Language Input**: Single prompt field
- **Sample Prompts**: Helpful suggestions for users
- **Actionable Results**: Approve, Copy, Delete buttons
- **No Preview Cards**: Direct actionable content

### Component Standards

#### Buttons
- **Primary**: Blue background, white text, rounded corners
- **Secondary**: White background, blue border, blue text
- **Destructive**: Red background for delete actions
- **Hover States**: Subtle color changes, smooth transitions

#### Forms
- **Input Fields**: Clean borders, focus rings, proper labels
- **Validation**: Real-time feedback, clear error messages
- **Submit**: Prominent, accessible buttons

#### Cards
- **Shadow**: Subtle drop shadows for depth
- **Padding**: Consistent 16px internal spacing
- **Border Radius**: 8px for modern look
- **Hover Effects**: Subtle elevation changes

## 🎭 Playwright MCP Usage Instructions

### When to Use Playwright
- **After UI Changes**: Always take screenshots after modifying components
- **Before Commits**: Verify visual changes match design principles
- **Responsive Testing**: Check mobile, tablet, desktop views
- **Error Detection**: Look for console errors and visual issues
- **Design Validation**: Compare against style guide and mockups

### Browser Configuration
```json
{
  "browser": "chromium",
  "headless": false,
  "devtools": true,
  "viewport": { "width": 1280, "height": 720 }
}
```

### Device Emulation
- **Mobile**: iPhone 12 (390x844)
- **Tablet**: iPad (768x1024)
- **Desktop**: 1920x1080

### Screenshot Workflow
1. Navigate to the page/component being modified
2. Take full-page screenshot
3. Compare against design principles
4. Identify visual issues or improvements
5. Make code adjustments
6. Re-screenshot and validate
7. Repeat until satisfied

### Design Review Checklist
- [ ] Colors match brand guidelines
- [ ] Typography is consistent and readable
- [ ] Spacing follows 4px grid system
- [ ] Buttons have proper hover states
- [ ] Voice interface is prominent and accessible
- [ ] Mobile responsiveness is maintained
- [ ] No console errors
- [ ] Loading states are handled
- [ ] Accessibility standards met

## 🚫 Avoid These Patterns

### Don't Add
- New CSS frameworks unless absolutely necessary
- Complex animations that slow down the app
- Too many buttons or form fields
- Generic UI components without brand customization
- Non-responsive designs

### Don't Remove
- Voice-first interaction patterns
- Natural language input fields
- Sample prompts for user guidance
- Actionable result buttons (Approve, Copy, Delete)
- Consistent navigation patterns

## 📱 Current App Structure

### Main Views
- **Dashboard**: Action grid with 6 main features
- **Marketing**: Voice/text input with content generation
- **Contact Management**: Client retention optimization
- **UI/UX Testing**: Playwright integration for design validation

### Key Components
- **CommandCenter**: Voice input with reactive waveform
- **MarketingView**: Natural language content generation
- **ContactManagementView**: Client follow-up automation
- **PlaywrightTestView**: Design validation tools

## 🎯 Success Criteria

### Visual Quality
- Clean, professional appearance
- Consistent with real estate industry standards
- Mobile-first responsive design
- Fast loading and smooth interactions

### User Experience
- Intuitive navigation
- Clear call-to-actions
- Helpful error messages
- Accessible to all users

### Technical Quality
- No console errors
- Proper TypeScript types
- Clean, maintainable code
- Good performance metrics

---

**Remember**: Always use Playwright to validate visual changes and ensure the UI matches these design principles!
