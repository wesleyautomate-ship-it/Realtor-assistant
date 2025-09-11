import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  LinearProgress,
  Avatar,
  AvatarGroup,
  useTheme,
  Tooltip,
  Fade
} from '@mui/material';
import {
  MoreVert as MoreVertIcon,
  OpenInNew as OpenIcon,
  ContentCopy as DuplicateIcon,
  Cancel as CancelIcon,
  Schedule as ScheduleIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  AccessTime as TimeIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';

const RequestCard = ({ request, onDuplicate, onCancel }) => {
  const theme = useTheme();
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = useState(null);
  const [isHovered, setIsHovered] = useState(false);

  const handleMenuOpen = (event) => {
    event.stopPropagation();
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleCardClick = () => {
    navigate(`/requests/${request.id}`);
  };

  const handleOpen = () => {
    handleCardClick();
    handleMenuClose();
  };

  const handleDuplicate = () => {
    onDuplicate?.(request);
    handleMenuClose();
  };

  const handleCancel = () => {
    onCancel?.(request);
    handleMenuClose();
  };

  const getStatusColor = (status) => {
    const colors = {
      queued: 'default',
      planning: 'info',
      generating: 'primary',
      validating: 'warning',
      draft_ready: 'success',
      needs_info: 'warning',
      approved: 'success',
      delivered: 'success',
      failed: 'error'
    };
    return colors[status] || 'default';
  };

  const getStatusIcon = (status) => {
    const icons = {
      queued: <TimeIcon />,
      planning: <TimeIcon />,
      generating: <TimeIcon />,
      validating: <TimeIcon />,
      draft_ready: <CheckIcon />,
      needs_info: <ErrorIcon />,
      approved: <CheckIcon />,
      delivered: <CheckIcon />,
      failed: <ErrorIcon />
    };
    return icons[status] || <TimeIcon />;
  };

  const getTeamColor = (team) => {
    const colors = {
      marketing: '#E91E63',
      analytics: '#9C27B0',
      social: '#FF9800',
      strategy: '#4CAF50',
      packages: '#2E7D32',
      transactions: '#673AB7'
    };
    return colors[team] || theme.palette.primary.main;
  };

  const formatETA = (eta) => {
    if (!eta) return 'TBD';
    const now = new Date();
    const etaDate = new Date(eta);
    const diff = etaDate - now;
    
    if (diff < 0) return 'Overdue';
    if (diff < 60000) return 'Any moment';
    if (diff < 3600000) return `${Math.ceil(diff / 60000)}m`;
    if (diff < 86400000) return `${Math.ceil(diff / 3600000)}h`;
    return `${Math.ceil(diff / 86400000)}d`;
  };

  const getProgressValue = (status) => {
    const progressMap = {
      queued: 10,
      planning: 25,
      generating: 50,
      validating: 75,
      draft_ready: 90,
      needs_info: 60,
      approved: 100,
      delivered: 100,
      failed: 0
    };
    return progressMap[status] || 0;
  };

  return (
    <Fade in timeout={300}>
      <Card
        sx={{
          height: '100%',
          cursor: 'pointer',
          transition: 'all 0.3s ease-in-out',
          border: `1px solid ${theme.palette.divider}`,
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: theme.shadows[4],
            border: `1px solid ${getTeamColor(request.team)}`,
          },
          minHeight: 200
        }}
        onClick={handleCardClick}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        <CardContent sx={{ p: 2.5, height: '100%', display: 'flex', flexDirection: 'column' }}>
          {/* Header */}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
            <Box sx={{ flex: 1, minWidth: 0 }}>
              <Chip
                label={request.team?.toUpperCase() || 'GENERAL'}
                size="small"
                sx={{
                  backgroundColor: getTeamColor(request.team),
                  color: 'white',
                  fontWeight: 600,
                  fontSize: '0.7rem',
                  mb: 1
                }}
              />
              <Typography
                variant="body2"
                sx={{
                  color: 'text.secondary',
                  fontSize: '0.75rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 0.5
                }}
              >
                <ScheduleIcon sx={{ fontSize: 14 }} />
                {formatDistanceToNow(new Date(request.created_at), { addSuffix: true })}
              </Typography>
            </Box>
            
            <IconButton
              size="small"
              onClick={handleMenuOpen}
              sx={{
                opacity: isHovered ? 1 : 0.7,
                transition: 'opacity 0.2s ease-in-out'
              }}
            >
              <MoreVertIcon />
            </IconButton>
          </Box>

          {/* Title */}
          <Typography
            variant="h6"
            sx={{
              fontWeight: 600,
              mb: 1,
              color: 'text.primary',
              fontSize: '1rem',
              lineHeight: 1.3,
              display: '-webkit-box',
              WebkitLineClamp: 2,
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              minHeight: '2.6em'
            }}
          >
            {request.title}
          </Typography>

          {/* Description */}
          <Typography
            variant="body2"
            sx={{
              color: 'text.secondary',
              mb: 2,
              fontSize: '0.875rem',
              lineHeight: 1.4,
              display: '-webkit-box',
              WebkitLineClamp: 2,
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              flex: 1
            }}
          >
            {request.description}
          </Typography>

          {/* Progress Bar */}
          <Box sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 0.5 }}>
              <Typography variant="caption" sx={{ color: 'text.secondary', fontSize: '0.75rem' }}>
                {request.status?.replace('_', ' ').toUpperCase()}
              </Typography>
              <Typography variant="caption" sx={{ color: 'text.secondary', fontSize: '0.75rem' }}>
                {getProgressValue(request.status)}%
              </Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={getProgressValue(request.status)}
              sx={{
                height: 6,
                borderRadius: 3,
                backgroundColor: theme.palette.grey[200],
                '& .MuiLinearProgress-bar': {
                  backgroundColor: getStatusColor(request.status) === 'success' 
                    ? theme.palette.success.main 
                    : getTeamColor(request.team),
                  borderRadius: 3,
                }
              }}
            />
          </Box>

          {/* Footer */}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <AvatarGroup max={3} sx={{ '& .MuiAvatar-root': { width: 24, height: 24, fontSize: '0.75rem' } }}>
                {request.assignees?.map((assignee, index) => (
                  <Avatar
                    key={index}
                    sx={{
                      bgcolor: getTeamColor(request.team),
                      fontSize: '0.75rem',
                      fontWeight: 600
                    }}
                  >
                    {assignee.name?.split(' ').map(n => n[0]).join('') || 'U'}
                  </Avatar>
                ))}
              </AvatarGroup>
              {request.assignees?.length > 3 && (
                <Typography variant="caption" sx={{ color: 'text.secondary', fontSize: '0.75rem' }}>
                  +{request.assignees.length - 3}
                </Typography>
              )}
            </Box>

            <Chip
              label={`ETA: ${formatETA(request.eta)}`}
              size="small"
              color={getStatusColor(request.status)}
              icon={getStatusIcon(request.status)}
              sx={{
                fontSize: '0.7rem',
                height: 24,
                '& .MuiChip-icon': {
                  fontSize: 14
                }
              }}
            />
          </Box>
        </CardContent>

        {/* Context Menu */}
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'right',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'right',
          }}
          PaperProps={{
            sx: {
              minWidth: 160,
              boxShadow: theme.shadows[8],
              borderRadius: 2,
            }
          }}
        >
          <MenuItem onClick={handleOpen}>
            <OpenIcon sx={{ mr: 2, fontSize: 20 }} />
            Open
          </MenuItem>
          <MenuItem onClick={handleDuplicate}>
            <DuplicateIcon sx={{ mr: 2, fontSize: 20 }} />
            Duplicate
          </MenuItem>
          {request.status !== 'delivered' && request.status !== 'failed' && (
            <MenuItem onClick={handleCancel} sx={{ color: 'error.main' }}>
              <CancelIcon sx={{ mr: 2, fontSize: 20 }} />
              Cancel
            </MenuItem>
          )}
        </Menu>
      </Card>
    </Fade>
  );
};

export default RequestCard;
