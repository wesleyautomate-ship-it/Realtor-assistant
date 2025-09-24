import React, { ReactNode } from 'react';
import {
  Image,
  Pressable,
  StyleProp,
  StyleSheet,
  Text,
  View,
  ViewStyle,
} from 'react-native';
import { useTheme } from '../../theme/ThemeProvider';

type HeaderAction = {
  id: string;
  icon?: ReactNode;
  onPress: () => void;
  accessibilityLabel?: string;
  style?: StyleProp<ViewStyle>;
};

interface HeaderProps {
  title: string;
  subtitle?: string;
  onBack?: () => void;
  actions?: HeaderAction[];
  avatarUrl?: string;
}

export const Header: React.FC<HeaderProps> = ({
  title,
  subtitle,
  onBack,
  actions,
  avatarUrl,
}) => {
  const theme = useTheme();
  const styles = useStyles(theme);
  const resolvedActions: HeaderAction[] = Array.isArray(actions) ? actions : [];

  return (
    <View style={styles.container}>
      <View style={styles.leftSection}>
        {onBack && (
          <Pressable
            accessibilityRole="button"
            accessibilityLabel="Go back"
            onPress={onBack}
            style={styles.backButton}
          >
            <Text style={styles.backButtonLabel}>{'‹'}</Text>
          </Pressable>
        )}
        <View>
          <Text style={styles.title}>{title}</Text>
          {subtitle ? <Text style={styles.subtitle}>{subtitle}</Text> : null}
        </View>
      </View>

      <View style={styles.rightSection}>
        {resolvedActions.map((action) => (
          <Pressable
            key={action.id}
            onPress={action.onPress}
            accessibilityRole="button"
            accessibilityLabel={action.accessibilityLabel || action.id}
            style={[styles.actionButton, action.style]}
          >
            {action.icon || <Text style={styles.actionFallback}>•</Text>}
          </Pressable>
        ))}

        {avatarUrl ? (
          <Image
            accessibilityRole="image"
            source={{ uri: avatarUrl }}
            style={styles.avatar}
          />
        ) : null}
      </View>
    </View>
  );
};

const useStyles = (theme: ReturnType<typeof useTheme>) =>
  StyleSheet.create({
    container: {
      paddingTop: theme.spacing.xxl,
      paddingBottom: theme.spacing.lg,
      paddingHorizontal: theme.spacing.lg,
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-between',
      backgroundColor: theme.colors.background,
    },
    leftSection: {
      flexDirection: 'row',
      alignItems: 'center',
      gap: theme.spacing.md,
    },
    rightSection: {
      flexDirection: 'row',
      alignItems: 'center',
      gap: theme.spacing.md,
    },
    title: {
      ...theme.typography.h2,
      color: theme.colors.text,
    },
    subtitle: {
      marginTop: theme.spacing.xs,
      color: theme.colors.textSecondary,
      fontSize: 14,
      lineHeight: 20,
    },
    backButton: {
      width: 40,
      height: 40,
      borderRadius: 20,
      backgroundColor: theme.colors.surface,
      alignItems: 'center',
      justifyContent: 'center',
      borderWidth: 1,
      borderColor: theme.colors.border,
      shadowColor: theme.colors.overlay,
      shadowOpacity: 0.1,
      shadowRadius: 6,
      shadowOffset: { width: 0, height: 3 },
      elevation: 2,
    },
    backButtonLabel: {
      fontSize: 24,
      color: theme.colors.text,
    },
    actionButton: {
      width: 40,
      height: 40,
      borderRadius: 12,
      backgroundColor: theme.colors.surface,
      borderWidth: 1,
      borderColor: theme.colors.border,
      alignItems: 'center',
      justifyContent: 'center',
    },
    actionFallback: {
      color: theme.colors.text,
      fontSize: 18,
      fontWeight: '600',
    },
    avatar: {
      width: 44,
      height: 44,
      borderRadius: 22,
      borderWidth: 2,
      borderColor: theme.colors.surface,
      backgroundColor: theme.colors.surfaceMuted,
    },
  });

export default Header;
