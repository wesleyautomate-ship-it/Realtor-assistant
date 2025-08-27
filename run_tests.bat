@echo off
REM Test Runner Script for Dubai Real Estate RAG Chat System (Windows)
REM Simple wrapper for the comprehensive test runner

setlocal enabledelayedexpansion

REM Colors for output (Windows 10+)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM Function to print colored output
:print_status
echo %BLUE%[INFO]%NC% %~1
goto :eof

:print_success
echo %GREEN%[SUCCESS]%NC% %~1
goto :eof

:print_warning
echo %YELLOW%[WARNING]%NC% %~1
goto :eof

:print_error
echo %RED%[ERROR]%NC% %~1
goto :eof

REM Function to show usage
:show_usage
echo Usage: %~nx0 [OPTIONS]
echo.
echo Options:
echo   unit                    Run unit tests only
echo   integration             Run integration tests only
echo   performance             Run performance tests only
echo   security                Run security tests only
echo   load                    Run load tests only
echo   frontend                Run frontend tests only
echo   docker                  Run Docker tests only
echo   all                     Run all tests
echo   quick                   Run unit and integration tests
echo   full                    Run all tests with full coverage
echo   ci                      Run tests for CI/CD pipeline
echo   --help                  Show this help message
echo.
echo Performance Test Scenarios:
echo   --smoke                 Smoke test (5 users, 1 minute)
echo   --load                  Load test (20 users, 5 minutes)
echo   --stress                Stress test (50 users, 10 minutes)
echo   --spike                 Spike test (100 users, 5 minutes)
echo.
echo Load Test Options:
echo   --users N               Number of users for load testing (default: 20)
echo   --duration N            Duration in seconds (default: 300)
echo.
echo Other Options:
echo   --parallel              Run tests in parallel where possible
echo   --verbose               Verbose output
echo   --timeout N             Test timeout in seconds (default: 1800)
echo.
echo Examples:
echo   %~nx0 unit                 # Run unit tests
echo   %~nx0 quick                # Run unit and integration tests
echo   %~nx0 performance --load   # Run performance tests with load scenario
echo   %~nx0 load --users 50      # Run load tests with 50 users
echo   %~nx0 all --verbose        # Run all tests with verbose output
goto :eof

REM Function to check prerequisites
:check_prerequisites
call :print_status "Checking prerequisites..."

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Python is required but not installed or not in PATH"
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    call :print_error "pip is required but not installed or not in PATH"
    exit /b 1
)

REM Check if the test runner script exists
if not exist "scripts\run_tests.py" (
    call :print_error "Test runner script not found: scripts\run_tests.py"
    exit /b 1
)

call :print_success "Prerequisites check passed"
goto :eof

REM Function to setup virtual environment
:setup_venv
if not exist "venv" (
    call :print_status "Creating virtual environment..."
    python -m venv venv
)

call :print_status "Activating virtual environment..."
call venv\Scripts\activate.bat

call :print_status "Installing dependencies..."
pip install -r requirements.txt

if exist "tests\requirements-test.txt" (
    call :print_status "Installing test dependencies..."
    pip install -r tests\requirements-test.txt
)
goto :eof

REM Function to run tests
:run_tests
set "test_types=%~1"
set "performance_scenario=%~2"
set "load_users=%~3"
set "parallel=%~4"
set "verbose=%~5"
set "timeout=%~6"

call :print_status "Running tests: %test_types%"

REM Build command
set "cmd=python scripts\run_tests.py --test-types %test_types%"

if not "%performance_scenario%"=="" (
    set "cmd=%cmd% --performance-scenario %performance_scenario%"
)

if not "%load_users%"=="" (
    set "cmd=%cmd% --load-users %load_users%"
)

if "%parallel%"=="true" (
    set "cmd=%cmd% --parallel"
)

if "%verbose%"=="true" (
    set "cmd=%cmd% --verbose"
)

if not "%timeout%"=="" (
    set "cmd=%cmd% --timeout %timeout%"
)

