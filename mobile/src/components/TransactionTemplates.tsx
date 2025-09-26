import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, FlatList, Modal } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';

import { TransactionTemplate, MilestoneType } from '../types';

const defaultTemplates: TransactionTemplate[] = [
  {
    id: 'temp-1',
    name: 'Offer Submitted',
    subject: 'Offer Submitted - {{propertyTitle}}',
    body: 'Dear {{clientName}},\n\nI am pleased to inform you that we have successfully submitted your offer for {{propertyTitle}} in the amount of AED {{offerAmount}}.\n\nThe seller has until {{responseDeadline}} to respond. I will notify you as soon as we receive their response.\n\nPlease let me know if you have any questions in the meantime.\n\nBest regards,\n{{agentName}}',
    milestoneTypes: ['offer_submitted'],
    isDefault: true,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: 'temp-2',
    name: 'Inspection Scheduled',
    subject: 'Inspection Scheduled - {{propertyTitle}}',
    body: 'Hi {{clientName}},\n\nThe inspection for {{propertyTitle}} has been scheduled for {{inspectionDate}} at {{inspectionTime}}.\n\nPlease let me know if you would like to be present during the inspection. The inspection typically takes 2-3 hours.\n\nAfter the inspection, we will receive a detailed report which I will review with you.\n\nBest regards,\n{{agentName}}',
    milestoneTypes: ['inspection'],
    isDefault: true,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: 'temp-3',
    name: 'Closing Instructions',
    subject: 'Closing Instructions - {{propertyTitle}}',
    body: 'Dear {{clientName}},\n\nWe are approaching the closing date for {{propertyTitle}}! Here are the details for the closing:\n\n- Date: {{closingDate}}\n- Time: {{closingTime}}\n- Location: {{closingLocation}}\n- Documents to bring: {{requiredDocuments}}\n\nPlease review the attached closing disclosure and let me know if you have any questions. I will be there to guide you through the entire process.\n\nLooking forward to handing you the keys!\n\nBest regards,\n{{agentName}}',
    milestoneTypes: ['closing'],
    isDefault: true,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
];

type TransactionTemplatesProps = {
  selectedMilestone?: MilestoneType;
  onSelectTemplate?: (template: TransactionTemplate) => void;
  onClose?: () => void;
  visible: boolean;
};

const TransactionTemplates: React.FC<TransactionTemplatesProps> = ({
  selectedMilestone,
  onSelectTemplate,
  onClose,
  visible,
}) => {
  const [templates, setTemplates] = useState<TransactionTemplate[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const [newTemplate, setNewTemplate] = useState<Partial<TransactionTemplate>>({
    name: '',
    subject: '',
    body: '',
    milestoneTypes: selectedMilestone ? [selectedMilestone] : [],
  });

  useEffect(() => {
    // In a real app, this would fetch from an API
    setTemplates(defaultTemplates);
  }, []);

  const filteredTemplates = templates.filter(template => {
    const matchesSearch = template.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      template.subject.toLowerCase().includes(searchQuery.toLowerCase());
    
    if (selectedMilestone) {
      return matchesSearch && template.milestoneTypes.includes(selectedMilestone);
    }
    
    return matchesSearch;
  });

  const handleCreateTemplate = () => {
    if (!newTemplate.name || !newTemplate.subject || !newTemplate.body) {
      alert('Please fill in all fields');
      return;
    }

    const template: TransactionTemplate = {
      id: `temp-${Date.now()}`,
      name: newTemplate.name!,
      subject: newTemplate.subject!,
      body: newTemplate.body!,
      milestoneTypes: newTemplate.milestoneTypes || [],
      isDefault: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    setTemplates([...templates, template]);
    setNewTemplate({
      name: '',
      subject: '',
      body: '',
      milestoneTypes: selectedMilestone ? [selectedMilestone] : [],
    });
    setIsCreating(false);
  };

  const renderTemplateItem = ({ item }: { item: TransactionTemplate }) => (
    <TouchableOpacity 
      style={styles.templateItem}
      onPress={() => onSelectTemplate?.(item)}
    >
      <View style={styles.templateHeader}>
        <Text style={styles.templateName}>{item.name}</Text>
        {item.isDefault && (
          <View style={styles.defaultBadge}>
            <Text style={styles.defaultBadgeText}>Default</Text>
          </View>
        )}
      </View>
      <Text style={styles.templateSubject} numberOfLines={1}>
        {item.subject}
      </Text>
      <Text style={styles.templateSnippet} numberOfLines={2}>
        {item.body.split('\n')[0]}
      </Text>
      <View style={styles.templateFooter}>
        <View style={styles.milestoneTags}>
          {item.milestoneTypes.map((type) => (
            <View key={type} style={styles.milestoneTag}>
              <Text style={styles.milestoneTagText}>
                {type.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
              </Text>
            </View>
          ))}
        </View>
        <MaterialIcons name="chevron-right" size={20} color="#9ca3af" />
      </View>
    </TouchableOpacity>
  );

  return (
    <Modal
      visible={visible}
      animationType="slide"
      transparent={false}
      onRequestClose={onClose}
    >
      <View style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={onClose} style={styles.closeButton}>
            <MaterialIcons name="close" size={24} color="#6b7280" />
          </TouchableOpacity>
          <Text style={styles.title}>Communication Templates</Text>
          <TouchableOpacity 
            style={styles.createButton}
            onPress={() => setIsCreating(true)}
          >
            <MaterialIcons name="add" size={20} color="#fff" />
          </TouchableOpacity>
        </View>

        {!isCreating ? (
          <>
            <View style={styles.searchContainer}>
              <MaterialIcons name="search" size={20} color="#9ca3af" style={styles.searchIcon} />
              <TextInput
                style={styles.searchInput}
                placeholder="Search templates..."
                value={searchQuery}
                onChangeText={setSearchQuery}
                placeholderTextColor="#9ca3af"
              />
            </View>

            <FlatList
              data={filteredTemplates}
              renderItem={renderTemplateItem}
              keyExtractor={(item) => item.id}
              contentContainerStyle={styles.templatesList}
              ListEmptyComponent={
                <View style={styles.emptyState}>
                  <MaterialIcons name="description" size={48} color="#d1d5db" />
                  <Text style={styles.emptyStateText}>No templates found</Text>
                  <Text style={styles.emptyStateSubtext}>
                    {selectedMilestone 
                      ? `No templates for ${selectedMilestone.replace('_', ' ')}`
                      : 'Create a new template to get started'}
                  </Text>
                </View>
              }
            />
          </>
        ) : (
          <ScrollView style={styles.formContainer}>
            <Text style={styles.formTitle}>New Template</Text>
            
            <View style={styles.formGroup}>
              <Text style={styles.label}>Template Name</Text>
              <TextInput
                style={styles.input}
                placeholder="e.g., Offer Submitted"
                value={newTemplate.name}
                onChangeText={(text) => setNewTemplate({...newTemplate, name: text})}
              />
            </View>
            
            <View style={styles.formGroup}>
              <Text style={styles.label}>Email Subject</Text>
              <TextInput
                style={styles.input}
                placeholder="e.g., Offer Submitted - {{propertyTitle}}"
                value={newTemplate.subject}
                onChangeText={(text) => setNewTemplate({...newTemplate, subject: text})}
              />
            </View>
            
            <View style={styles.formGroup}>
              <Text style={styles.label}>Email Body</Text>
              <TextInput
                style={[styles.input, styles.textArea]}
                placeholder="Write your email template here..."
                value={newTemplate.body}
                onChangeText={(text) => setNewTemplate({...newTemplate, body: text})}
                multiline
                numberOfLines={8}
                textAlignVertical="top"
              />
              <Text style={styles.variablesHint}>
                Use {{variableName}} for dynamic content (e.g., {{clientName}}, {{propertyTitle}})
              </Text>
            </View>
            
            <View style={styles.formGroup}>
              <Text style={styles.label}>Applicable Milestones</Text>
              <View style={styles.milestoneOptions}>
                {Object.values([
                  'offer_submitted',
                  'offer_accepted',
                  'contract_signed',
                  'inspection',
                  'appraisal',
                  'financing_approved',
                  'closing',
                  'possession',
                ] as MilestoneType[]).map((milestone) => (
                  <TouchableOpacity
                    key={milestone}
                    style={[
                      styles.milestoneOption,
                      newTemplate.milestoneTypes?.includes(milestone) && styles.milestoneOptionSelected,
                    ]}
                    onPress={() => {
                      const types = [...(newTemplate.milestoneTypes || [])];
                      const index = types.indexOf(milestone);
                      
                      if (index === -1) {
                        types.push(milestone);
                      } else {
                        types.splice(index, 1);
                      }
                      
                      setNewTemplate({...newTemplate, milestoneTypes: types});
                    }}
                  >
                    <Text style={[
                      styles.milestoneOptionText,
                      newTemplate.milestoneTypes?.includes(milestone) && styles.milestoneOptionTextSelected,
                    ]}>
                      {milestone.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>
            
            <View style={styles.formActions}>
              <TouchableOpacity 
                style={[styles.button, styles.cancelButton]}
                onPress={() => setIsCreating(false)}
              >
                <Text style={styles.cancelButtonText}>Cancel</Text>
              </TouchableOpacity>
              
              <TouchableOpacity 
                style={[styles.button, styles.saveButton]}
                onPress={handleCreateTemplate}
              >
                <Text style={styles.saveButtonText}>Save Template</Text>
              </TouchableOpacity>
            </View>
          </ScrollView>
        )}
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  closeButton: {
    padding: 8,
    marginLeft: -8,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: '#111827',
  },
  createButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#ea580c',
    justifyContent: 'center',
    alignItems: 'center',
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f3f4f6',
    borderRadius: 8,
    margin: 16,
    paddingHorizontal: 12,
  },
  searchIcon: {
    marginRight: 8,
  },
  searchInput: {
    flex: 1,
    height: 48,
    color: '#111827',
  },
  templatesList: {
    padding: 16,
    paddingTop: 8,
  },
  templateItem: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#e5e7eb',
  },
  templateHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  templateName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
    flex: 1,
  },
  defaultBadge: {
    backgroundColor: '#ecfdf5',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
    marginLeft: 8,
  },
  defaultBadgeText: {
    fontSize: 12,
    color: '#065f46',
    fontWeight: '500',
  },
  templateSubject: {
    fontSize: 14,
    color: '#374151',
    marginBottom: 4,
  },
  templateSnippet: {
    fontSize: 13,
    color: '#6b7280',
    marginBottom: 12,
  },
  templateFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: '#f3f4f6',
    paddingTop: 12,
  },
  milestoneTags: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    flex: 1,
  },
  milestoneTag: {
    backgroundColor: '#f3f4f6',
    borderRadius: 4,
    paddingHorizontal: 8,
    paddingVertical: 2,
    marginRight: 6,
    marginBottom: 4,
  },
  milestoneTagText: {
    fontSize: 10,
    color: '#4b5563',
    fontWeight: '500',
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 40,
  },
  emptyStateText: {
    fontSize: 16,
    color: '#374151',
    fontWeight: '500',
    marginTop: 16,
    marginBottom: 4,
  },
  emptyStateSubtext: {
    fontSize: 14,
    color: '#9ca3af',
    textAlign: 'center',
  },
  formContainer: {
    flex: 1,
    padding: 16,
  },
  formTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 24,
  },
  formGroup: {
    marginBottom: 20,
  },
  label: {
    fontSize: 14,
    fontWeight: '500',
    color: '#374151',
    marginBottom: 8,
  },
  input: {
    backgroundColor: '#f9fafb',
    borderRadius: 8,
    padding: 12,
    fontSize: 14,
    color: '#111827',
    borderWidth: 1,
    borderColor: '#e5e7eb',
  },
  textArea: {
    minHeight: 120,
    textAlignVertical: 'top',
  },
  variablesHint: {
    fontSize: 12,
    color: '#6b7280',
    marginTop: 4,
    fontStyle: 'italic',
  },
  milestoneOptions: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: 8,
  },
  milestoneOption: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    backgroundColor: '#f3f4f6',
    marginRight: 8,
    marginBottom: 8,
    borderWidth: 1,
    borderColor: '#e5e7eb',
  },
  milestoneOptionSelected: {
    backgroundColor: '#ffedd5',
    borderColor: '#ea580c',
  },
  milestoneOptionText: {
    fontSize: 12,
    color: '#4b5563',
    fontWeight: '500',
  },
  milestoneOptionTextSelected: {
    color: '#9a3412',
  },
  formActions: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    marginTop: 24,
  },
  button: {
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 6,
    marginLeft: 12,
    minWidth: 100,
    alignItems: 'center',
  },
  cancelButton: {
    backgroundColor: '#f3f4f6',
  },
  saveButton: {
    backgroundColor: '#ea580c',
  },
  cancelButtonText: {
    color: '#4b5563',
    fontWeight: '500',
  },
  saveButtonText: {
    color: '#fff',
    fontWeight: '500',
  },
});

export default TransactionTemplates;
