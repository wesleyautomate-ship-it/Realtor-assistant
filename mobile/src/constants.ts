import { ActionId, Task } from './types';

export const ACTION_ITEMS: { id: ActionId; title: string; icon?: string }[] = [
  { id: 'workflows', title: 'AURA Workflows' },
  { id: 'transactions', title: 'Transactions' },
  { id: 'marketing', title: 'Marketing' },
  { id: 'social', title: 'Social Media' },
  { id: 'analytics', title: 'Analytics' },
  { id: 'properties', title: 'Properties' },
  { id: 'content', title: 'Content' },
  { id: 'contacts', title: 'Contacts' },
  { id: 'playwright', title: 'Playwright' },
];

export const MOCK_TASKS: Task[] = [
  { id: 't-1', title: 'Follow up with Ali Khan', status: 'pending', dueDate: '2025-09-22' },
  { id: 't-2', title: 'Create CMA for Marina apt', status: 'in_progress', dueDate: '2025-09-24' },
  { id: 't-3', title: 'Schedule viewing - Palm villa', status: 'pending', dueDate: '2025-09-23' },
];

// Mock transaction data
export const MOCK_TRANSACTIONS = [
  {
    id: 'tx-1',
    propertyId: 'p-1',
    clientId: 'client-1',
    status: 'in_progress',
    offerAmount: 1800000,
    salePrice: 1850000,
    createdAt: '2025-09-01T10:00:00Z',
    updatedAt: '2025-09-15T14:30:00Z',
    expectedClosingDate: '2025-10-15',
    notes: 'Client is a first-time homebuyer. Pre-approved for 80% financing.',
    agentId: 'agent-1',
    milestones: [
      {
        id: 'm-1',
        type: 'offer_submitted',
        title: 'Offer Submitted',
        description: 'Initial offer submitted to seller',
        dueDate: '2025-09-01',
        completed: true,
        completedAt: '2025-09-01T15:30:00Z'
      },
      {
        id: 'm-2',
        type: 'offer_accepted',
        title: 'Offer Accepted',
        description: 'Seller accepted the offer with counter',
        dueDate: '2025-09-05',
        completed: true,
        completedAt: '2025-09-04T11:20:00Z'
      },
      {
        id: 'm-3',
        type: 'contract_signed',
        title: 'Contract Signed',
        description: 'Both parties signed the purchase agreement',
        dueDate: '2025-09-10',
        completed: true,
        completedAt: '2025-09-09T16:45:00Z'
      },
      {
        id: 'm-4',
        type: 'inspection',
        title: 'Property Inspection',
        description: 'Schedule and complete property inspection',
        dueDate: '2025-09-20',
        completed: false
      },
      {
        id: 'm-5',
        type: 'appraisal',
        title: 'Appraisal',
        description: 'Lender appraisal scheduled',
        dueDate: '2025-09-25',
        completed: false
      },
      {
        id: 'm-6',
        type: 'financing_approved',
        title: 'Financing Approved',
        description: 'Final mortgage approval from bank',
        dueDate: '2025-10-05',
        completed: false
      },
      {
        id: 'm-7',
        type: 'closing',
        title: 'Closing',
        description: 'Final closing and key handover',
        dueDate: '2025-10-15',
        completed: false
      },
      {
        id: 'm-8',
        type: 'possession',
        title: 'Possession',
        description: 'Client takes possession of property',
        dueDate: '2025-10-16',
        completed: false
      }
    ],
    documents: [
      {
        id: 'doc-1',
        name: 'Purchase Agreement.pdf',
        type: 'contract',
        url: 'https://example.com/documents/purchase-agreement-123.pdf',
        uploadedAt: '2025-09-10T14:30:00Z',
        size: 245678
      },
      {
        id: 'doc-2',
        name: 'Disclosure Form.pdf',
        type: 'disclosure',
        url: 'https://example.com/documents/disclosure-123.pdf',
        uploadedAt: '2025-09-11T10:15:00Z',
        size: 187654
      }
    ]
  },
  {
    id: 'tx-2',
    propertyId: 'p-2',
    clientId: 'client-2',
    status: 'pending_approval',
    offerAmount: 12000000,
    createdAt: '2025-09-10T09:30:00Z',
    updatedAt: '2025-09-12T16:45:00Z',
    expectedClosingDate: '2025-11-30',
    notes: 'Luxury property with custom upgrades. Client is an investor from overseas.',
    agentId: 'agent-1',
    milestones: [
      {
        id: 'm-21',
        type: 'offer_submitted',
        title: 'Offer Submitted',
        description: 'Initial offer submitted to seller',
        dueDate: '2025-09-12',
        completed: true,
        completedAt: '2025-09-12T11:20:00Z'
      },
      {
        id: 'm-22',
        type: 'offer_accepted',
        title: 'Offer Accepted',
        description: 'Waiting for seller response',
        dueDate: '2025-09-17',
        completed: false
      },
      // Other milestones will be added as the transaction progresses
    ],
    documents: []
  }
];

export const MOCK_PROPERTIES = [
  {
    id: 'p-1',
    title: '2BR Marina View Apartment',
    price: 'AED 1,850,000',
    area: 'Dubai Marina',
    sizeSqft: 1120,
    beds: 2,
    baths: 2,
    image: undefined as string | undefined,
  },
  {
    id: 'p-2',
    title: 'Palm Jumeirah Garden Villa',
    price: 'AED 12,400,000',
    area: 'Palm Jumeirah',
    sizeSqft: 5200,
    beds: 5,
    baths: 6,
    image: undefined as string | undefined,
  },
  {
    id: 'p-3',
    title: 'Downtown Burj View 1BR',
    price: 'AED 1,450,000',
    area: 'Downtown Dubai',
    sizeSqft: 780,
    beds: 1,
    baths: 1,
    image: undefined as string | undefined,
  },
];

