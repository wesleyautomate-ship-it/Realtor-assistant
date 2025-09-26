import React, { useState } from 'react';
import { View, Text, TextInput, StyleSheet, TouchableOpacity, ActivityIndicator } from 'react-native';

export interface PropertyFormValues {
  title: string;
  price?: number;
  beds?: number;
  baths?: number;
  sqft?: number;
  imageUrl?: string;
}

export interface PropertyFormProps {
  initial?: PropertyFormValues;
  submitting?: boolean;
  onSubmit: (values: PropertyFormValues) => void;
  onCancel?: () => void;
}

export default function PropertyForm({ initial, submitting, onSubmit, onCancel }: PropertyFormProps) {
  const [title, setTitle] = useState(initial?.title ?? '');
  const [price, setPrice] = useState(initial?.price?.toString() ?? '');
  const [beds, setBeds] = useState(initial?.beds?.toString() ?? '');
  const [baths, setBaths] = useState(initial?.baths?.toString() ?? '');
  const [sqft, setSqft] = useState(initial?.sqft?.toString() ?? '');
  const [imageUrl, setImageUrl] = useState(initial?.imageUrl ?? '');

  const handleSubmit = () => {
    onSubmit({
      title: title.trim(),
      price: price ? Number(price) : undefined,
      beds: beds ? Number(beds) : undefined,
      baths: baths ? Number(baths) : undefined,
      sqft: sqft ? Number(sqft) : undefined,
      imageUrl: imageUrl || undefined,
    });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Property Details</Text>
      <TextInput style={styles.input} placeholder="Title" value={title} onChangeText={setTitle} />
      <TextInput style={styles.input} placeholder="Price (USD)" keyboardType="numeric" value={price} onChangeText={setPrice} />
      <View style={styles.row}>
        <TextInput style={[styles.input, styles.rowItem]} placeholder="Beds" keyboardType="numeric" value={beds} onChangeText={setBeds} />
        <TextInput style={[styles.input, styles.rowItem]} placeholder="Baths" keyboardType="numeric" value={baths} onChangeText={setBaths} />
      </View>
      <TextInput style={styles.input} placeholder="Square Feet" keyboardType="numeric" value={sqft} onChangeText={setSqft} />
      <TextInput style={styles.input} placeholder="Image URL" value={imageUrl} onChangeText={setImageUrl} />

      <View style={styles.actions}>
        {!!onCancel && (
          <TouchableOpacity style={[styles.btn, styles.cancel]} onPress={onCancel} disabled={submitting}>
            <Text style={styles.btnText}>Cancel</Text>
          </TouchableOpacity>
        )}
        <TouchableOpacity style={[styles.btn, styles.submit]} onPress={handleSubmit} disabled={submitting || !title.trim()}>
          {submitting ? <ActivityIndicator color="#fff" /> : <Text style={styles.btnText}>Save</Text>}
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { backgroundColor: '#fff', borderRadius: 12, padding: 12, borderWidth: 1, borderColor: '#E5E7EB' },
  header: { fontSize: 16, fontWeight: '700', marginBottom: 8, color: '#111827' },
  input: { backgroundColor: '#fff', borderColor: '#93C5FD', borderWidth: 1, borderRadius: 10, paddingHorizontal: 12, paddingVertical: 10, marginBottom: 10 },
  row: { flexDirection: 'row', gap: 10 },
  rowItem: { flex: 1 },
  actions: { flexDirection: 'row', justifyContent: 'flex-end', gap: 10, marginTop: 6 },
  btn: { paddingHorizontal: 14, paddingVertical: 10, borderRadius: 10 },
  cancel: { backgroundColor: '#1f2937' },
  submit: { backgroundColor: '#2563eb' },
  btnText: { color: '#fff', fontWeight: '700' },
});


