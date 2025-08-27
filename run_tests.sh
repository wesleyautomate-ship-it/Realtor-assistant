#!/bin/bash

# Test Runner Script for Dubai Real Estate RAG Chat System
# Simple wrapper for the comprehensive test runner

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  unit                    Run unit tests only"
    echo "  integration             Run integration tests only"
    echo "  performance             Run performance tests only"
    echo "  security                Run security tests only"
    echo "  load                    Run load tests only"
    echo "  frontend                Run frontend tests only"
    echo "  docker                  Run Docker tests only"
    echo "  all                     Run all tests"
    echo "  quick                   Run unit and integration tests"
    echo "  full                    Run all tests with full coverage"
    echo "  ci                      Run tests for CI/CD pipeline"
    echo "  --help                  Show this help message"
    echo ""
    echo "Performance Test Scenarios:"
    echo "  --smoke                 Smoke test (5 users, 1 minute)"
    echo "  --load                  Load test (20 users, 5 minutes)"
    echo "  --stress                Stress test (50 users, 10 minutes)"
    echo "  --spike                 Spike test (100 users, 5 minutes)"
    echo ""
    echo "Load Test Options:"
    echo "  --users N               Number of users for load testing (default: 20)"
    echo "  --duration N            Duration in seconds (default: 300)"
    echo ""
    echo "Other Options:"
    echo "  --parallel              Run tests in parallel where possible"
    echo "  --verbose               Verbose output"
    echo "  --timeout N             Test timeout in seconds (default: 1800)"
    echo ""
    echo "Examples:"
    echo "  $0 unit                 # Run unit tests"
    echo "  $0 quick                # Run unit and integration tests"
    echo "  $0 performance --load   # Run performance tests with load scenario"
    echo "  $0 load --users 50      # Run load tests with 50 users"
    echo "  $0 all --verbose        # Run all tests with verbose output"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check if pip is available
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is required but not installed"
        exit 1
    fi
    
    # Check if the test runner script exists
    if [ ! -f "scripts/run_tests.py" ]; then
        print_error "Test runner script not found: scripts/run_tests.py"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Function to setup virtual environment
setup_venv() {
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    print_status "Installing dependencies..."
    pip install -r requirements.txt
    
    if [ -f "tests/requirements-test.txt" ]; then
        print_status "Installing test dependencies..."
        pip install -r tests/requirements-test.txt
    fi
}

# Function to run tests
run_tests() {
    local test_types="$1"
    local performance_scenario="$2"
    local load_users="$3"
    local parallel="$4"
    local verbose="$5"
    local timeout="$6"
    
    print_status "Running tests: $test_types"
    
    # Build command
    local cmd="python scripts/run_tests.py --test-types $test_types"
    
    if [ -n "$performance_scenario" ]; then
        cmd="$cmd --performance-scenario $performance_scenario"
    fi
    
    if [ -n "$load_users" ]; then
        cmd="$cmd --load-users $load_users"
    fi
    
    if [ "$parallel" = "true" ]; then
        cmd="$cmd --parallel"
    fi
    
    if [ "$verbose" = "true" ]; then
        cmd="$cmd --verbose"
    fi
    
    if [ -n "$timeout" ]; then
        cmd="$cmd --timeout $timeout"
    fi
    
    print_status "Executing: $cmd"
    
    # Run the command
    if eval $cmd; then
        print_success "Tests completed successfully!"
        return 0
    else
        print_error "Tests failed!"
        return 1
    fi
}

# Main script logic
main() {
    # Parse command line arguments
    local test_types=""
    local performance_scenario=""
    local load_users=""
    local parallel="false"
    local verbose="false"
    local timeout=""
    
    # Default values
    local default_test_types="unit integration"
    local default_performance_scenario="load"
    local default_load_users="20"
    local default_timeout="1800"
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            unit|integration|performance|security|load|frontend|docker)
                test_types="$1"
                shift
                ;;
            all)
                test_types="unit integration performance security load frontend docker"
                shift
                ;;
            quick)
                test_types="unit integration"
                shift
                ;;
            full)
                test_types="unit integration performance security load frontend docker"
                verbose="true"
                shift
                ;;
            ci)
                test_types="unit integration performance security"
                parallel="true"
                shift
                ;;
            --smoke)
                performance_scenario="smoke"
                shift
                ;;
            --load)
                performance_scenario="load"
                shift
                ;;
            --stress)
                performance_scenario="stress"
                shift
                ;;
            --spike)
                performance_scenario="spike"
                shift
                ;;
            --users)
                load_users="$2"
                shift 2
                ;;
            --duration)
                timeout="$2"
                shift 2
                ;;
            --parallel)
                parallel="true"
                shift
                ;;
            --verbose)
                verbose="true"
                shift
                ;;
            --timeout)
                timeout="$2"
                shift 2
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Set defaults if not specified
    if [ -z "$test_types" ]; then
        test_types="$default_test_types"
    fi
    
    if [ -z "$performance_scenario" ]; then
        performance_scenario="$default_performance_scenario"
    fi
    
    if [ -z "$load_users" ]; then
        load_users="$default_load_users"
    fi
    
    if [ -z "$timeout" ]; then
        timeout="$default_timeout"
    fi
    
    # Check prerequisites
    check_prerequisites
    
    # Setup virtual environment
    setup_venv
    
    # Run tests
    if run_tests "$test_types" "$performance_scenario" "$load_users" "$parallel" "$verbose" "$timeout"; then
        print_success "All tests passed! 🎉"
        exit 0
    else
        print_error "Some tests failed! ❌"
        exit 1
    fi
}

# Run main function with all arguments
main "$@"
