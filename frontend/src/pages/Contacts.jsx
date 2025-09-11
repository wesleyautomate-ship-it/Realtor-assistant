import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Avatar,
  TextField,
  InputAdornment,
  Chip,
  Stack,
  Grid,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  useTheme,
  useMediaQuery,
  Paper,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  ListItemSecondaryAction,
  Divider,
  Snackbar,
} from '@mui/material';
import {
  Search as SearchIcon,
  Add as AddIcon,
  Phone as PhoneIcon,
  Email as EmailIcon,
  LocationOn as LocationIcon,
  Business as BusinessIcon,
  FilterList as FilterIcon,
  MoreVert as MoreVertIcon,
  Star as StarIcon,
  StarBorder as StarBorderIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { api } from '../utils/apiClient';

const Contacts = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const navigate = useNavigate();
  const { currentUser } = useAppContext();
  
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');
  const [addContactOpen, setAddContactOpen] = useState(false);
  const [selectedContact, setSelectedContact] = useState(null);
  const [nurturingCampaigns, setNurturingCampaigns] = useState([]);
  const [automatedFollowUps, setAutomatedFollowUps] = useState([]);
  const [leadScoring, setLeadScoring] = useState({});
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  
  // Mock data - in real app, this would come from your backend
  const [contacts, setContacts] = useState([
    {
      id: 1,
      name: 'Ahmed Al-Rashid',
      email: 'ahmed@email.com',
      phone: '+971 50 123 4567',
      company: 'Al-Rashid Properties',
      location: 'Dubai Marina',
      type: 'client',
      status: 'active',
      lastContact: '2024-01-15',
      isFavorite: true,
      avatar: null,
    },
    {
      id: 2,
      name: 'Sarah Johnson',
      email: 'sarah.j@email.com',
      phone: '+971 55 987 6543',
      company: 'Johnson Investments',
      location: 'Palm Jumeirah',
      type: 'client',
      status: 'hot',
      lastContact: '2024-01-14',
      isFavorite: false,
      avatar: null,
    },
    {
      id: 3,
      name: 'Mohammed Hassan',
      email: 'm.hassan@email.com',
      phone: '+971 52 456 7890',
      company: 'Hassan Real Estate',
      location: 'Downtown Dubai',
      type: 'partner',
      status: 'active',
      lastContact: '2024-01-13',
      isFavorite: true,
      avatar: null,
    },
    {
      id: 4,
      name: 'Emma Thompson',
      email: 'emma.t@email.com',
      phone: '+971 56 789 0123',
      company: 'Thompson Holdings',
      location: 'Business Bay',
      type: 'client',
      status: 'warm',
      lastContact: '2024-01-12',
      isFavorite: false,
      avatar: null,
    },
  ]);

  const filters = [
    { id: 'all', label: 'All Contacts', count: contacts.length },
    { id: 'client', label: 'Clients', count: contacts.filter(c => c.type === 'client').length },
    { id: 'partner', label: 'Partners', count: contacts.filter(c => c.type === 'partner').length },
    { id: 'favorites', label: 'Favorites', count: contacts.filter(c => c.isFavorite).length },
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'hot': return 'error';
      case 'warm': return 'warning';
      case 'active': return 'success';
      default: return 'default';
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'client': return 'primary';
      case 'partner': return 'secondary';
      default: return 'default';
    }
  };

  const filteredContacts = contacts.filter(contact => {
    const matchesSearch = contact.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         contact.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         contact.company.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFilter = filter === 'all' || 
                         (filter === 'favorites' ? contact.isFavorite : contact.type === filter);
    
    return matchesSearch && matchesFilter;
  });

  const handleToggleFavorite = (contactId) => {
    setContacts(prev => prev.map(contact => 
      contact.id === contactId 
        ? { ...contact, isFavorite: !contact.isFavorite }
        : contact
    ));
  };

  const handleContactClick = (contact) => {
    setSelectedContact(contact);
    // Navigate to contact details or open modal
    console.log('Contact clicked:', contact);
  };

  const loadLeadNurturingData = async () => {
    try {
      // Load nurturing campaigns
      const campaigns = await api.getLeadNurturingCampaigns();
      setNurturingCampaigns(campaigns);

      // Load automated follow-ups
      const followUps = await api.getAutomatedFollowUps();
      setAutomatedFollowUps(followUps);

      // Load lead scoring for each contact
      const scoringPromises = contacts.map(contact => 
        api.getLeadScoring(contact.id).catch(() => ({ contactId: contact.id, score: 0 }))
      );
      const scoringResults = await Promise.all(scoringPromises);
      const scoringMap = {};
      scoringResults.forEach(result => {
        scoringMap[result.contactId] = result.score;
      });
      setLeadScoring(scoringMap);

    } catch (error) {
      console.error('Error loading lead nurturing data:', error);
    }
  };

  const handleScheduleFollowUp = async (contactId, followUpData) => {
    try {
      await api.scheduleFollowUp(contactId, followUpData);
      setSnackbar({
        open: true,
        message: 'Follow-up scheduled successfully!',
        severity: 'success'
      });
      // Refresh data
      loadLeadNurturingData();
    } catch (error) {
      console.error('Error scheduling follow-up:', error);
      setSnackbar({
        open: true,
        message: 'Failed to schedule follow-up',
        severity: 'error'
      });
    }
  };

  useEffect(() => {
    loadLeadNurturingData();
  }, [contacts]);

  return (
    <Box sx={{ 
      minHeight: '100vh', 
      bgcolor: 'background.default',
      pb: isMobile ? 8 : 4
    }}>
      {/* Header */}
      <Box sx={{ 
        p: 3, 
        background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
        color: 'white'
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            Contacts
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setAddContactOpen(true)}
            sx={{
              bgcolor: 'rgba(255,255,255,0.2)',
              color: 'white',
              '&:hover': {
                bgcolor: 'rgba(255,255,255,0.3)',
              },
              borderRadius: 2,
            }}
          >
            Add Contact
          </Button>
        </Box>
        
        <Typography variant="body1" sx={{ opacity: 0.9 }}>
          Manage your clients and business partners
        </Typography>
      </Box>

      {/* Search and Filters */}
      <Box sx={{ p: 2 }}>
        <TextField
          fullWidth
          placeholder="Search contacts..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          sx={{
            mb: 2,
            '& .MuiOutlinedInput-root': {
              borderRadius: 3,
            },
          }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
        />

        {/* Filter Chips */}
        <Stack 
          direction="row" 
          spacing={1} 
          sx={{ 
            mb: 3, 
            flexWrap: 'wrap', 
            gap: 1,
            justifyContent: isMobile ? 'center' : 'flex-start'
          }}
        >
          {filters.map((filterOption) => (
            <Chip
              key={filterOption.id}
              label={`${filterOption.label} (${filterOption.count})`}
              onClick={() => setFilter(filterOption.id)}
              variant={filter === filterOption.id ? 'filled' : 'outlined'}
              color={filter === filterOption.id ? 'primary' : 'default'}
              size="small"
            />
          ))}
        </Stack>

        {/* Contacts List */}
        <Paper sx={{ borderRadius: 3, overflow: 'hidden' }}>
          <List>
            {filteredContacts.map((contact, index) => (
              <React.Fragment key={contact.id}>
                <ListItem
                  sx={{
                    cursor: 'pointer',
                    '&:hover': {
                      bgcolor: 'grey.50',
                    },
                  }}
                  onClick={() => handleContactClick(contact)}
                >
                  <ListItemAvatar>
                    <Avatar
                      sx={{
                        bgcolor: 'primary.main',
                        width: 48,
                        height: 48,
                      }}
                    >
                      {contact.name.split(' ').map(n => n[0]).join('')}
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          {contact.name}
                        </Typography>
                        <Chip
                          label={contact.type}
                          size="small"
                          color={getTypeColor(contact.type)}
                          variant="outlined"
                        />
                        <Chip
                          label={contact.status}
                          size="small"
                          color={getStatusColor(contact.status)}
                          variant="filled"
                        />
                      </Box>
                    }
                    secondary={
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          {contact.company} • {contact.location}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Last contact: {contact.lastContact}
                        </Typography>
                      </Box>
                    }
                  />
                  <ListItemSecondaryAction>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <IconButton
                        onClick={(e) => {
                          e.stopPropagation();
                          handleToggleFavorite(contact.id);
                        }}
                        size="small"
                      >
                        {contact.isFavorite ? (
                          <StarIcon sx={{ color: 'warning.main' }} />
                        ) : (
                          <StarBorderIcon />
                        )}
                      </IconButton>
                      <IconButton size="small">
                        <MoreVertIcon />
                      </IconButton>
                    </Box>
                  </ListItemSecondaryAction>
                </ListItem>
                {index < filteredContacts.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </Paper>

        {filteredContacts.length === 0 && (
          <Paper
            sx={{
              textAlign: 'center',
              py: 6,
              px: 3,
              borderRadius: 3,
              border: `2px dashed ${theme.palette.divider}`,
              bgcolor: 'background.paper'
            }}
          >
            <BusinessIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" sx={{ mb: 1, color: 'text.secondary' }}>
              No contacts found
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary', mb: 3 }}>
              {searchTerm ? 'Try adjusting your search terms' : 'Add your first contact to get started'}
            </Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => setAddContactOpen(true)}
              sx={{ borderRadius: 2 }}
            >
              Add Contact
            </Button>
          </Paper>
        )}
      </Box>

      {/* Add Contact Dialog */}
      <Dialog
        open={addContactOpen}
        onClose={() => setAddContactOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Add New Contact</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            This feature will be implemented to integrate with your backend contact management system.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAddContactOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={() => setAddContactOpen(false)}>
            Add Contact
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        message={snackbar.message}
        severity={snackbar.severity}
      />
    </Box>
  );
};

export default Contacts;
