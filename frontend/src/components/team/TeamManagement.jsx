import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Avatar,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Fab,
  Tooltip
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Person as PersonIcon,
  Email as EmailIcon,
  Phone as PhoneIcon,
  MoreVert as MoreVertIcon,
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon
} from '@mui/icons-material';

const TeamManagement = () => {
  const [teamMembers, setTeamMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addMemberDialog, setAddMemberDialog] = useState(false);
  const [editMemberDialog, setEditMemberDialog] = useState(false);
  const [selectedMember, setSelectedMember] = useState(null);
  const [newMember, setNewMember] = useState({
    first_name: '',
    last_name: '',
    email: '',
    role: 'agent',
    phone: ''
  });

  useEffect(() => {
    fetchTeamMembers();
  }, []);

  const fetchTeamMembers = async () => {
    try {
      setLoading(true);
      // This would be replaced with actual API call
      // const response = await fetch('/api/team/members');
      // const data = await response.json();
      
      // Mock data for now
      const mockData = [
        {
          id: 1,
          first_name: 'Ahmed',
          last_name: 'Al-Rashid',
          email: 'ahmed@dubaielite.com',
          role: 'brokerage_owner',
          phone: '+971-50-123-4567',
          is_active: true,
          last_login: '2024-12-15T10:30:00Z',
          created_at: '2024-01-15T00:00:00Z',
          performance_score: 95
        },
        {
          id: 2,
          first_name: 'Sarah',
          last_name: 'Ahmed',
          email: 'sarah@dubaielite.com',
          role: 'agent',
          phone: '+971-50-234-5678',
          is_active: true,
          last_login: '2024-12-15T09:15:00Z',
          created_at: '2024-02-20T00:00:00Z',
          performance_score: 88
        },
        {
          id: 3,
          first_name: 'Mohammed',
          last_name: 'Hassan',
          email: 'mohammed@dubaielite.com',
          role: 'agent',
          phone: '+971-50-345-6789',
          is_active: true,
          last_login: '2024-12-14T16:45:00Z',
          created_at: '2024-03-10T00:00:00Z',
          performance_score: 92
        },
        {
          id: 4,
          first_name: 'Fatima',
          last_name: 'Khan',
          email: 'fatima@dubaielite.com',
          role: 'agent',
          phone: '+971-50-456-7890',
          is_active: false,
          last_login: '2024-12-10T14:20:00Z',
          created_at: '2024-04-05T00:00:00Z',
          performance_score: 85
        }
      ];
      
      setTeamMembers(mockData);
    } catch (err) {
      setError('Failed to load team members');
      console.error('Error fetching team members:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddMember = async () => {
    try {
      // This would be replaced with actual API call
      // const response = await fetch('/api/team/members', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(newMember)
      // });
      
      // Mock success
      const newId = Math.max(...teamMembers.map(m => m.id)) + 1;
      const addedMember = {
        id: newId,
        ...newMember,
        is_active: true,
        last_login: null,
        created_at: new Date().toISOString(),
        performance_score: 0
      };
      
      setTeamMembers([...teamMembers, addedMember]);
      setAddMemberDialog(false);
      setNewMember({
        first_name: '',
        last_name: '',
        email: '',
        role: 'agent',
        phone: ''
      });
    } catch (err) {
      setError('Failed to add team member');
      console.error('Error adding team member:', err);
    }
  };

  const handleEditMember = async () => {
    try {
      // This would be replaced with actual API call
      // const response = await fetch(`/api/team/members/${selectedMember.id}`, {
      //   method: 'PUT',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(selectedMember)
      // });
      
      // Mock success
      setTeamMembers(teamMembers.map(member => 
        member.id === selectedMember.id ? selectedMember : member
      ));
      setEditMemberDialog(false);
      setSelectedMember(null);
    } catch (err) {
      setError('Failed to update team member');
      console.error('Error updating team member:', err);
    }
  };

  const handleRemoveMember = async (memberId) => {
    if (window.confirm('Are you sure you want to remove this team member?')) {
      try {
        // This would be replaced with actual API call
        // const response = await fetch(`/api/team/members/${memberId}`, {
        //   method: 'DELETE'
        // });
        
        // Mock success
        setTeamMembers(teamMembers.filter(member => member.id !== memberId));
      } catch (err) {
        setError('Failed to remove team member');
        console.error('Error removing team member:', err);
      }
    }
  };

  const getRoleColor = (role) => {
    switch (role) {
      case 'brokerage_owner':
        return 'primary';
      case 'agent':
        return 'success';
      case 'employee':
        return 'info';
      default:
        return 'default';
    }
  };

  const getPerformanceColor = (score) => {
    if (score >= 90) return 'success';
    if (score >= 80) return 'warning';
    return 'error';
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box p={3}>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Team Management
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Manage your brokerage team members and their performance
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setAddMemberDialog(true)}
        >
          Add Team Member
        </Button>
      </Box>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Team Overview Cards */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                  <PersonIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {teamMembers.length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Members
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Avatar sx={{ bgcolor: 'success.main', mr: 2 }}>
                  <TrendingUpIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {teamMembers.filter(m => m.is_active).length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Active Members
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Avatar sx={{ bgcolor: 'info.main', mr: 2 }}>
                  <AssessmentIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {teamMembers.filter(m => m.role === 'agent').length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Agents
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Avatar sx={{ bgcolor: 'warning.main', mr: 2 }}>
                  <TrendingUpIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {Math.round(teamMembers.reduce((sum, m) => sum + m.performance_score, 0) / teamMembers.length)}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Avg Performance
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Team Members Table */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Team Members
          </Typography>
          <TableContainer component={Paper} variant="outlined">
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Member</TableCell>
                  <TableCell>Role</TableCell>
                  <TableCell>Contact</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Performance</TableCell>
                  <TableCell>Last Login</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {teamMembers.map((member) => (
                  <TableRow key={member.id}>
                    <TableCell>
                      <Box display="flex" alignItems="center">
                        <Avatar sx={{ mr: 2 }}>
                          {member.first_name[0]}{member.last_name[0]}
                        </Avatar>
                        <Box>
                          <Typography variant="subtitle2">
                            {member.first_name} {member.last_name}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            ID: {member.id}
                          </Typography>
                        </Box>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={member.role.replace('_', ' ').toUpperCase()}
                        color={getRoleColor(member.role)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Box>
                        <Box display="flex" alignItems="center" mb={0.5}>
                          <EmailIcon sx={{ mr: 1, fontSize: 16 }} />
                          <Typography variant="body2">{member.email}</Typography>
                        </Box>
                        <Box display="flex" alignItems="center">
                          <PhoneIcon sx={{ mr: 1, fontSize: 16 }} />
                          <Typography variant="body2">{member.phone}</Typography>
                        </Box>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={member.is_active ? 'Active' : 'Inactive'}
                        color={member.is_active ? 'success' : 'default'}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={`${member.performance_score}%`}
                        color={getPerformanceColor(member.performance_score)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {member.last_login 
                          ? new Date(member.last_login).toLocaleDateString()
                          : 'Never'
                        }
                      </Typography>
                    </TableCell>
                    <TableCell align="right">
                      <IconButton
                        onClick={() => {
                          setSelectedMember(member);
                          setEditMemberDialog(true);
                        }}
                      >
                        <EditIcon />
                      </IconButton>
                      <IconButton
                        onClick={() => handleRemoveMember(member.id)}
                        color="error"
                      >
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Add Member Dialog */}
      <Dialog open={addMemberDialog} onClose={() => setAddMemberDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Team Member</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="First Name"
                value={newMember.first_name}
                onChange={(e) => setNewMember({...newMember, first_name: e.target.value})}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Last Name"
                value={newMember.last_name}
                onChange={(e) => setNewMember({...newMember, last_name: e.target.value})}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Email"
                type="email"
                value={newMember.email}
                onChange={(e) => setNewMember({...newMember, email: e.target.value})}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Role</InputLabel>
                <Select
                  value={newMember.role}
                  onChange={(e) => setNewMember({...newMember, role: e.target.value})}
                >
                  <MenuItem value="agent">Agent</MenuItem>
                  <MenuItem value="employee">Employee</MenuItem>
                  <MenuItem value="brokerage_owner">Brokerage Owner</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Phone"
                value={newMember.phone}
                onChange={(e) => setNewMember({...newMember, phone: e.target.value})}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAddMemberDialog(false)}>Cancel</Button>
          <Button onClick={handleAddMember} variant="contained">Add Member</Button>
        </DialogActions>
      </Dialog>

      {/* Edit Member Dialog */}
      <Dialog open={editMemberDialog} onClose={() => setEditMemberDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Team Member</DialogTitle>
        <DialogContent>
          {selectedMember && (
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="First Name"
                  value={selectedMember.first_name}
                  onChange={(e) => setSelectedMember({...selectedMember, first_name: e.target.value})}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Last Name"
                  value={selectedMember.last_name}
                  onChange={(e) => setSelectedMember({...selectedMember, last_name: e.target.value})}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Email"
                  type="email"
                  value={selectedMember.email}
                  onChange={(e) => setSelectedMember({...selectedMember, email: e.target.value})}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Role</InputLabel>
                  <Select
                    value={selectedMember.role}
                    onChange={(e) => setSelectedMember({...selectedMember, role: e.target.value})}
                  >
                    <MenuItem value="agent">Agent</MenuItem>
                    <MenuItem value="employee">Employee</MenuItem>
                    <MenuItem value="brokerage_owner">Brokerage Owner</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Phone"
                  value={selectedMember.phone}
                  onChange={(e) => setSelectedMember({...selectedMember, phone: e.target.value})}
                />
              </Grid>
            </Grid>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditMemberDialog(false)}>Cancel</Button>
          <Button onClick={handleEditMember} variant="contained">Save Changes</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default TeamManagement;
