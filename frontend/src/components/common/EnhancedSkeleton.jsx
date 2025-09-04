import React from 'react';
import {
  Skeleton,
  Box,
  Card,
  CardContent,
  Grid,
  useTheme,
  Fade,
} from '@mui/material';
import { 
  PRIORITY_COLORS, 
  SPACING_SCALE, 
  BORDER_RADIUS, 
  TRANSITIONS 
} from '../../theme/designSystem';

// Enhanced Skeleton Components for consistent loading states

export const CardSkeleton = ({ 
  height = 200, 
  showHeader = true, 
  showContent = true,
  showActions = false,
  variant = 'rectangular',
  animation = 'pulse',
  ...props 
}) => {
  const theme = useTheme();
  
  return (
    <Fade in timeout={300}>
      <Card 
        sx={{ 
          height,
          borderRadius: BORDER_RADIUS.lg,
          boxShadow: theme.shadows[1],
          overflow: 'hidden',
          ...props.sx 
        }}
        {...props}
      >
        {showHeader && (
          <Box sx={{ p: 2, borderBottom: `1px solid ${theme.palette.divider}` }}>
            <Skeleton 
              variant="text" 
              width="60%" 
              height={32}
              animation={animation}
              sx={{ 
                borderRadius: BORDER_RADIUS.sm,
                bgcolor: theme.palette.grey[200]
              }}
            />
            <Skeleton 
              variant="text" 
              width="40%" 
              height={20}
              animation={animation}
              sx={{ 
                mt: 1,
                borderRadius: BORDER_RADIUS.sm,
                bgcolor: theme.palette.grey[100]
              }}
            />
          </Box>
        )}
        
        {showContent && (
          <CardContent sx={{ p: 2 }}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Skeleton 
                  variant="text" 
                  width="80%" 
                  height={24}
                  animation={animation}
                  sx={{ 
                    borderRadius: BORDER_RADIUS.sm,
                    bgcolor: theme.palette.grey[200]
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <Skeleton 
                  variant="text" 
                  width="60%" 
                  height={20}
                  animation={animation}
                  sx={{ 
                    borderRadius: BORDER_RADIUS.sm,
                    bgcolor: theme.palette.grey[100]
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <Skeleton 
                  variant="text" 
                  width="70%" 
                  height={20}
                  animation={animation}
                  sx={{ 
                    borderRadius: BORDER_RADIUS.sm,
                    bgcolor: theme.palette.grey[100]
                  }}
                />
              </Grid>
            </Grid>
          </CardContent>
        )}
        
        {showActions && (
          <Box sx={{ p: 2, borderTop: `1px solid ${theme.palette.divider}` }}>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Skeleton 
                variant="rectangular" 
                width={80} 
                height={36}
                animation={animation}
                sx={{ 
                  borderRadius: BORDER_RADIUS.md,
                  bgcolor: theme.palette.grey[200]
                }}
              />
              <Skeleton 
                variant="rectangular" 
                width={80} 
                height={36}
                animation={animation}
                sx={{ 
                  borderRadius: BORDER_RADIUS.md,
                  bgcolor: theme.palette.grey[200]
                }}
              />
            </Box>
          </Box>
        )}
      </Card>
    </Fade>
  );
};

export const ListItemSkeleton = ({ 
  showAvatar = true, 
  showContent = true,
  showActions = false,
  height = 72,
  animation = 'pulse',
  ...props 
}) => {
  const theme = useTheme();
  
  return (
    <Fade in timeout={200}>
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          p: 2,
          height,
          borderRadius: BORDER_RADIUS.md,
          border: `1px solid ${theme.palette.divider}`,
          bgcolor: theme.palette.background.paper,
          ...props.sx
        }}
        {...props}
      >
        {showAvatar && (
          <Box sx={{ mr: 2 }}>
            <Skeleton 
              variant="circular" 
              width={40} 
              height={40}
              animation={animation}
              sx={{ bgcolor: theme.palette.grey[200] }}
            />
          </Box>
        )}
        
        {showContent && (
          <Box sx={{ flex: 1 }}>
            <Skeleton 
              variant="text" 
              width="70%" 
              height={24}
              animation={animation}
              sx={{ 
                borderRadius: BORDER_RADIUS.sm,
                bgcolor: theme.palette.grey[200]
              }}
            />
            <Skeleton 
              variant="text" 
              width="50%" 
              height={20}
              animation={animation}
              sx={{ 
                mt: 1,
                borderRadius: BORDER_RADIUS.sm,
                bgcolor: theme.palette.grey[100]
              }}
            />
          </Box>
        )}
        
        {showActions && (
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Skeleton 
              variant="circular" 
              width={32} 
              height={32}
              animation={animation}
              sx={{ bgcolor: theme.palette.grey[200] }}
            />
            <Skeleton 
              variant="circular" 
              width={32} 
              height={32}
              animation={animation}
              sx={{ bgcolor: theme.palette.grey[200] }}
            />
          </Box>
        )}
      </Box>
    </Fade>
  );
};

export const TableSkeleton = ({ 
  rows = 5, 
  columns = 4,
  showHeader = true,
  animation = 'pulse',
  ...props 
}) => {
  const theme = useTheme();
  
  return (
    <Fade in timeout={400}>
      <Box
        sx={{
          borderRadius: BORDER_RADIUS.lg,
          border: `1px solid ${theme.palette.divider}`,
          overflow: 'hidden',
          ...props.sx
        }}
        {...props}
      >
        {showHeader && (
          <Box sx={{ 
            p: 2, 
            bgcolor: theme.palette.grey[50],
            borderBottom: `1px solid ${theme.palette.divider}` 
          }}>
            <Grid container spacing={2}>
              {Array.from({ length: columns }).map((_, index) => (
                <Grid item xs key={index}>
                  <Skeleton 
                    variant="text" 
                    width="80%" 
                    height={24}
                    animation={animation}
                    sx={{ 
                      borderRadius: BORDER_RADIUS.sm,
                      bgcolor: theme.palette.grey[200]
                    }}
                  />
                </Grid>
              ))}
            </Grid>
          </Box>
        )}
        
        <Box>
          {Array.from({ length: rows }).map((_, rowIndex) => (
            <Box
              key={rowIndex}
              sx={{
                p: 2,
                borderBottom: rowIndex < rows - 1 ? `1px solid ${theme.palette.divider}` : 'none',
                '&:hover': {
                  bgcolor: theme.palette.action.hover,
                },
                transition: TRANSITIONS.fast,
              }}
            >
              <Grid container spacing={2}>
                {Array.from({ length: columns }).map((_, colIndex) => (
                  <Grid item xs key={colIndex}>
                    <Skeleton 
                      variant="text" 
                      width={colIndex === 0 ? "60%" : "80%"} 
                      height={20}
                      animation={animation}
                      sx={{ 
                        borderRadius: BORDER_RADIUS.sm,
                        bgcolor: theme.palette.grey[100]
                      }}
                    />
                  </Grid>
                ))}
              </Grid>
            </Box>
          ))}
        </Box>
      </Box>
    </Fade>
  );
};

export const DashboardSkeleton = ({ 
  showWidgets = true,
  showInsights = true,
  animation = 'pulse',
  ...props 
}) => {
  const theme = useTheme();
  
  return (
    <Fade in timeout={500}>
      <Box sx={{ p: 3, ...props.sx }} {...props}>
        {/* Header Skeleton */}
        <Box sx={{ mb: 4 }}>
          <Skeleton 
            variant="text" 
            width="40%" 
            height={48}
            animation={animation}
            sx={{ 
              borderRadius: BORDER_RADIUS.sm,
              bgcolor: theme.palette.grey[200]
            }}
          />
          <Skeleton 
            variant="text" 
            width="60%" 
            height={24}
            animation={animation}
            sx={{ 
              mt: 1,
              borderRadius: BORDER_RADIUS.sm,
              bgcolor: theme.palette.grey[100]
            }}
          />
        </Box>
        
        {/* Widgets Grid Skeleton */}
        {showWidgets && (
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} lg={6}>
              <CardSkeleton 
                height={300}
                showHeader={true}
                showContent={true}
                showActions={false}
                animation={animation}
              />
            </Grid>
            <Grid item xs={12} lg={6}>
              <CardSkeleton 
                height={300}
                showHeader={true}
                showContent={true}
                showActions={false}
                animation={animation}
              />
            </Grid>
          </Grid>
        )}
        
        {/* Insights Panel Skeleton */}
        {showInsights && (
          <CardSkeleton 
            height={400}
            showHeader={true}
            showContent={true}
            showActions={true}
            animation={animation}
          />
        )}
      </Box>
    </Fade>
  );
};

export const ChatSkeleton = ({ 
  messages = 3,
  animation = 'pulse',
  ...props 
}) => {
  const theme = useTheme();
  
  return (
    <Fade in timeout={300}>
      <Box sx={{ p: 2, ...props.sx }} {...props}>
        {Array.from({ length: messages }).map((_, index) => (
          <Box
            key={index}
            sx={{
              display: 'flex',
              mb: 3,
              justifyContent: index % 2 === 0 ? 'flex-start' : 'flex-end',
            }}
          >
            <Box
              sx={{
                maxWidth: '70%',
                display: 'flex',
                flexDirection: 'column',
                alignItems: index % 2 === 0 ? 'flex-start' : 'flex-end',
              }}
            >
              {index % 2 === 0 && (
                <Skeleton 
                  variant="circular" 
                  width={32} 
                  height={32}
                  animation={animation}
                  sx={{ 
                    mb: 1,
                    bgcolor: theme.palette.grey[200]
                  }}
                />
              )}
              
              <Box
                sx={{
                  p: 2,
                  borderRadius: BORDER_RADIUS.lg,
                  bgcolor: index % 2 === 0 
                    ? theme.palette.grey[100] 
                    : theme.palette.primary.light,
                  color: index % 2 === 0 
                    ? theme.palette.text.primary 
                    : theme.palette.primary.contrastText,
                }}
              >
                <Skeleton 
                  variant="text" 
                  width={Math.random() * 60 + 40 + '%'} 
                  height={20}
                  animation={animation}
                  sx={{ 
                    borderRadius: BORDER_RADIUS.sm,
                    bgcolor: index % 2 === 0 
                      ? theme.palette.grey[300]
                      : theme.palette.primary.main,
                  }}
                />
                <Skeleton 
                  variant="text" 
                  width={Math.random() * 40 + 30 + '%'} 
                  height={20}
                  animation={animation}
                  sx={{ 
                    mt: 1,
                    borderRadius: BORDER_RADIUS.sm,
                    bgcolor: index % 2 === 0 
                      ? theme.palette.grey[300]
                      : theme.palette.primary.main,
                  }}
                />
              </Box>
            </Box>
          </Box>
        ))}
      </Box>
    </Fade>
  );
};

// Export all skeleton components
export default {
  CardSkeleton,
  ListItemSkeleton,
  TableSkeleton,
  DashboardSkeleton,
  ChatSkeleton,
};
