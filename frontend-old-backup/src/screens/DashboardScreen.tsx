import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import type { ActionId, View as AppView } from '../types';

interface Props {
  actions: { id: ActionId; title: string; icon?: string }[];
  onActionClick: (id: ActionId) => void;
  onNavigate: (v: AppView) => void;
}

export default function DashboardScreen({ actions, onActionClick, onNavigate }: Props) {
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>PropertyPro AI</Text>
      <Text style={styles.subtitle}>Your Intelligent Real Estate Assistant</Text>

      <View style={styles.quickNav}>
        <TouchableOpacity style={styles.quickBtn} onPress={() => onNavigate('tasks')}>
          <Text style={styles.quickText}>Tasks</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.quickBtn} onPress={() => onNavigate('chat')}>
          <Text style={styles.quickText}>Chat</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.quickBtn} onPress={() => onNavigate('analytics')}>
          <Text style={styles.quickText}>Analytics</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.grid}>
        {actions.map((a) => (
          <TouchableOpacity key={a.id} style={styles.card} onPress={() => onActionClick(a.id)}>
            <Text style={styles.cardTitle}>{a.title}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 8 },
  subtitle: { fontSize: 14, color: '#666', marginBottom: 16 },
  quickNav: { flexDirection: 'row', gap: 8, marginBottom: 16 },
  quickBtn: { backgroundColor: '#111827', paddingHorizontal: 12, paddingVertical: 8, borderRadius: 9999 },
  quickText: { color: 'white', fontWeight: '700' },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 12 },
  card: { backgroundColor: '#F9FAFB', padding: 16, borderRadius: 12, width: '48%' },
  cardTitle: { color: '#111827', fontWeight: '700' }
});
