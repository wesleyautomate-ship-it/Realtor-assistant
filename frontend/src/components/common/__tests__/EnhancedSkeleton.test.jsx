import React from 'react';
import { render, screen } from '../../../test-utils/test-utils-simple';
import EnhancedSkeleton from '../EnhancedSkeleton';

describe('EnhancedSkeleton Component', () => {
  describe('CardSkeleton', () => {
    it('renders card skeleton with title', () => {
      render(<EnhancedSkeleton.CardSkeleton title="Test Card" />);
      // Check that the title attribute is set on the card
      const card = document.querySelector('[title="Test Card"]');
      expect(card).toBeInTheDocument();
    });

    it('renders card skeleton without title', () => {
      render(<EnhancedSkeleton.CardSkeleton />);
      // Check that skeleton elements are rendered by looking for MUI Skeleton components
      const skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
    });
  });

  describe('ListItemSkeleton', () => {
    it('renders list item skeleton', () => {
      render(<EnhancedSkeleton.ListItemSkeleton />);
      // Check that skeleton elements are rendered
      const skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
    });
  });

  describe('TableSkeleton', () => {
    it('renders table skeleton with rows', () => {
      render(<EnhancedSkeleton.TableSkeleton rows={5} />);
      // Check that skeleton elements are rendered
      const skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
    });

    it('renders table skeleton with default rows', () => {
      render(<EnhancedSkeleton.TableSkeleton />);
      // Check that skeleton elements are rendered
      const skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
    });
  });

  describe('DashboardSkeleton', () => {
    it('renders dashboard skeleton', () => {
      render(<EnhancedSkeleton.DashboardSkeleton />);
      // Check that skeleton elements are rendered
      const skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
    });
  });

  describe('ChatSkeleton', () => {
    it('renders chat skeleton', () => {
      render(<EnhancedSkeleton.ChatSkeleton />);
      // Check that skeleton elements are rendered
      const skeletons = document.querySelectorAll('.MuiSkeleton-root');
      expect(skeletons.length).toBeGreaterThan(0);
    });
  });
});
