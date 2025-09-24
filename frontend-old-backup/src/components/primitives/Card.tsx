import React from 'react';
import { Pressable, PressableProps, StyleProp, StyleSheet, View, ViewProps, ViewStyle } from 'react-native';
import { useTheme } from '../../theme/ThemeProvider';

type CardVariant = 'elevated' | 'outlined' | 'flat';

interface CardProps extends ViewProps, Pick<PressableProps, 'onPress' | 'disabled'> {
  children: React.ReactNode;
  variant?: CardVariant;
  style?: StyleProp<ViewStyle>;
}

export const Card: React.FC<CardProps> = ({
  children,
  variant = 'elevated',
  style,
  onPress,
  disabled,
  ...rest
}) => {
  const theme = useTheme();
  const styles = useStyles(theme, variant);

  if (onPress) {
    return (
      <Pressable
        style={[styles.container, style]}
        onPress={onPress}
        disabled={disabled}
        {...rest}
      >
        {children}
      </Pressable>
    );
  }

  return (
    <View style={[styles.container, style]} {...rest}>
      {children}
    </View>
  );
};

const useStyles = (theme: ReturnType<typeof useTheme>, variant: CardVariant) => {
  const base: ViewStyle = {
    backgroundColor: theme.colors.surface,
    borderRadius: 16,
    padding: theme.spacing.lg,
  };

  switch (variant) {
    case 'outlined':
      return StyleSheet.create({
        container: {
          ...base,
          borderWidth: 1,
          borderColor: theme.colors.border,
        },
      });
    case 'flat':
      return StyleSheet.create({
        container: {
          ...base,
          backgroundColor: theme.colors.surfaceMuted,
        },
      });
    case 'elevated':
    default:
      return StyleSheet.create({
        container: {
          ...base,
          shadowColor: theme.colors.overlay,
          shadowOpacity: 0.15,
          shadowOffset: { width: 0, height: 8 },
          shadowRadius: 12,
          elevation: 6,
        },
      });
  }
};

export default Card;
