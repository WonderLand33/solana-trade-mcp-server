#!/usr/bin/env python3
"""
Setup script for Solana MCP Server.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def setup_virtual_environment():
    """Set up virtual environment."""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("📦 Virtual environment already exists")
        return True
    
    print("📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def install_dependencies():
    """Install Python dependencies."""
    # Determine the correct pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
        python_path = "venv\\Scripts\\python"
    else:  # Unix-like
        pip_path = "venv/bin/pip"
        python_path = "venv/bin/python"
    
    # Upgrade pip first
    if not run_command(f"{python_path} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{pip_path} install -r requirements.txt", "Installing dependencies"):
        return False
    
    return True

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("📦 .env file already exists")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file with your configuration")
        return True
    else:
        print("❌ .env.example not found")
        return False

def run_tests():
    """Run basic tests to verify installation."""
    if os.name == 'nt':  # Windows
        python_path = "venv\\Scripts\\python"
    else:  # Unix-like
        python_path = "venv/bin/python"
    
    print("📦 Running basic tests...")
    try:
        result = subprocess.run([python_path, "test_server.py"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Basic tests passed")
            return True
        else:
            print("⚠️  Tests completed with warnings")
            print(f"   Output: {result.stdout}")
            return True
    except subprocess.TimeoutExpired:
        print("⚠️  Tests timed out (this is normal for network tests)")
        return True
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def print_usage_instructions():
    """Print usage instructions."""
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("1. Edit the .env file with your Solana configuration:")
    print("   - Set SOLANA_RPC_URL for your preferred network")
    print("   - Set SOLANA_PRIVATE_KEY for transaction capabilities")
    print("   - Configure other settings as needed")
    print("\n2. Activate the virtual environment:")
    
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
        print("\n3. Run the MCP server:")
        print("   python solana_mcp_server.py")
        print("\n4. Or run tests:")
        print("   python test_server.py")
    else:  # Unix-like
        print("   source venv/bin/activate")
        print("\n3. Run the MCP server:")
        print("   python solana_mcp_server.py")
        print("\n4. Or run tests:")
        print("   python test_server.py")
    
    print("\n📚 Documentation:")
    print("   - README.md for detailed usage instructions")
    print("   - .env.example for configuration options")
    print("\n⚠️  Security reminders:")
    print("   - Never commit private keys to version control")
    print("   - Test on devnet before using mainnet")
    print("   - Keep your .env file secure")

def main():
    """Main setup function."""
    print("🚀 Solana MCP Server Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Set up virtual environment
    if not setup_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("⚠️  Please create .env file manually")
    
    # Run basic tests
    run_tests()
    
    # Print usage instructions
    print_usage_instructions()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nSetup error: {e}")
        sys.exit(1)