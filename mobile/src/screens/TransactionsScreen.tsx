import React, { useState } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, SafeAreaView, ScrollView } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';

import { MOCK_TRANSACTIONS } from '../constants';
import { Transaction, TransactionStatus } from '../types';

type RootStackParamList = {
  TransactionDetail: { transactionId: string };
  // Add other screen params as needed
};

type TransactionScreenNavigationProp = StackNavigationProp<RootStackParamList, 'TransactionDetail'>;

const statusColors: Record<TransactionStatus, string> = {
  draft: '#9ca3af',
  in_progress: '#ea580c', // Orange from design guide
  pending_approval: '#f59e0b',
  completed: '#10b981',
  cancelled: '#ef4444',
};

const statusLabels: Record<TransactionStatus, string> = {
  draft: 'Draft',
  in_progress: 'In Progress',
  pending_approval: 'Pending Approval',
  completed: 'Completed',
  cancelled: 'Cancelled',
};

const TransactionsScreen = () => {
  const [transactions, setTransactions] = useState<Transaction[]>(MOCK_TRANSACTIONS);
  const navigation = useNavigation<TransactionScreenNavigationProp>();

  const getStatusBadge = (status: TransactionStatus) => (
    <View style={[styles.statusBadge, { backgroundColor: statusColors[status] }]}>
      <Text style={styles.statusText}>{statusLabels[status]}</Text>
    </View>
  );

  const getProgress = (milestones: any[]) => {
    const completed = milestones.filter(m => m.completed).length;
    return Math.round((completed / milestones.length) * 100);
  };

  const renderTransactionItem = ({ item }: { item: Transaction }) => {
    const progress = getProgress(item.milestones);
    const property = MOCK_PROPERTIES.find(p => p.id === item.propertyId);
    
    return (
      <TouchableOpacity 
        style={styles.transactionCard}
        onPress={() => navigation.navigate('TransactionDetail', { transactionId: item.id })}
      >
        <View style={styles.transactionHeader}>
          <Text style={styles.propertyTitle}>
            {property?.title || 'Property'}
          </Text>
          {getStatusBadge(item.status)}
        </View>
        
        <Text style={styles.priceText}>AED {item.salePrice?.toLocaleString() || item.offerAmount.toLocaleString()}</Text>
        
        <View style={styles.progressContainer}>
          <View style={styles.progressBar}>
            <View 
              style={[
                styles.progressFill, 
                { 
                  width: `${progress}%`,
                  backgroundColor: statusColors[item.status] || '#ea580c' 
                }
              ]} 
            />
          </View>
          <Text style={styles.progressText}>{progress}% Complete</Text>
        </View>
        
        <View style={styles.milestoneRow}>
          <View style={styles.milestoneCount}>
            <MaterialIcons name="check-circle" size={16} color="#10b981" />
            <Text style={styles.milestoneText}>
              {item.milestones.filter(m => m.completed).length} of {item.milestones.length} Milestones
            </Text>
          </View>
          <Text style={styles.dueDate}>
            Closing: {new Date(item.expectedClosingDate).toLocaleDateString()}
          </Text>
        </View>
      </TouchableOpacity>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Transaction Management</Text>
        <TouchableOpacity style={styles.addButton}>
          <MaterialIcons name="add" size={24} color="#fff" />
        </TouchableOpacity>
      </View>
      
      {transactions.length === 0 ? (
        <View style={styles.emptyState}>
          <MaterialIcons name="receipt-long" size={48} color="#9ca3af" />
          <Text style={styles.emptyStateText}>No transactions yet</Text>
          <Text style={styles.emptyStateSubtext}>Add your first transaction to get started</Text>
          <TouchableOpacity style={styles.primaryButton}>
            <Text style={styles.primaryButtonText}>+ New Transaction</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <FlatList
          data={transactions}
          renderItem={renderTransactionItem}
          keyExtractor={(item) => item.id}
          contentContainerStyle={styles.listContent}
          showsVerticalScrollIndicator={false}
        />
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  title: {
    fontSize: 20,
    fontWeight: '600',
    color: '#111827',
  },
  addButton: {
    backgroundColor: '#ea580c',
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  listContent: {
    padding: 16,
    paddingBottom: 32,
  },
  transactionCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  transactionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  propertyTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
    flex: 1,
    marginRight: 8,
  },
  statusBadge: {
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 12,
    minWidth: 80,
    alignItems: 'center',
  },
  statusText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  priceText: {
    fontSize: 20,
    fontWeight: '700',
    color: '#111827',
    marginBottom: 16,
  },
  progressContainer: {
    marginBottom: 12,
  },
  progressBar: {
    height: 8,
    backgroundColor: '#e5e7eb',
    borderRadius: 4,
    marginBottom: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 4,
  },
  progressText: {
    fontSize: 12,
    color: '#6b7280',
    textAlign: 'right',
  },
  milestoneRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  milestoneCount: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  milestoneText: {
    fontSize: 12,
    color: '#4b5563',
    marginLeft: 4,
  },
  dueDate: {
    fontSize: 12,
    color: '#6b7280',
    fontWeight: '500',
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  emptyStateText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#111827',
    marginTop: 16,
    marginBottom: 8,
  },
  emptyStateSubtext: {
    fontSize: 14,
    color: '#6b7280',
    textAlign: 'center',
    marginBottom: 24,
  },
  primaryButton: {
    backgroundColor: '#ea580c',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
  },
  primaryButtonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 14,
  },
});

export default TransactionsScreen;
