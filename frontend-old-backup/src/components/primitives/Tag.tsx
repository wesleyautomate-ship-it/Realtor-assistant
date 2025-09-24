import React from 'react';
import { StyleProp, StyleSheet, Text, TextStyle, View, ViewStyle } from 'react-native';
import { useTheme } from '../../theme/ThemeProvider';

type TagTone = 'default' | 'success' | 'warning' | 'danger' | 'info';

interface TagProps {
  label: string;
  tone?: TagTone;
  style?: StyleProp<ViewStyle>;
  textStyle?: StyleProp<TextStyle>;
}

export const Tag: React.FC<TagProps> = ({ label, tone = 'default', style, textStyle }) => {
  const theme = useTheme();
  const { container, text } = getStyles(theme, tone);

  return (
    <View style={[container, style]}>
      <Text style={[text, textStyle]}>{label}</Text>
    </View>
  );
};

const getStyles = (theme: ReturnType<typeof useTheme>, tone: TagTone) => {
  const baseContainer: ViewStyle = {
    borderRadius: 999,
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.xs,
    alignSelf: 'flex-start',
  };

  const baseText: TextStyle = {
    fontSize: 12,
    fontWeight: '600',
  };

  switch (tone) {
    case 'success':
      return StyleSheet.create({
        container: {
          ...baseContainer,
          backgroundColor: theme.colors.success,
        },
        text: {
          ...baseText,
          color: theme.colors.surface,
        },
      });
    case 'warning':
      return StyleSheet.create({
        container: {
          ...baseContainer,
          backgroundColor: theme.colors.warning,
        },
        text: {
          ...baseText,
          color: theme.colors.surface,
        },
      });
    case 'danger':
      return StyleSheet.create({
        container: {
          ...baseContainer,
          backgroundColor: theme.colors.danger,
        },
        text: {
          ...baseText,
          color: theme.colors.surface,
        },
      });
    case 'info':
      return StyleSheet.create({
        container: {
          ...baseContainer,
          backgroundColor: theme.colors.accent,
        },
        text: {
          ...baseText,
          color: theme.colors.surface,
        },
      });
    case 'default':
    default:
      return StyleSheet.create({
        container: {
          ...baseContainer,
          backgroundColor: theme.colors.surfaceMuted,
        },
        text: {
          ...baseText,
          color: theme.colors.text,
        },
      });
  }
};

export default Tag;
