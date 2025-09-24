import React from 'react';
import { Pressable, PressableProps, StyleProp, StyleSheet, Text, TextStyle, ViewStyle } from 'react-native';
import { useTheme } from '../../theme/ThemeProvider';

type ButtonVariant = 'primary' | 'secondary' | 'ghost';

type ButtonSize = 'sm' | 'md' | 'lg';

interface ButtonProps extends PressableProps {
  label: string;
  variant?: ButtonVariant;
  size?: ButtonSize;
  textStyle?: StyleProp<TextStyle>;
  style?: StyleProp<ViewStyle>;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  variant = 'primary',
  size = 'md',
  textStyle,
  style,
  ...rest
}) => {
  const theme = useTheme();

  const { containerStyle, labelStyle } = getVariantStyles(theme, variant, size);

  return (
    <Pressable style={[containerStyle, style]} {...rest}>
      <Text style={[labelStyle, textStyle]}>{label}</Text>
    </Pressable>
  );
};

const getVariantStyles = (theme: ReturnType<typeof useTheme>, variant: ButtonVariant, size: ButtonSize) => {
  const baseContainer: ViewStyle = {
    borderRadius: 999,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: theme.spacing.lg,
  };

  const baseLabel: TextStyle = {
    fontWeight: '600',
    color: theme.colors.text,
  };

  switch (size) {
    case 'sm':
      baseContainer.paddingVertical = theme.spacing.sm;
      baseLabel.fontSize = 14;
      break;
    case 'lg':
      baseContainer.paddingVertical = theme.spacing.xl;
      baseLabel.fontSize = 18;
      break;
    case 'md':
    default:
      baseContainer.paddingVertical = theme.spacing.md;
      baseLabel.fontSize = 16;
      break;
  }

  const containerStyle: ViewStyle = { ...baseContainer };
  const labelStyle: TextStyle = { ...baseLabel };

  switch (variant) {
    case 'secondary':
      containerStyle.backgroundColor = theme.colors.secondary;
      labelStyle.color = theme.colors.surface;
      break;
    case 'ghost':
      containerStyle.backgroundColor = 'transparent';
      containerStyle.borderWidth = 1;
      containerStyle.borderColor = theme.colors.border;
      labelStyle.color = theme.colors.text;
      break;
    case 'primary':
    default:
      containerStyle.backgroundColor = theme.colors.primary;
      labelStyle.color = theme.colors.surface;
      break;
  }

  return {
    containerStyle,
    labelStyle,
  };
};

const styles = StyleSheet.create({});

export default Button;
