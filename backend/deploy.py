#!/usr/bin/env python3
"""
Simple deployment setup - just create tables
"""
import os
import sys
sys.path.append('.')

from app.database import create_tables

def main():
    print("Creating database tables...")
    create_tables()
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    main()