call :print_status "Executing: %cmd%"

REM Run the command
%cmd%
if errorlevel 1 (
    call :print_error "Tests failed!"
    exit /b 1
) else (
    call :print_success "Tests completed successfully!"
    exit /b 0
)

REM Main script logic
:main
REM Parse command line arguments
set "test_types="
set "performance_scenario="
set "load_users="
set "parallel=false"
set "verbose=false"
set "timeout="

REM Default values
set "default_test_types=unit integration"
set "default_performance_scenario=load"
set "default_load_users=20"
set "default_timeout=1800"

REM Parse arguments
:parse_args
if "%~1"=="" goto :end_parse
if "%~1"=="unit" (
    set "test_types=%~1"
    shift
    goto :parse_args
)
if "%~1"=="integration" (
    set "test_types=%~1"
    shift
    goto :parse_args
)
if "%~1"=="performance" (
    set "test_types=%~1"
    shift
    goto :parse_args
)
if "%~1"=="security" (
    set "test_types=%~1"
    shift
    goto :parse_args
)
if "%~1"=="load" (
    set "test_types=%~1"
    shift
    goto :parse_args
)
if "%~1"=="frontend" (
    set "test_types=%~1"
    shift
    goto :parse_args
)
if "%~1"=="docker" (
    set "test_types=%~1"
    shift
    goto :parse_args
)
if "%~1"=="all" (
    set "test_types=unit integration performance security load frontend docker"
    shift
    goto :parse_args
)
if "%~1"=="quick" (
    set "test_types=unit integration"
    shift
    goto :parse_args
)
if "%~1"=="full" (
    set "test_types=unit integration performance security load frontend docker"
    set "verbose=true"
    shift
    goto :parse_args
)
if "%~1"=="ci" (
    set "test_types=unit integration performance security"
    set "parallel=true"
    shift
    goto :parse_args
)
if "%~1"=="--smoke" (
    set "performance_scenario=smoke"
    shift
    goto :parse_args
)
if "%~1"=="--load" (
    set "performance_scenario=load"
    shift
    goto :parse_args
)
if "%~1"=="--stress" (
    set "performance_scenario=stress"
    shift
    goto :parse_args
)
if "%~1"=="--spike" (
    set "performance_scenario=spike"
    shift
    goto :parse_args
)
if "%~1"=="--users" (
    set "load_users=%~2"
    shift
    shift
    goto :parse_args
)
if "%~1"=="--duration" (
    set "timeout=%~2"
    shift
    shift
    goto :parse_args
)
if "%~1"=="--parallel" (
    set "parallel=true"
    shift
    goto :parse_args
)
if "%~1"=="--verbose" (
    set "verbose=true"
    shift
    goto :parse_args
)
if "%~1"=="--timeout" (
    set "timeout=%~2"
    shift
    shift
    goto :parse_args
)
if "%~1"=="--help" (
    call :show_usage
    exit /b 0
)
if "%~1"=="-h" (
    call :show_usage
    exit /b 0
)
call :print_error "Unknown option: %~1"
call :show_usage
exit /b 1

:end_parse
REM Set defaults if not specified
if "%test_types%"=="" set "test_types=%default_test_types%"
if "%performance_scenario%"=="" set "performance_scenario=%default_performance_scenario%"
if "%load_users%"=="" set "load_users=%default_load_users%"
if "%timeout%"=="" set "timeout=%default_timeout%"

REM Check prerequisites
call :check_prerequisites
if errorlevel 1 exit /b 1

REM Setup virtual environment
call :setup_venv

REM Run tests
call :run_tests "%test_types%" "%performance_scenario%" "%load_users%" "%parallel%" "%verbose%" "%timeout%"
if errorlevel 1 (
    call :print_error "Some tests failed! ❌"
    exit /b 1
) else (
    call :print_success "All tests passed! 🎉"
    exit /b 0
)

REM Run main function with all arguments
call :main %*
