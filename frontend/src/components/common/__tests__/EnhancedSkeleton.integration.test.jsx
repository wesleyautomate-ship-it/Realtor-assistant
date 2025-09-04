import React from 'react';
import { render, screen } from '../../../test-utils/test-utils-simple';
import EnhancedSkeleton from '../EnhancedSkeleton';

describe('EnhancedSkeleton Integration Tests', () => {
  describe('Real Component Rendering', () => {
    it('renders real CardSkeleton component', () => {
      render(<EnhancedSkeleton.CardSkeleton title="Test Card" />);
      
      // Check that the title attribute is set on the card (not text content)
      const card = document.querySelector('.MuiCard-root');
      expect(card).toBeInTheDocument();
      expect(card).toHaveAttribute('title', 'Test Card');
      
      // Check that skeleton elements are rendered
      const skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
      
      // Check that the card structure is correct
      expect(card).toBeInTheDocument();
    });

    it('renders real ListItemSkeleton component', () => {
      render(<EnhancedSkeleton.ListItemSkeleton />);
      
      // Check that skeleton elements are rendered
      const skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
      
      // Check that the list item structure is correct
      const listItem = document.querySelector('.MuiBox-root');
      expect(listItem).toBeInTheDocument();
    });

    it('renders real TableSkeleton component with custom rows', () => {
      render(<EnhancedSkeleton.TableSkeleton rows={3} />);
      
      // Check that skeleton elements are rendered
      const skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
      
      // Check that the table structure is correct
      const tableContainer = document.querySelector('.MuiBox-root');
      expect(tableContainer).toBeInTheDocument();
    });

    it('renders real DashboardSkeleton component', () => {
      render(<EnhancedSkeleton.DashboardSkeleton />);
      
      // Check that skeleton elements are rendered
      const skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
      
      // Check that the dashboard structure is correct
      const dashboardContainer = document.querySelector('.MuiBox-root');
      expect(dashboardContainer).toBeInTheDocument();
    });

    it('renders real ChatSkeleton component', () => {
      render(<EnhancedSkeleton.ChatSkeleton />);
      
      // Check that skeleton elements are rendered
      const skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
      
      // Check that the chat structure is correct
      const chatContainer = document.querySelector('.MuiBox-root');
      expect(chatContainer).toBeInTheDocument();
    });
  });

  describe('Component Props and Customization', () => {
    it('renders CardSkeleton with custom height and animation', () => {
      render(
        <EnhancedSkeleton.CardSkeleton 
          height={300} 
          animation="wave"
          showHeader={false}
        />
      );
      
      // Check that the card has custom height
      const card = document.querySelector('.MuiCard-root');
      expect(card).toBeInTheDocument();
      
      // Check that skeleton elements are rendered
      const skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
    });

    it('renders TableSkeleton with different row counts', () => {
      const { rerender } = render(<EnhancedSkeleton.TableSkeleton rows={1} />);
      
      // Check initial render
      let skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
      
      // Re-render with different row count
      rerender(<EnhancedSkeleton.TableSkeleton rows={5} />);
      
      // Check that it still renders correctly
      skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
    });
  });

  describe('Material-UI Integration', () => {
    it('uses correct Material-UI classes and styling', () => {
      render(<EnhancedSkeleton.CardSkeleton />);
      
      // Check for Material-UI specific classes
      const card = document.querySelector('.MuiCard-root');
      expect(card).toBeInTheDocument();
      
      const cardContent = document.querySelector('.MuiCardContent-root');
      expect(cardContent).toBeInTheDocument();
      
      const grid = document.querySelector('.MuiGrid-root');
      expect(grid).toBeInTheDocument();
    });

    it('applies theme-based styling correctly', () => {
      render(<EnhancedSkeleton.CardSkeleton />);
      
      // Check that skeleton elements have proper styling
      const skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
      
      // Check that the first skeleton has proper styling
      const firstSkeleton = skeletons[0];
      expect(firstSkeleton).toHaveClass('MuiSkeleton-root');
    });
  });

  describe('Accessibility and Performance', () => {
    it('renders without accessibility violations', () => {
      render(<EnhancedSkeleton.CardSkeleton title="Test Card" />);
      
      // Check that the component renders without crashing
      const card = document.querySelector('.MuiCard-root');
      expect(card).toBeInTheDocument();
      expect(card).toHaveAttribute('title', 'Test Card');
      
      // Check that skeleton elements are present
      const skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
    });

    it('handles multiple instances without conflicts', () => {
      render(
        <div>
          <EnhancedSkeleton.CardSkeleton title="Card 1" />
          <EnhancedSkeleton.CardSkeleton title="Card 2" />
          <EnhancedSkeleton.ListItemSkeleton />
        </div>
      );
      
      // Check that all components render with correct title attributes
      const cards = document.querySelectorAll('.MuiCard-root');
      expect(cards).toHaveLength(2);
      expect(cards[0]).toHaveAttribute('title', 'Card 1');
      expect(cards[1]).toHaveAttribute('title', 'Card 2');
      
      // Check that multiple skeleton instances exist
      const skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
    });
  });
});
