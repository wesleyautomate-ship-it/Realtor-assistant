import React from 'react';
import { render, screen } from '../../../test-utils/test-utils-simple';
import TaskQueue from '../TaskQueue';

describe('TaskQueue Real Component Tests', () => {
  describe('Basic Component Rendering', () => {
    it('renders the TaskQueue component without crashing', () => {
      // Just check if the component renders without throwing errors
      expect(() => {
        render(<TaskQueue />);
      }).not.toThrow();
    });

    it('displays the component title', () => {
      render(<TaskQueue />);
      const title = screen.getByText(/Smart Task Queue/i);
      expect(title).toBeInTheDocument();
    });
  });

  describe('Component Structure', () => {
    it('has the expected Material-UI components', () => {
      render(<TaskQueue />);
      const boxes = document.querySelectorAll('.MuiBox-root');
      expect(boxes.length).toBeGreaterThan(0);
    });
  });

  describe('Error Handling', () => {
    it('handles rendering gracefully', () => {
      render(<TaskQueue />);
      const container = document.querySelector('.MuiBox-root');
      expect(container).toBeInTheDocument();
    });
  });
});
